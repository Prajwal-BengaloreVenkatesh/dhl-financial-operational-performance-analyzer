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
    / "dhl_investment_efficiency.csv"
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
# 4. Calculate investment KPIs
# ---------------------------------------------------------

# Acquired-asset capex intensity
df["acquired_capex_intensity_pct"] = (
    df["capex_assets_eur_m"]
    / df["external_revenue_eur_m"]
    * 100
)


# Total capex intensity
df["total_capex_intensity_pct"] = (
    df["total_capex_eur_m"]
    / df["external_revenue_eur_m"]
    * 100
)


# Asset intensity
df["asset_intensity_pct"] = (
    df["segment_assets_eur_m"]
    / df["external_revenue_eur_m"]
    * 100
)


# Total capex / D&A
df["capex_to_da_ratio"] = (
    df["total_capex_eur_m"]
    / df["depreciation_amortization_eur_m"]
)


# ---------------------------------------------------------
# 5. Round
# ---------------------------------------------------------

percentage_columns = [
    "acquired_capex_intensity_pct",
    "total_capex_intensity_pct",
    "asset_intensity_pct"
]

for column in percentage_columns:
    df[column] = df[column].round(2)

df["capex_to_da_ratio"] = (
    df["capex_to_da_ratio"].round(2)
)


# ---------------------------------------------------------
# 6. Select output columns
# ---------------------------------------------------------

result = df[
    [
        "year",
        "segment",
        "external_revenue_eur_m",
        "ebit_eur_m",
        "segment_assets_eur_m",
        "capex_assets_eur_m",
        "capex_rou_eur_m",
        "total_capex_eur_m",
        "depreciation_amortization_eur_m",
        "acquired_capex_intensity_pct",
        "total_capex_intensity_pct",
        "asset_intensity_pct",
        "capex_to_da_ratio"
    ]
].sort_values(
    ["segment", "year"]
)


# ---------------------------------------------------------
# 7. Display
# ---------------------------------------------------------

print("\nDHL Segment Investment & Capital Efficiency")
print("=" * 120)

print(
    result.to_string(index=False)
)


# ---------------------------------------------------------
# 8. Save
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

result.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\nInvestment analysis saved to:\n{OUTPUT_FILE}"
)