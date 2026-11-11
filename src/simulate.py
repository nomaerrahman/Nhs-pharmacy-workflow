"""Discrete-event simulation of one community pharmacy trading day (09:00-18:00).

Demand levels come from the NHSBSA analysis (data/processed/metrics.json); process
times and behaviour shares are stated assumptions (see ASSUMPTIONS). Each scenario
is run for 300 simulated days at three demand levels, and we report:

* average and 95th-percentile wait for patients waiting for a prescription
* average wait for a clinical consultation (Pharmacy First, NMS, BP check, contraception)
* pharmacist and dispenser utilisation
* forms still unprocessed at closing (backlog that turns into overtime)
"""
from dataclasses import dataclass, replace
from pathlib import Path
import json
import random

import numpy as np
import pandas as pd
import simpy

ROOT = Path(__file__).resolve().parents[1]
METRICS = json.loads((ROOT / "data" / "processed" / "metrics.json").read_text())
OUT = ROOT / "data" / "processed"

OPEN_MIN = 9 * 60          # trading day length in minutes (09:00-18:00)
DAYS = 300                 # replications per scenario
TRADING_DAYS = 26          # per month

# Share of arrivals in each opening hour 09:00 ... 17:00 (lunchtime and after-work peaks).
HOURLY_PROFILE = [0.08, 0.10, 0.12, 0.13, 0.12, 0.10, 0.10, 0.13, 0.12]

ASSUMPTIONS = {
    "share_of_forms_collected_in_person": 0.55,
    "share_of_collections_that_wait_for_a_new_prescription": 0.25,
    "assemble_min (min, mode, max)": (2, 4, 8),
    "clinical_check_min": (0.5, 1.0, 2.0),
    "accuracy_check_min": (0.5, 1.0, 2.0),
    "hand_out_min": (1, 1.5, 3),
    "background_assemble_min": (1.5, 2.5, 4),
    "consultation_min": (8, 12, 20),
}


@dataclass(frozen=True)
class Scenario:
    name: str
    extra_dispensers: int = 0
    repeats_ready: float = 0.60       # share of repeat collections already bagged on arrival
    act_does_accuracy: bool = False   # accredited checking technician takes the accuracy check
    peak_dispenser: bool = False      # extra dispenser 11:00-14:00 and 16:00-18:00


SCENARIOS = [
    Scenario("Current process"),
    Scenario("A. Pre-assemble repeats", repeats_ready=0.95),
    Scenario("B. Accuracy checking technician", act_does_accuracy=True),
    Scenario("C. Extra peak-hour dispenser", peak_dispenser=True),
    Scenario("A + B combined", repeats_ready=0.95, act_does_accuracy=True),
]


def demand_levels() -> dict:
    forms_med = METRICS["median_forms_per_pharmacy_jul_2026"] / TRADING_DAYS
    services_med = METRICS["median_clinical_services_per_pharmacy_jul_2026"] / TRADING_DAYS
    busy_ratio = METRICS["p90_items_per_day_jul_2026"] / METRICS["median_items_per_day_jul_2026"]
    growth_items = 1 + METRICS["london_items_ytd_growth_pct"] / 100
    growth_services = (METRICS["median_clinical_services_per_pharmacy_jul_2026"]
                       / METRICS["median_clinical_services_per_pharmacy_jul_2025"])
    return {
        # (forms per day, consultations per day, dispensing staff); one pharmacist throughout
        "Median London pharmacy (2026)": (forms_med, services_med, 2),
        "Median pharmacy + 1 year growth": (forms_med * growth_items, services_med * growth_services, 2),
        "Busy pharmacy (90th percentile)": (forms_med * busy_ratio, services_med * busy_ratio, 4),
    }


def tri(rng, t):
    lo, mode, hi = t
    return rng.triangular(lo, hi, mode)


def arrival_times(rng, n_expected: float) -> list[float]:
    """Poisson arrivals with an hourly profile."""
    times = []
    for hour, share in enumerate(HOURLY_PROFILE):
        n = np.random.default_rng(rng.randrange(1 << 30)).poisson(n_expected * share)
        times += [hour * 60 + rng.random() * 60 for _ in range(n)]
    return sorted(times)


def run_day(sc: Scenario, forms_per_day: float, services_per_day: float, staff: int, seed: int) -> dict:
    rng = random.Random(seed)
    env = simpy.Environment()
    pharmacist = simpy.PriorityResource(env, capacity=1)
    dispensers = simpy.PriorityResource(env, capacity=staff + (1 if sc.peak_dispenser else 0))
    busy = {"pharmacist": 0.0, "dispensers": 0.0}
    waits, consult_waits = [], []
    done_background = [0]

    def use(res, key, minutes, priority):
        with res.request(priority=priority) as req:
            yield req
            start = env.now
            yield env.timeout(minutes)
            busy[key] += env.now - start

    def checks(priority):
        yield from use(pharmacist, "pharmacist", tri(rng, ASSUMPTIONS["clinical_check_min"]), priority)
        if sc.act_does_accuracy:
            yield from use(dispensers, "dispensers", tri(rng, ASSUMPTIONS["accuracy_check_min"]), priority)
        else:
            yield from use(pharmacist, "pharmacist", tri(rng, ASSUMPTIONS["accuracy_check_min"]), priority)

    def waiting_patient(needs_full_process: bool):
        arrive = env.now
        if needs_full_process:
            yield from use(dispensers, "dispensers", tri(rng, ASSUMPTIONS["assemble_min (min, mode, max)"]), 0)
            yield from checks(0)
        yield from use(dispensers, "dispensers", tri(rng, ASSUMPTIONS["hand_out_min"]), 0)
        waits.append(env.now - arrive)

    def consultation():
        arrive = env.now
        with pharmacist.request(priority=0) as req:
            yield req
            consult_waits.append(env.now - arrive)
            start = env.now
            yield env.timeout(tri(rng, ASSUMPTIONS["consultation_min"]))
            busy["pharmacist"] += env.now - start

    def background_form():
        # Prescriptions prepared in advance (deliveries, care homes, pre-assembly): done in idle time.
        yield from use(dispensers, "dispensers", tri(rng, ASSUMPTIONS["background_assemble_min"]), 1)
        yield from checks(1)
        done_background[0] += 1

    def schedule(times, factory):
        for t in times:
            yield env.timeout(max(0, t - env.now))
            env.process(factory())

    def peak_blocker():
        # Holds the extra dispenser slot outside 11:00-14:00 and 16:00-18:00.
        for start, end in [(0, 120), (300, 420)]:
            yield env.timeout(max(0, start - env.now))
            with dispensers.request(priority=-1) as req:
                yield req
                yield env.timeout(end - env.now)

    collections = forms_per_day * ASSUMPTIONS["share_of_forms_collected_in_person"]
    new_rx = collections * ASSUMPTIONS["share_of_collections_that_wait_for_a_new_prescription"]
    repeats = collections - new_rx

    patient_times = arrival_times(rng, collections)
    kinds = []
    for _ in patient_times:
        is_new = rng.random() < new_rx / collections
        kinds.append(True if is_new else rng.random() > sc.repeats_ready)
    it = iter(kinds)
    env.process(schedule(patient_times, lambda: waiting_patient(next(it))))
    env.process(schedule(arrival_times(rng, services_per_day), consultation))

    n_background = max(0, round(forms_per_day - sum(kinds)))
    for _ in range(n_background):
        env.process(background_form())
    if sc.peak_dispenser:
        env.process(peak_blocker())

    env.run(until=OPEN_MIN)
    disp_minutes = OPEN_MIN * staff + (300 if sc.peak_dispenser else 0)
    return {
        "mean_wait": float(np.mean(waits)) if waits else 0.0,
        "p95_wait": float(np.percentile(waits, 95)) if waits else 0.0,
        "consult_wait": float(np.mean(consult_waits)) if consult_waits else 0.0,
        "pharmacist_util": busy["pharmacist"] / OPEN_MIN,
        "dispenser_util": busy["dispensers"] / disp_minutes,
        "backlog_forms": n_background - done_background[0],
    }


def main():
    rows = []
    for level, (forms, services, staff) in demand_levels().items():
        for sc in SCENARIOS:
            days = pd.DataFrame([run_day(sc, forms, services, staff, seed=d) for d in range(DAYS)])
            rows.append({
                "demand_level": level,
                "scenario": sc.name,
                "forms_per_day": round(forms),
                "consultations_per_day": round(services, 1),
                "dispensing_staff": staff,
                "avg_wait_min": round(float(days.mean_wait.mean()), 1),
                "p95_wait_min": round(float(days.p95_wait.mean()), 1),
                "avg_consult_wait_min": round(float(days.consult_wait.mean()), 1),
                "pharmacist_utilisation_pct": int(round(100 * days.pharmacist_util.mean())),
                "dispenser_utilisation_pct": int(round(100 * days.dispenser_util.mean())),
                "backlog_forms_at_close": int(round(days.backlog_forms.mean())),
            })
            print(" | ".join(str(v) for v in rows[-1].values()))
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "simulation_results.csv", index=False)
    (OUT / "simulation_assumptions.json").write_text(json.dumps(
        {"assumptions": ASSUMPTIONS, "hourly_profile": HOURLY_PROFILE, "days_per_scenario": DAYS}, indent=2))


if __name__ == "__main__":
    main()
