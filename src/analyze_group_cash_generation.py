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
    / "dhl_group_financials_kpi.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dhl_group_cash_generation.csv"
)


# ---------------------------------------------------------
# 2. Load data
# ---------------------------------------------------------

try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Could not find:\n{INPUT_FILE}\n"
        "Run calculate_group_kpis.py first."
    )


# ---------------------------------------------------------
# 3. Calculate cash-flow KPIs
# ---------------------------------------------------------

df["ocf_margin_pct"] = (
    df["operating_cash_flow_eur_m"]
    / df["revenue_eur_m"]
    * 100
)

df["cash_conversion_pct"] = (
    df["operating_cash_flow_eur_m"]
    / df["ebit_eur_m"]
    * 100
)

df["fcf_margin_pct"] = (
    df["free_cash_flow_eur_m"]
    / df["revenue_eur_m"]
    * 100
)


# ---------------------------------------------------------
# 4. Round
# ---------------------------------------------------------

df["ocf_margin_pct"] = df["ocf_margin_pct"].round(2)
df["cash_conversion_pct"] = df["cash_conversion_pct"].round(2)
df["fcf_margin_pct"] = df["fcf_margin_pct"].round(2)


# ---------------------------------------------------------
# 5. Display
# ---------------------------------------------------------

print("\nDHL Group Cash Generation Analysis")
print("=" * 100)

print(
    df[
        [
            "year",
            "revenue_eur_m",
            "ebit_eur_m",
            "operating_cash_flow_eur_m",
            "free_cash_flow_eur_m",
            "ocf_margin_pct",
            "cash_conversion_pct",
            "fcf_margin_pct"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# 6. Save
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\nCash analysis saved to:\n{OUTPUT_FILE}"
)