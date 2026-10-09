"""Beat the Delay: download and clean the TTC subway delay open data.

Run:  python pipeline/clean_ttc_delays.py
Needs: pandas, requests

What it does
1. Downloads "TTC Subway Delay Data since 2025" and the delay code list from
   City of Toronto Open Data (Open Government Licence - Toronto).
2. Keeps delays longer than zero minutes on Lines 1, 2 and 4.
3. Standardises station names (for example, "BLOOR STATION" on Line 1 and
   "YONGE BD STATION" on Line 2 both become "Bloor-Yonge").
4. Groups the TTC delay codes into ten plain-English causes.
5. Writes the clean file plus the Power BI star schema and the two mapping tables.

Re-run it each month: the city refreshes the source monthly, and every Excel
formula and Power BI measure recalculates from the new files.
"""
import io
import re
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CKAN = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show?id=ttc-subway-delay-data"

STATIONS = [
    "Bathurst", "Bay", "Bayview", "Bessarion", "Bloor-Yonge", "Broadview", "Castle Frank", "Cedarvale", "Chester",
    "Christie", "College", "Coxwell", "Davisville", "Don Mills", "Donlands", "Downsview Park", "Dufferin", "Dundas West",
    "Dupont", "Eglinton", "Finch", "Finch West", "Glencairn", "Greenwood", "High Park", "Highway 407", "Islington", "Jane",
    "Keele", "Kennedy", "King", "Kipling", "Lansdowne", "Lawrence", "Lawrence West", "Leslie", "Main Street", "Museum",
    "North York Centre", "Old Mill", "Osgoode", "Ossington", "Pape", "Pioneer Village", "Queen", "Queen's Park", "Rosedale",
    "Royal York", "Runnymede", "Sheppard West", "Sheppard-Yonge", "Sherbourne", "Spadina", "St Andrew", "St Clair",
    "St Clair West", "St George", "St Patrick", "Summerhill", "TMU (Dundas)", "Union", "Vaughan Metropolitan Centre",
    "Victoria Park", "Warden", "Wellesley", "Wilson", "Woodbine", "York Mills", "York University", "Yorkdale",
]
ALIASES = {
    "BLOOR": "Bloor-Yonge", "YONGE BD": "Bloor-Yonge", "YONGE": "Bloor-Yonge", "KENNEDY BD": "Kennedy",
    "ST GEORGE BD": "St George", "ST GEORGE YUS": "St George", "ST GEORGE YU": "St George",
    "SPADINA BD": "Spadina", "SPADINA YUS": "Spadina", "SPADINA YU": "Spadina",
    "VMC": "Vaughan Metropolitan Centre", "VAUGHAN MC": "Vaughan Metropolitan Centre",
    "SHEPPARD": "Sheppard-Yonge", "NORTH YORK CTR": "North York Centre", "CEDARVALE YU": "Cedarvale",
    "EGLINTON WEST": "Cedarvale", "TMU": "TMU (Dundas)", "DUNDAS": "TMU (Dundas)",
}
LINES = {"YU": "Line 1", "YUS": "Line 1", "BD": "Line 2", "SHP": "Line 4"}
PEOPLE = {"Disorderly or security", "Customer illness or injury", "Track-level emergencies",
          "Alarms with no trouble found", "Unsanitary vehicle"}


def station_key(raw: str) -> str:
    s = raw.upper().strip()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"\b(STATION|STN|STATIO|STA|STAT)\b.*$", "", s).strip()
    return re.sub(r"\s+", " ", s).strip(" -.").replace("ST. ", "ST ")


def clean_station(raw: str) -> str:
    key = station_key(raw)
    if key in ALIASES:
        return ALIASES[key]
    lookup = {name.upper(): name for name in STATIONS}
    return lookup.get(key, "Line-wide or yard")


def cause_group(code: str) -> str:
    if code.startswith("MUI"):
        return "Customer illness or injury"
    if code in ("SUUT", "MUPR1", "PUTDN", "MUPLB", "MUPLA", "MUPLC"):
        return "Track-level emergencies"
    if code in ("MUWEA", "PUTIS", "PUSIS"):
        return "Weather"
    if code in ("MUPAA", "EUNT", "SUEAS"):
        return "Alarms with no trouble found"
    if code.startswith("SU"):
        return "Disorderly or security"
    if code.startswith("EU") or code in ("MUDD", "MUD"):
        return "Train and door faults"
    if code.startswith("PU"):
        return "Track and signals"
    if code.startswith("TU") or code == "MUTO":
        return "Operations and staffing"
    if code == "MUSAN":
        return "Unsanitary vehicle"
    return "Other"


def resource_url(meta: dict, name: str) -> str:
    for r in meta["result"]["resources"]:
        if r["name"] == name:
            return r["url"]
    raise KeyError(name)


def main() -> None:
    meta = requests.get(CKAN, timeout=60).json()
    raw = pd.read_csv(io.StringIO(requests.get(resource_url(meta, "TTC Subway Delay Data since 2025.csv"), timeout=120).text))
    codes = pd.read_csv(io.StringIO(requests.get(resource_url(meta, "Code Descriptions.csv"), timeout=60).text))

    raw["Code"] = raw["Code"].str.strip()
    raw["Line"] = raw["Line"].fillna("").str.strip().map(lambda x: LINES.get(x, "Multiple lines" if "/" in x else None))
    raw = raw[(raw["Min Delay"] > 0) & raw["Line"].notna()].copy()
    raw["Station Clean"] = raw["Station"].map(clean_station)
    raw["Cause"] = raw["Code"].map(cause_group)
    raw["Hour"] = raw["Time"].str[:2].astype(int)

    out = raw.rename(columns={"Min Delay": "Minutes"})
    out = out[["Date", "Day", "Hour", "Line", "Station Clean", "Cause", "Code", "Minutes"]].rename(columns={"Station Clean": "Station"})
    (ROOT / "data").mkdir(exist_ok=True)
    out.to_csv(ROOT / "data" / "ttc_subway_delays_2025_2026.csv", index=False)

    # mapping tables, so every cleaning decision can be audited
    smap = raw[["Station", "Station Clean"]].drop_duplicates().sort_values("Station")
    smap.columns = ["Station as published", "Station used"]
    smap.to_csv(ROOT / "data" / "station_map.csv", index=False)
    cm = codes.rename(columns={"CODE": "Code", "DESCRIPTION": "Description"})[["Code", "Description"]]
    cm["Code"] = cm["Code"].str.strip()
    cm["Cause"] = cm["Code"].map(cause_group)
    cm["Cause Type"] = cm["Cause"].map(lambda c: "People-related" if c in PEOPLE else "Equipment, track, operations or other")
    cm.to_csv(ROOT / "data" / "cause_code_map.csv", index=False)
    print(f"{len(out):,} delays, {out['Minutes'].sum():,} minutes, {out['Date'].min()} to {out['Date'].max()}")


if __name__ == "__main__":
    main()
