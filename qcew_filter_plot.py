"""
SB 257 / Charlotte Small Business Impact Project — Filter, Label, Plot
DTSC 2301 Portfolio Project 1

Run AFTER qcew_fallback_pipeline.py has produced mecklenburg_qcew_dataset.csv.

Filters to county-level NAICS Sector data (agglvl_code 74), joins in
readable industry names, and produces two visualizations tied to the
employment-trend variable in your research question.

Industry title reference verified against:
https://www.bls.gov/cew/classifications/industry/high-level-industries.htm
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

INPUT_FILE = "mecklenburg_qcew_dataset.csv"

# NAICS 2017 2-digit sector titles. Corrected against the actual
# industry_code values confirmed present in the real data output
# (11, 21, 22, 23, 31-33, 42, 44-45, 48-49, 51, 52, 53, 54, 55, 56, 61,
# 62, 71, 72, 81, 99) rather than assumed from documentation alone.
NAICS_SECTOR_TITLES = {
    "11": "Agriculture, Forestry, Fishing and Hunting",
    "21": "Mining, Quarrying, and Oil and Gas Extraction",
    "22": "Utilities",
    "23": "Construction",
    "31-33": "Manufacturing",
    "42": "Wholesale Trade",
    "44-45": "Retail Trade",
    "48-49": "Transportation and Warehousing",
    "51": "Information",
    "52": "Finance and Insurance",
    "53": "Real Estate and Rental and Leasing",
    "54": "Professional, Scientific, and Technical Services",
    "55": "Management of Companies and Enterprises",
    "56": "Administrative and Support and Waste Management Services",
    "61": "Educational Services",
    "62": "Health Care and Social Assistance",
    "71": "Arts, Entertainment, and Recreation",
    "72": "Accommodation and Food Services",
    "81": "Other Services (except Public Administration)",
    "99": "Unclassified",
}


def load_and_filter(path: str, agglvl: int = 74) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"industry_code": str})
    df = df[df["agglvl_code"] == agglvl].copy()
    df["industry_title"] = df["industry_code"].map(NAICS_SECTOR_TITLES)
    df["industry_title"] = df["industry_title"].fillna(df["industry_code"])
    return df


def plot_employment_trend(df: pd.DataFrame, top_n: int = 8):
    """Line chart: employment by sector, Mecklenburg County, over available years."""
    pivot = df.pivot_table(
        index="year", columns="industry_title",
        values="annual_avg_emplvl", aggfunc="sum"
    )
    # Keep only the largest sectors by most recent year so the chart stays readable
    top_sectors = pivot.iloc[-1].sort_values(ascending=False).head(top_n).index
    pivot = pivot[top_sectors]

    fig, ax = plt.subplots(figsize=(10, 6))
    pivot.plot(ax=ax, marker="o")
    ax.set_title("Mecklenburg County Employment by Industry Sector (2022-2024)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Annual Employment")
    # Force whole-number year ticks instead of matplotlib's default
    # fractional ticks (2022.00, 2022.25, ...) on a 3-point numeric axis.
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend(title="Sector", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig("employment_trend_by_sector.png", dpi=150)
    plt.close(fig)


def plot_wage_vs_employment(df: pd.DataFrame, year: int):
    """Scatter: average annual pay vs. employment level, one point per sector, for one year."""
    subset = df[df["year"] == year].copy()
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.scatter(subset["annual_avg_emplvl"], subset["avg_annual_pay"], zorder=3)

    # Simple collision avoidance: normalize both axes to 0-1 so "closeness"
    # accounts for the very different scales of employment (0-90k) vs pay
    # ($0-$160k), then nudge a label vertically (alternating up/down, with
    # growing offset) whenever it lands within a small radius of a label
    # already placed. This is a plain heuristic, not a real layout solver
    # (no external "adjustText"-style dependency needed for a quick fix).
    x = subset["annual_avg_emplvl"].to_numpy(dtype=float)
    y = subset["avg_annual_pay"].to_numpy(dtype=float)
    x_norm = (x - x.min()) / (x.max() - x.min() + 1e-9)
    y_norm = (y - y.min()) / (y.max() - y.min() + 1e-9)

    placed = []
    threshold = 0.05
    for i, (_, row) in enumerate(subset.iterrows()):
        offset_y = 6  # points, in font-offset space
        direction = 1
        step = 0
        while any(
            abs(x_norm[i] - px) < threshold and abs(y_norm[i] - py) < threshold
            for px, py in placed
        ) and step < 6:
            step += 1
            direction *= -1
            offset_y = 6 + direction * step * 10

        placed.append((x_norm[i], y_norm[i]))
        ax.annotate(
            row["industry_title"],
            (row["annual_avg_emplvl"], row["avg_annual_pay"]),
            textcoords="offset points",
            xytext=(6, offset_y),
            fontsize=7.5,
            alpha=0.85,
        )

    ax.set_title(f"Sector Employment vs. Average Annual Pay, Mecklenburg County ({year})")
    ax.set_xlabel("Average Annual Employment")
    ax.set_ylabel("Average Annual Pay ($)")
    fig.tight_layout()
    fig.savefig(f"wage_vs_employment_{year}.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    data = load_and_filter(INPUT_FILE, agglvl=74)
    print("Industry codes present at this aggregation level:")
    print(data["industry_code"].unique())
    print("\nColumns available:")
    print(data.columns.tolist())

    plot_employment_trend(data)
    plot_wage_vs_employment(data, year=data["year"].max())
    print("\nSaved: employment_trend_by_sector.png, wage_vs_employment_<year>.png")
