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
    / "dhl_segment_cash_generation.csv"
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
# 4. Calculate cash KPIs
# ---------------------------------------------------------

df["ocf_margin_pct"] = (
    df["operating_cash_flow_eur_m"]
    / df["external_revenue_eur_m"]
    * 100
)

df["cash_conversion_pct"] = (
    df["operating_cash_flow_eur_m"]
    / df["ebit_eur_m"]
    * 100
)


# ---------------------------------------------------------
# 5. Round
# ---------------------------------------------------------

df["ocf_margin_pct"] = df["ocf_margin_pct"].round(2)
df["cash_conversion_pct"] = df["cash_conversion_pct"].round(2)


# ---------------------------------------------------------
# 6. Select columns
# ---------------------------------------------------------

result = df[
    [
        "year",
        "segment",
        "external_revenue_eur_m",
        "ebit_eur_m",
        "operating_cash_flow_eur_m",
        "ocf_margin_pct",
        "cash_conversion_pct"
    ]
].sort_values(
    ["segment", "year"]
)


# ---------------------------------------------------------
# 7. Display
# ---------------------------------------------------------

print("\nDHL Segment Cash Generation Analysis")
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
    f"\nSegment cash analysis saved to:\n{OUTPUT_FILE}"
)