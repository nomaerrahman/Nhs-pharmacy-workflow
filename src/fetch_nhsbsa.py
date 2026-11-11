"""Download community pharmacy activity from the NHSBSA Open Data Portal.

Source: "Pharmacy and appliance contractor dispensing data" (monthly, England).
The portal exposes each monthly file through a SQL API, so the aggregation runs
server-side and only the summary rows are downloaded:

* data/raw/pharmacy_month.csv : one row per London pharmacy per month
* data/raw/icb_month.csv      : one row per ICB in England per month
"""
from pathlib import Path
import json
import time
import urllib.parse
import urllib.request

import pandas as pd

API = "https://opendata.nhsbsa.net/api/3/action"
DATASET = "25230765-9494-4fde-b3fc-af9c00037dfb"
RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

METRICS = {
    "items": "CONTENT = 'Items'",
    "forms": "CONTENT = 'Forms'",
    "eps_items": "CONTENT = 'Items processed via Electronic Prescription Service (EPS)'",
    "pharmacy_first": "CONTENT LIKE 'Pharmacy First%'",
    "nms": "CONTENT = 'New Medicine Service (NMS) interventions declared'",
    "bp_checks": "CONTENT = 'Community Pharmacy Clinic Blood Pressure checks'",
    "contraception": "CONTENT LIKE 'Community Pharmacy Contraceptive%'",
}


def _get(action: str, **params) -> dict:
    url = f"{API}/{action}?{urllib.parse.urlencode(params)}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                return json.load(r)
        except Exception as exc:  # network hiccup: back off and retry
            if attempt == 3:
                raise
            print(f"  retry after {exc}")
            time.sleep(5 * (attempt + 1))


def monthly_resources() -> list[str]:
    res = _get("package_show", id=DATASET)["result"]["resources"]
    names = [r["name"] for r in res if r["name"].startswith("DISPENSING_DATA_2025") or r["name"].startswith("DISPENSING_DATA_2026")]
    return sorted(names)


def sql(resource: str, query: str) -> pd.DataFrame:
    out = _get("datastore_search_sql", resource_id=resource, sql=query)
    if not out.get("success"):
        raise RuntimeError(out)
    return pd.DataFrame(out["result"]["result"]["records"])


def pivot_cols() -> str:
    return ",\n".join(
        f"SUM(IF({cond}, SAFE_CAST(VALUE AS FLOAT64), 0)) AS {name}" for name, cond in METRICS.items()
    )


def fetch() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    pharm, icb = [], []
    for res in monthly_resources():
        print(f"Fetching {res}")
        pharm.append(sql(res, f"""
            SELECT YEAR_MONTH, ICB_NAME, HWB_NAME, CONTRACTOR_CODE,
                   ANY_VALUE(CONTRACTOR_NAME) AS CONTRACTOR_NAME, ANY_VALUE(POSTCODE) AS POSTCODE,
                   {pivot_cols()}
            FROM `{res}`
            WHERE ICB_NAME LIKE '%LONDON%' AND PHARMACY_ACCOUNT_TYPE = 'Pharmacy'
            GROUP BY YEAR_MONTH, ICB_NAME, HWB_NAME, CONTRACTOR_CODE
        """))
        icb.append(sql(res, f"""
            SELECT YEAR_MONTH, ICB_NAME,
                   COUNT(DISTINCT CONTRACTOR_CODE) AS pharmacies,
                   {pivot_cols()}
            FROM `{res}`
            WHERE PHARMACY_ACCOUNT_TYPE = 'Pharmacy'
            GROUP BY YEAR_MONTH, ICB_NAME
        """))
    pd.concat(pharm).to_csv(RAW / "pharmacy_month.csv", index=False)
    pd.concat(icb).to_csv(RAW / "icb_month.csv", index=False)
    print("Saved", RAW / "pharmacy_month.csv", "and", RAW / "icb_month.csv")


if __name__ == "__main__":
    fetch()
