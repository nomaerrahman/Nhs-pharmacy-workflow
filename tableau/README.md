# Tableau Public dashboard

Build the dashboard from `data/processed/london_pharmacy_month.csv` in **Tableau Public** (free, Windows and Mac) and publish it to your Tableau Public profile so recruiters can open it in a browser.

## Data source

1. **Connect → Text file →** `data/processed/london_pharmacy_month.csv`.
2. Check `month` is a Date and `CONTRACTOR_CODE` is a String dimension.
3. Create these calculated fields:

```
Clinical services   = [pharmacy_first] + [nms] + [bp_checks] + [contraception]
Items per day       = [items] / 26
Pharmacies          = COUNTD([CONTRACTOR_CODE])
Items per pharmacy  = SUM([items]) / COUNTD([CONTRACTOR_CODE])
EPS share           = SUM([eps_items]) / SUM([items])
```

## Sheets

| Sheet | Build |
| --- | --- |
| **Trend** | Columns: MONTH(`month`) · Rows: SUM(`items`) and SUM(`pharmacy_first`) as two separate line charts (not dual axis), plus `Pharmacies` |
| **By ICB** | Bar: `ICB_NAME` × `Items per pharmacy`, coloured by ICB; filter to latest month |
| **By borough** | Bar or map: `HWB_NAME` (borough) × SUM(`pharmacy_first`), sorted descending |
| **Pharmacy workload** | Histogram of `Items per day` for the latest month, with a reference line at the median (282) and 90th percentile (563) |
| **Top pharmacies** | Table: `CONTRACTOR_NAME`, `POSTCODE`, `Items per day`, `Clinical services`, top 20 by items |

## Dashboard

Put Trend across the top, By ICB and By borough in the middle, and Pharmacy workload and Top pharmacies at the bottom. Add a month filter applied to all sheets. Title it *"London community pharmacy: demand vs capacity, 2025–2026"*.

Publish with **File → Save to Tableau Public**, then add the link to the main README.
