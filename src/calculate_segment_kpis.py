from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# 1. Define project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "dhl_segment_financials.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dhl_segment_financials_kpi.csv"
)


# ---------------------------------------------------------
# 2. Load raw segment data
# ---------------------------------------------------------

try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Could not find the input file:\n{INPUT_FILE}"
    )


# ---------------------------------------------------------
# 3. Validate required columns
# ---------------------------------------------------------

required_columns = [
    "year",
    "segment",
    "external_revenue_eur_m",
    "total_revenue_eur_m",
    "ebit_eur_m",
    "staff_costs_eur_m",
    "total_capex_eur_m",
    "operating_cash_flow_eur_m",
    "average_fte"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ---------------------------------------------------------
# 4. Sort data
# ---------------------------------------------------------

df = df.sort_values(
    ["segment", "year"]
).reset_index(drop=True)


# ---------------------------------------------------------
# 5. Calculate year-over-year growth
# ---------------------------------------------------------

df["external_revenue_growth_pct"] = (
    df.groupby("segment")["external_revenue_eur_m"]
    .pct_change() * 100
)


# ---------------------------------------------------------
# 6. Calculate profitability KPIs
# ---------------------------------------------------------

# Segment EBIT Margin
df["ebit_margin_pct"] = (
    df["ebit_eur_m"] /
    df["total_revenue_eur_m"] *
    100
)


# Staff Cost as % of External Revenue
df["staff_cost_pct"] = (
    df["staff_costs_eur_m"] /
    df["total_revenue_eur_m"] *
    100
)

df["material_cost_pct"] = (
    df["material_expense_eur_m"] /
    df["total_revenue_eur_m"] *
    100
)

df["d_and_a_pct"] = (
    df["depreciation_amortization_eur_m"] /
    df["total_revenue_eur_m"] *
    100
)


# ---------------------------------------------------------
# 7. Calculate employee productivity
# ---------------------------------------------------------

# Revenue generated per average FTE
df["external_revenue_per_fte_eur"] = (
    df["external_revenue_eur_m"] * 1_000_000
    / df["average_fte"]
)


# EBIT generated per average FTE
df["ebit_per_fte_eur"] = (
    df["ebit_eur_m"] * 1_000_000
    / df["average_fte"]
)


# ---------------------------------------------------------
# 8. Calculate investment KPIs
# ---------------------------------------------------------

# Capex relative to external revenue
df["capex_intensity_pct"] = (
    df["capex_assets_eur_m"] /
    df["external_revenue_eur_m"] *
    100
)


# Operating Cash Flow Margin
df["ocf_margin_pct"] = (
    df["operating_cash_flow_eur_m"] /
    df["external_revenue_eur_m"] *
    100
)


# ---------------------------------------------------------
# 9. Round KPI values
# ---------------------------------------------------------

percentage_columns = [
    "external_revenue_growth_pct",
    "ebit_margin_pct",
    "staff_cost_pct",
    "capex_intensity_pct",
    "ocf_margin_pct",
    "material_cost_pct",
    "d_and_a_pct"
]

for column in percentage_columns:
    df[column] = df[column].round(2)


df["external_revenue_per_fte_eur"] = (
    df["external_revenue_per_fte_eur"].round(0)
)

df["ebit_per_fte_eur"] = (
    df["ebit_per_fte_eur"].round(0)
)


# ---------------------------------------------------------
# 10. Save processed data
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
# 11. Display important KPIs
# ---------------------------------------------------------

print("\nDHL Segment KPI Analysis")
print("=" * 100)

display_columns = [
    "year",
    "segment",
    "external_revenue_eur_m",
    "external_revenue_growth_pct",
    "ebit_eur_m",
    "ebit_margin_pct",
    "staff_cost_pct",
    "external_revenue_per_fte_eur",
    "ebit_per_fte_eur",
    "total_capex_eur_m",
    "capex_intensity_pct",
    "operating_cash_flow_eur_m"
]

print(
    df[display_columns]
    .to_string(index=False)
)

print("\n")
print(
    f"Processed file saved to:\n{OUTPUT_FILE}"
)