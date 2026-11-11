"""Clean the NHSBSA extracts, compute headline demand metrics and export Tableau-ready files.

Outputs
* data/processed/london_pharmacy_month.csv  tidy, harmonised pharmacy-level table (Tableau source)
* data/processed/england_icb_month.csv      ICB-level table for England context
* data/processed/metrics.json              headline numbers used in the README and the simulation
"""
from pathlib import Path
import json
import re

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

METRICS = ["items", "forms", "eps_items", "pharmacy_first", "nms", "bp_checks", "contraception"]
TRADING_DAYS_PER_MONTH = 26  # Mon-Sat opening; an explicit assumption


def harmonise_icb(name: str) -> str:
    """Standardise ICB names across months.

    The portal changed naming in Mar 2026, and on 1 Apr 2026 North Central and
    North West London ICBs merged into West and North London ICB. All months are
    mapped onto the current four-ICB structure so trends are comparable.
    """
    n = re.sub(r"^NHS ", "", name.upper())
    n = re.sub(r"INTEGRATED CARE BOARD.*$", "ICB", n).strip()
    if n in {"NORTH CENTRAL LONDON ICB", "NORTH WEST LONDON ICB"}:
        return "WEST AND NORTH LONDON ICB"
    return n


def load():
    p = pd.read_csv(RAW / "pharmacy_month.csv")
    i = pd.read_csv(RAW / "icb_month.csv")
    for df in (p, i):
        df["ICB_NAME"] = df["ICB_NAME"].map(harmonise_icb)
        df["month"] = pd.to_datetime(df["YEAR_MONTH"] + "-01")
    p = p[p["items"] > 0].copy()  # drop pharmacies with no dispensing that month (opening/closing)
    p["items_per_day"] = p["items"] / TRADING_DAYS_PER_MONTH
    p["eps_share"] = p["eps_items"] / p["items"]
    return p, i


def ytd(df, year, cols):
    m = df[(df.month.dt.year == year) & (df.month.dt.month <= 7)]
    return m[cols].sum()


def main():
    p, i = load()
    p.to_csv(OUT / "london_pharmacy_month.csv", index=False)
    i.to_csv(OUT / "england_icb_month.csv", index=False)

    lon_25, lon_26 = ytd(p, 2025, METRICS), ytd(p, 2026, METRICS)
    eng_25, eng_26 = ytd(i, 2025, ["items", "pharmacy_first"]), ytd(i, 2026, ["items", "pharmacy_first"])
    count = p.groupby("month").CONTRACTOR_CODE.nunique()
    jul = p[p.YEAR_MONTH == "2026-07"]
    jul25 = p[p.YEAR_MONTH == "2025-07"]

    metrics = {
        "period": "Jan 2025 - Jul 2026",
        "london_pharmacies_jan_2025": int(count.iloc[0]),
        "london_pharmacies_jul_2026": int(count.iloc[-1]),
        "london_items_ytd_growth_pct": round(100 * (lon_26["items"] / lon_25["items"] - 1), 1),
        "london_pharmacy_first_ytd_growth_pct": round(100 * (lon_26["pharmacy_first"] / lon_25["pharmacy_first"] - 1), 1),
        "london_nms_ytd_growth_pct": round(100 * (lon_26["nms"] / lon_25["nms"] - 1), 1),
        "london_contraception_ytd_growth_pct": round(100 * (lon_26["contraception"] / lon_25["contraception"] - 1), 1),
        "england_items_ytd_growth_pct": round(100 * (eng_26["items"] / eng_25["items"] - 1), 1),
        "england_pharmacy_first_ytd_growth_pct": round(100 * (eng_26["pharmacy_first"] / eng_25["pharmacy_first"] - 1), 1),
        "london_items_jul_2026": int(jul["items"].sum()),
        "london_eps_share_jul_2026_pct": round(100 * jul["eps_items"].sum() / jul["items"].sum(), 1),
        "median_items_per_pharmacy_jul_2026": int(jul["items"].median()),
        "median_items_per_pharmacy_jul_2025": int(jul25["items"].median()),
        "median_forms_per_pharmacy_jul_2026": int(jul["forms"].median()),
        "median_pharmacy_first_per_pharmacy_jul_2026": int(jul["pharmacy_first"].median()),
        "median_items_per_day_jul_2026": round(jul["items_per_day"].median(), 0),
        "p90_items_per_day_jul_2026": round(jul["items_per_day"].quantile(0.9), 0),
        "median_clinical_services_per_pharmacy_jul_2026": int(
            jul[["pharmacy_first", "nms", "bp_checks", "contraception"]].sum(axis=1).median()),
        "median_clinical_services_per_pharmacy_jul_2025": int(
            jul25[["pharmacy_first", "nms", "bp_checks", "contraception"]].sum(axis=1).median()),
    }
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
