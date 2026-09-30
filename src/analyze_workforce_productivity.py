from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# 1. Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dhl_segment_financials_kpi.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dhl_workforce_productivity_analysis.csv"
)


# ---------------------------------------------------------
# 2. Load data
# ---------------------------------------------------------

try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Could not find:\n{INPUT_FILE}\n"
        "Run calculate_segment_kpis.py first."
    )


# ---------------------------------------------------------
# 3. Keep operating divisions
# ---------------------------------------------------------

operating_divisions = [
    "Express",
    "Global Forwarding Freight",
    "Supply Chain",
    "eCommerce",
    "Post & Parcel Germany"
]

df = df[
    df["segment"].isin(operating_divisions)
].copy()


# ---------------------------------------------------------
# 4. Keep 2024 and 2025
# ---------------------------------------------------------

df = df[
    df["year"].isin([2024, 2025])
].copy()


# ---------------------------------------------------------
# 5. Create 2024 / 2025 tables
# ---------------------------------------------------------

df_2024 = (
    df[df["year"] == 2024]
    .set_index("segment")
)

df_2025 = (
    df[df["year"] == 2025]
    .set_index("segment")
)


# ---------------------------------------------------------
# 6. Create analysis table
# ---------------------------------------------------------

analysis = pd.DataFrame(
    index=operating_divisions
)


# Workforce
analysis["fte_2024"] = (
    df_2024["average_fte"]
)

analysis["fte_2025"] = (
    df_2025["average_fte"]
)

analysis["fte_change"] = (
    analysis["fte_2025"]
    - analysis["fte_2024"]
)

analysis["fte_growth_pct"] = (
    analysis["fte_change"]
    / analysis["fte_2024"]
    * 100
)


# Revenue per FTE
analysis["revenue_per_fte_2024_eur"] = (
    df_2024["external_revenue_per_fte_eur"]
)

analysis["revenue_per_fte_2025_eur"] = (
    df_2025["external_revenue_per_fte_eur"]
)

analysis["revenue_per_fte_change_pct"] = (
    (
        analysis["revenue_per_fte_2025_eur"]
        /
        analysis["revenue_per_fte_2024_eur"]
    )
    - 1
) * 100


# EBIT per FTE
analysis["ebit_per_fte_2024_eur"] = (
    df_2024["ebit_per_fte_eur"]
)

analysis["ebit_per_fte_2025_eur"] = (
    df_2025["ebit_per_fte_eur"]
)

analysis["ebit_per_fte_change_pct"] = (
    (
        analysis["ebit_per_fte_2025_eur"]
        /
        analysis["ebit_per_fte_2024_eur"]
    )
    - 1
) * 100


# ---------------------------------------------------------
# 7. Round percentages
# ---------------------------------------------------------

percentage_columns = [
    "fte_growth_pct",
    "revenue_per_fte_change_pct",
    "ebit_per_fte_change_pct"
]

for column in percentage_columns:
    analysis[column] = analysis[column].round(2)


# ---------------------------------------------------------
# 8. Reset index
# ---------------------------------------------------------

analysis = analysis.reset_index(names="segment")


# ---------------------------------------------------------
# 9. Display results
# ---------------------------------------------------------

print("\nDHL Workforce & Productivity Analysis")
print("=" * 120)

print(
    analysis[
        [
            "segment",
            "fte_2024",
            "fte_2025",
            "fte_growth_pct",
            "revenue_per_fte_2024_eur",
            "revenue_per_fte_2025_eur",
            "revenue_per_fte_change_pct",
            "ebit_per_fte_2024_eur",
            "ebit_per_fte_2025_eur",
            "ebit_per_fte_change_pct"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# 10. Save
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

analysis.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\nProductivity analysis saved to:\n{OUTPUT_FILE}"
)