from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# 1. Define project paths
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
    / "dhl_segment_cost_analysis.csv"
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
# 3. Keep operating divisions only
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
# 4. Select 2024 and 2025
# ---------------------------------------------------------

df = df[
    df["year"].isin([2024, 2025])
].copy()


# ---------------------------------------------------------
# 5. Select important cost metrics
# ---------------------------------------------------------

result = df[
    [
        "year",
        "segment",
        "total_revenue_eur_m",
        "material_expense_eur_m",
        "staff_costs_eur_m",
        "depreciation_amortization_eur_m",
        "ebit_eur_m",
        "material_cost_pct",
        "staff_cost_pct",
        "d_and_a_pct",
        "ebit_margin_pct"
    ]
].copy()


# ---------------------------------------------------------
# 6. Sort
# ---------------------------------------------------------

result = result.sort_values(
    ["segment", "year"]
)


# ---------------------------------------------------------
# 7. Display
# ---------------------------------------------------------

print("\nDHL Segment Cost Structure")
print("=" * 110)

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
    f"\nCost analysis saved to:\n{OUTPUT_FILE}"
)