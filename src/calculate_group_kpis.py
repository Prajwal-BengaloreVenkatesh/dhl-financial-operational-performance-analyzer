from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# 1. Define file locations
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "dhl_group_financials.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "dhl_group_financials_kpi.csv"


# ---------------------------------------------------------
# 2. Load the raw data
# ---------------------------------------------------------

try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Could not find the input file:\n{INPUT_FILE}"
    )


# ---------------------------------------------------------
# 3. Basic validation
# ---------------------------------------------------------

required_columns = [
    "year",
    "revenue_eur_m",
    "ebit_eur_m",
    "capex_eur_m"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# Make sure data is sorted chronologically
df = df.sort_values("year").reset_index(drop=True)


# ---------------------------------------------------------
# 4. Calculate KPIs
# ---------------------------------------------------------

# Revenue Growth %
df["revenue_growth_pct"] = (
    df["revenue_eur_m"].pct_change() * 100
)

# EBIT Margin %
df["ebit_margin_pct"] = (
    df["ebit_eur_m"] /
    df["revenue_eur_m"] *
    100
)

# Capex Intensity %
df["capex_intensity_pct"] = (
    df["capex_eur_m"] /
    df["revenue_eur_m"] *
    100
)


# ---------------------------------------------------------
# 5. Round calculated KPIs
# ---------------------------------------------------------

df["revenue_growth_pct"] = df["revenue_growth_pct"].round(2)
df["ebit_margin_pct"] = df["ebit_margin_pct"].round(2)
df["capex_intensity_pct"] = df["capex_intensity_pct"].round(2)


# ---------------------------------------------------------
# 6. Save processed dataset
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)


# ---------------------------------------------------------
# 7. Display results
# ---------------------------------------------------------

print("\nDHL Group KPI Analysis")
print("=" * 60)

print(
    df[
        [
            "year",
            "revenue_eur_m",
            "revenue_growth_pct",
            "ebit_eur_m",
            "ebit_margin_pct",
            "capex_eur_m",
            "capex_intensity_pct"
        ]
    ].to_string(index=False)
)

print("\n")
print(f"Processed file saved to:\n{OUTPUT_FILE}")