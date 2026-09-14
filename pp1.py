"""
SB 257 / Charlotte Small Business Impact Project — Filter, Label, Plot
DTSC 2301 Portfolio Project 1
"""

import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "mecklenburg_qcew_dataset.csv"

# NAICS 2-digit sector titles. Pulled from BLS's own high-level industry
# reference. Verify against https://www.bls.gov/cew/classifications/industry/high-level-industries.htm
# if you add sectors not listed here, some codes are hyphenated (31-33,
# 44-45, 48-49) and QCEW represents these as separate industry_code values,
# not literal hyphens.
NAICS_SECTOR_TITLES = {
    "1011": "Natural Resources and Mining",
    "1012": "Construction",
    "1013": "Manufacturing",
    "1021": "Trade, Transportation, and Utilities",
    "1022": "Information",
    "1023": "Financial Activities",
    "1024": "Professional and Business Services",
    "1025": "Education and Health Services",
    "1026": "Leisure and Hospitality",
    "1027": "Other Services",
    "1028": "Public Administration",
    "1029": "Unclassified",
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
    ax.legend(title="Sector", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig("employment_trend_by_sector.png", dpi=150)
    plt.close(fig)


def plot_wage_vs_employment(df: pd.DataFrame, year: int):
    """Scatter: average annual pay vs. employment level, one point per sector, for one year."""
    subset = df[df["year"] == year]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(subset["annual_avg_emplvl"], subset["avg_annual_pay"])
    for _, row in subset.iterrows():
        ax.annotate(row["industry_title"], (row["annual_avg_emplvl"], row["avg_annual_pay"]),
                    fontsize=8, alpha=0.75)
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
