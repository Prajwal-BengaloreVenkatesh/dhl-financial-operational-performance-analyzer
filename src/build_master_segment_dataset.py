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
    / "dhl_segment_master.csv"
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
# 4. Sort data
# ---------------------------------------------------------

df = df.sort_values(
    ["segment", "year"]
).reset_index(drop=True)


# ---------------------------------------------------------
# 5. Add metadata
# ---------------------------------------------------------

df["data_type"] = "reported"
df["entity_level"] = "operating_segment"


# ---------------------------------------------------------
# 6. Workforce growth
# ---------------------------------------------------------

df["fte_growth_pct"] = (
    df.groupby("segment")["average_fte"]
    .pct_change() * 100
)


# ---------------------------------------------------------
# 7. EBIT changes
# ---------------------------------------------------------

df["ebit_change_eur_m"] = (
    df.groupby("segment")["ebit_eur_m"]
    .diff()
)

df["ebit_growth_pct"] = (
    df.groupby("segment")["ebit_eur_m"]
    .pct_change() * 100
)


# ---------------------------------------------------------
# 8. EBIT margin change
# ---------------------------------------------------------

df["ebit_margin_change_pp"] = (
    df.groupby("segment")["ebit_margin_pct"]
    .diff()
)


# ---------------------------------------------------------
# 9. Cost structure changes
# ---------------------------------------------------------

df["material_cost_change_pp"] = (
    df.groupby("segment")["material_cost_pct"]
    .diff()
)

df["staff_cost_change_pp"] = (
    df.groupby("segment")["staff_cost_pct"]
    .diff()
)


# ---------------------------------------------------------
# 10. Revenue / FTE growth
# ---------------------------------------------------------

df["revenue_per_fte_change_pct"] = (
    df.groupby("segment")["external_revenue_per_fte_eur"]
    .pct_change() * 100
)


# ---------------------------------------------------------
# 11. EBIT / FTE growth
# ---------------------------------------------------------

df["ebit_per_fte_change_pct"] = (
    df.groupby("segment")["ebit_per_fte_eur"]
    .pct_change() * 100
)


# ---------------------------------------------------------
# 12. Capex change
# ---------------------------------------------------------

df["capex_change_eur_m"] = (
    df.groupby("segment")["total_capex_eur_m"]
    .diff()
)

df["capex_growth_pct"] = (
    df.groupby("segment")["total_capex_eur_m"]
    .pct_change() * 100
)


# ---------------------------------------------------------
# 13. Asset change
# ---------------------------------------------------------

df["asset_change_eur_m"] = (
    df.groupby("segment")["segment_assets_eur_m"]
    .diff()
)

df["asset_growth_pct"] = (
    df.groupby("segment")["segment_assets_eur_m"]
    .pct_change() * 100
)


# ---------------------------------------------------------
# 14. Round calculated metrics
# ---------------------------------------------------------

percentage_columns = [
    "revenue_growth_pct",
    "ebit_margin_pct",
    "staff_cost_pct",
    "capex_intensity_pct",
    "ocf_margin_pct",
    "cash_conversion_pct",
    "asset_intensity_pct",
    "acquired_capex_intensity_pct",
    "total_capex_intensity_pct",
    "capex_to_da_ratio",
    "fte_growth_pct",
    "ebit_growth_pct",
    "ebit_margin_change_pp",
    "material_cost_change_pp",
    "staff_cost_change_pp",
    "revenue_per_fte_change_pct",
    "ebit_per_fte_change_pct",
    "capex_growth_pct",
    "asset_growth_pct"
]

for column in percentage_columns:
    if column in df.columns:
        df[column] = df[column].round(2)


# ---------------------------------------------------------
# 15. Round monetary changes
# ---------------------------------------------------------

for column in [
    "ebit_change_eur_m",
    "capex_change_eur_m",
    "asset_change_eur_m"
]:
    df[column] = df[column].round(2)


# ---------------------------------------------------------
# 16. Define final column order
# ---------------------------------------------------------

final_columns = [
    "year",
    "segment",
    "data_type",
    "entity_level",

    # Revenue
    "external_revenue_eur_m",
    "total_revenue_eur_m",
    "external_revenue_growth_pct",

    # Profitability
    "ebit_eur_m",
    "ebit_growth_pct",
    "ebit_change_eur_m",
    "ebit_margin_pct",
    "ebit_margin_change_pp",

    # Costs
    "material_expense_eur_m",
    "material_cost_pct",
    "material_cost_change_pp",
    "staff_costs_eur_m",
    "staff_cost_pct",
    "staff_cost_change_pp",
    "depreciation_amortization_eur_m",
    "d_and_a_pct",

    # Workforce
    "average_fte",
    "fte_growth_pct",
    "external_revenue_per_fte_eur",
    "revenue_per_fte_change_pct",
    "ebit_per_fte_eur",
    "ebit_per_fte_change_pct",

    # Cash
    "operating_cash_flow_eur_m",
    "ocf_margin_pct",
    "cash_conversion_pct",

    # Investment
    "segment_assets_eur_m",
    "asset_intensity_pct",
    "asset_change_eur_m",
    "asset_growth_pct",
    "capex_assets_eur_m",
    "capex_rou_eur_m",
    "total_capex_eur_m",
    "capex_growth_pct",
    "capex_change_eur_m",
    "acquired_capex_intensity_pct",
    "total_capex_intensity_pct",
    "capex_to_da_ratio",

    # Source
    "source_id"
]


# Keep only columns that exist
final_columns = [
    column
    for column in final_columns
    if column in df.columns
]

df = df[final_columns]


# ---------------------------------------------------------
# 17. Save
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# 18. Display
# ---------------------------------------------------------

print("\nDHL Master Segment Dataset")
print("=" * 120)

print(
    df[
        [
            "year",
            "segment",
            "external_revenue_eur_m",
            "external_revenue_growth_pct",
            "ebit_eur_m",
            "ebit_margin_pct",
            "average_fte",
            "fte_growth_pct",
            "operating_cash_flow_eur_m",
            "total_capex_eur_m"
        ]
    ].to_string(index=False)
)

print("\n")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to:\n{OUTPUT_FILE}")