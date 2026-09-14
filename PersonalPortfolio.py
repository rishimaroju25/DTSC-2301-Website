"""
SB 257 / Charlotte Small Business Impact Project — Data Pipeline
DTSC 2301 Portfolio Project 1

Fills Project 1 sections: Data Description, Data Cleaning and Preparation.

Requires a free Census API key: https://api.census.gov/data/key_signup.html
Set it as an environment variable before running:
    export CENSUS_API_KEY="your_key_here"

Verified against Census Bureau's own CBP API documentation
(https://www.census.gov/data/developers/data-sets/cbp-zbp/cbp-api.html)
as of the date this script was written. Confirm the current dataset year
is still valid before you rely on it — CBP lags by 1-2 years.
"""

import os
import requests
import pandas as pd

CENSUS_API_KEY = os.environ.get("b0d75ff2a6eeda05d397dd1ce82f1fb8d9a3040c")
if not CENSUS_API_KEY:
    raise RuntimeError(
        "Set CENSUS_API_KEY as an environment variable. "
        "Get one free at https://api.census.gov/data/key_signup.html"
    )

# Mecklenburg County, NC. Verify against the Census FIPS lookup if you
# want to be 100% sure before submitting: https://www.census.gov/library/reference/code-lists/ansi.html
STATE_FIPS = "37"    # North Carolina
COUNTY_FIPS = "119"  # Mecklenburg County

# 2-digit NAICS sectors worth checking for direct/indirect SB 257 exposure.
# This list is a starting point, NOT a verified provision mapping — you still
# need to read the enacted bill text / committee report to justify which
# sectors are "directly" vs "indirectly" exposed and cite the specific section.
NAICS_SECTORS = {
    "23": "Construction",
    "44-45": "Retail Trade",
    "54": "Professional, Scientific, and Technical Services",
    "61": "Educational Services",
    "62": "Health Care and Social Assistance",
    "72": "Accommodation and Food Services",
    "81": "Other Services (except Public Administration)",
}


def fetch_cbp(year: int, naics_code: str) -> pd.DataFrame:
    """Pull County Business Patterns data for one NAICS sector, Mecklenburg County."""
    url = f"https://api.census.gov/data/{year}/cbp"
    params = {
        "get": "NAME,NAICS2017_LABEL,ESTAB,EMP,PAYANN",
        "for": f"county:{COUNTY_FIPS}",
        "in": f"state:{STATE_FIPS}",
        "NAICS2017": naics_code,
        "key": CENSUS_API_KEY,
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df["year"] = year
    return df


def fetch_nonemployer(year: int, naics_code: str) -> pd.DataFrame:
    """Pull Nonemployer Statistics for one NAICS sector, Mecklenburg County.
    Catches very small / sole-proprietor firms CBP misses."""
    url = f"https://api.census.gov/data/{year}/nonemp"
    params = {
        "get": "NAME,NAICS2017_LABEL,NESTAB,NRCPTOT",
        "for": f"county:{COUNTY_FIPS}",
        "in": f"state:{STATE_FIPS}",
        "NAICS2017": naics_code,
        "key": CENSUS_API_KEY,
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df["year"] = year
    return df


def build_raw_dataset(years: list[int]) -> pd.DataFrame:
    """Pull CBP for every sector/year and merge with Nonemployer stats."""
    cbp_frames, nonemp_frames = [], []
    for year in years:
        for code in NAICS_SECTORS:
            try:
                cbp_frames.append(fetch_cbp(year, code))
            except requests.HTTPError as e:
                print(f"CBP fetch failed for {code}, {year}: {e}")
            try:
                nonemp_frames.append(fetch_nonemployer(year, code))
            except requests.HTTPError as e:
                print(f"Nonemployer fetch failed for {code}, {year}: {e}")

    cbp = pd.concat(cbp_frames, ignore_index=True) if cbp_frames else pd.DataFrame()
    nonemp = pd.concat(nonemp_frames, ignore_index=True) if nonemp_frames else pd.DataFrame()

    merged = cbp.merge(
        nonemp,
        on=["NAICS2017", "year"],
        how="outer",
        suffixes=("_cbp", "_nonemp"),
    )
    return merged


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Document every cleaning decision here with a comment — this is what
    you'll be asked to defend in the code review.
    """
    numeric_cols = ["ESTAB", "EMP", "PAYANN", "NESTAB", "NRCPTOT"]
    for col in numeric_cols:
        if col in df.columns:
            # Census suppresses some cells for disclosure avoidance; these
            # show up as null or a flag code rather than a true zero.
            # Decide explicitly: are you dropping suppressed cells or
            # imputing them? Do NOT silently coerce to 0 without saying so
            # in your write-up, that misrepresents suppressed data as
            # "no activity."
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def classify_provision_tier(row) -> str:
    """
    Placeholder logic. Replace this with your actual mapping once you've
    read the enacted SB 257 text / committee report and identified which
    sections apply to each NAICS sector. Every tier assignment should be
    traceable to a specific bill section in your write-up.
    """
    # Example structure only, not a real classification yet:
    directly_exposed = {"23"}     # e.g. construction, if budget funds building projects
    indirectly_exposed = {"61", "62"}  # e.g. education/health, if funded via appropriations
    naics = str(row.get("NAICS2017", ""))[:2]
    if naics in directly_exposed:
        return "directly_exposed"
    elif naics in indirectly_exposed:
        return "indirectly_exposed"
    return "not_materially_affected"


if __name__ == "__main__":
    # CBP typically lags 1-2 years; check the Bureau's dataset page for the
    # latest available year before running: https://www.census.gov/programs-surveys/cbp/data/datasets.html
    raw = build_raw_dataset(years=[2022, 2023])
    clean = clean_dataset(raw)
    clean["provision_tier"] = clean.apply(classify_provision_tier, axis=1)
    clean.to_csv("mecklenburg_sb257_dataset.csv", index=False)
    print(clean.head())
    print(f"\nRows: {len(clean)}")