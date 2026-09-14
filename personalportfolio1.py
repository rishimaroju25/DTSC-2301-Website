"""
SB 257 / Charlotte Small Business Impact Project — QCEW Fallback Pipeline
DTSC 2301 Portfolio Project 1
"""

import pandas as pd

AREA_CODE = "37119"  # Mecklenburg County, NC


def fetch_qcew_area(year: int, quarter: str = "a") -> pd.DataFrame:
    """Pull all industries for Mecklenburg County for one year.
    quarter='a' gives annual averages; use '1','2','3','4' for a specific quarter."""
    url = f"https://data.bls.gov/cew/data/api/{year}/{quarter}/area/{AREA_CODE}.csv"
    df = pd.read_csv(url)
    df["year"] = year
    df["quarter"] = quarter
    return df


def fetch_qcew_multi_year(years: list[int], quarter: str = "a") -> pd.DataFrame:
    frames = []
    for year in years:
        try:
            frames.append(fetch_qcew_area(year, quarter))
        except Exception as e:
            print(f"Failed to fetch {year} Q{quarter}: {e}")
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def clean_qcew(df: pd.DataFrame) -> pd.DataFrame:
    """
    QCEW's raw area file includes every ownership type (federal, state,
    local government, private) and every NAICS aggregation level at once.
    Document your filtering choices explicitly here for the code review.
    """
    # own_code 5 = Private ownership only — excludes government employers,
    # which aren't "small businesses" in any meaningful sense for this study.
    if "own_code" in df.columns:
        df = df[df["own_code"] == 5].copy()

    # agglvl_code identifies aggregation level (state total, county total,
    # by-industry, by-supersector, etc.). Keep only county-by-NAICS-industry
    # rows so you're not double-counting totals as if they were industries.
    # Check the agglvl_titles reference file to confirm which code you want:
    # https://www.bls.gov/cew/classifications/aggregation/agg-level-titles.htm

    numeric_cols = ["annual_avg_estabs", "annual_avg_emplvl", "total_annual_wages"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


if __name__ == "__main__":
    # Adjust years based on what's actually published — check
    # https://www.bls.gov/cew/ for the latest release before assuming 2024
    # is current.
    raw = fetch_qcew_multi_year(years=[2022, 2023, 2024], quarter="a")
    clean = clean_qcew(raw)
    clean.to_csv("mecklenburg_qcew_dataset.csv", index=False)
    print(clean.head())
    print(f"\nRows: {len(clean)}")
