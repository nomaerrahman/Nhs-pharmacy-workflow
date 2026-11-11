# Business case: freeing pharmacist time in busy London pharmacies

## Recommendation

Pilot **pre-assembled repeat prescriptions (A)** together with an **accuracy checking technician (B)** at one busy branch for three months. In the simulation of a busy London pharmacy, the combination cuts the average wait for a prescription from **14 to 6 minutes** and the 95th-percentile wait from **48 to 20 minutes**. It also reduces the work left unfinished at closing from **174 forms to 11**, without adding a pharmacist.

## Why act now

- **Clinical work is growing much faster than dispensing.** Between Jan–Jul 2025 and Jan–Jul 2026, London pharmacies dispensed 2.5% more items, but delivered **20.5% more Pharmacy First consultations**. The median pharmacy's monthly clinical services (Pharmacy First, New Medicine Service, blood pressure checks, contraception) rose from 142 to 181, up 27% year on year.
- **Capacity isn't growing.** London had 1,714 pharmacies in Jan 2025 and 1,716 in Jul 2026.
- **The pharmacist is the bottleneck.** In the simulation, a busy pharmacy's pharmacist is occupied 99% of the opening day. Every consultation pauses prescription checking.

## Options compared

Simulated busy London pharmacy: 294 prescription forms and 14 consultations a day, 1 pharmacist and 4 dispensing staff, 300 simulated days per option.

| Option | Avg wait (min) | 95th-pct wait (min) | Consultation wait (min) | Pharmacist busy | Forms unfinished at close |
| --- | ---: | ---: | ---: | ---: | ---: |
| Current process | 14.0 | 47.7 | 7.8 | 99% | 174 |
| A. Pre-assemble repeats | 6.6 | 28.1 | 5.2 | 99% | 195 |
| B. Accuracy checking technician | 9.5 | 27.6 | 5.4 | 93% | 10 |
| C. Extra peak-hour dispenser | 13.9 | 47.8 | 7.9 | 99% | 174 |
| **A + B combined** | **5.6** | **19.6** | **4.5** | **94%** | **11** |

**What the simulation shows**

- **C does nothing.** Dispensers aren't the bottleneck, so adding dispensing hours, the most common response to busy periods, doesn't shorten waits.
- **A alone moves work around rather than creating capacity.** Patients wait less, but the pharmacist is still fully booked, and more work is left at closing.
- **B creates pharmacist capacity**, and A turns that capacity into shorter waits. They work best together.

At the median London pharmacy (147 forms a day, 2 dispensing staff), A + B cuts the 95th-percentile wait from 23 to 15 minutes. It also frees the pharmacist from being busy 80% of the day to 49%, leaving room for next year's growth in consultations.

## Costs and benefits

| | Detail |
| --- | --- |
| **One-off costs** | Updated standard operating procedure; recruiting or seconding an accredited checking technician; a dispensing system change to log who checked each item |
| **Ongoing costs** | Pay difference for the ACT role (no extra headcount); storage space for bagged repeats |
| **Benefits** | Shorter waits; less overtime to clear end-of-day work; more pharmacist time for funded clinical services (Pharmacy First, NMS, blood pressure checks) |
| **Not quantified here** | Actual pay rates and service fees vary by branch and contract; the pilot should measure them |

## Risks

The full RAID log is in [project_plan.md](project_plan.md). The main risk is dispensing accuracy: the pharmacist keeps every clinical check, only accredited technicians do accuracy checks, and errors are reviewed monthly.

## Success measures for the pilot

1. 95th-percentile prescription wait under 25 minutes (measured, not simulated)
2. Forms unfinished at closing under 20 a day
3. No increase in dispensing errors reported
4. Pharmacy First consultations delivered per week maintained or increased

## Assumptions

Demand comes from NHSBSA data. Process times and patient behaviour are assumptions, listed in `data/processed/simulation_assumptions.json`, and should be replaced with times measured during the pilot's baseline week.
