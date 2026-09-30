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
    / "dhl_segment_master.csv"
)


# ---------------------------------------------------------
# 2. Load dataset
# ---------------------------------------------------------

try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Could not find:\n{INPUT_FILE}"
    )


print("\nDHL Master Dataset — Data Quality Check")
print("=" * 70)


# ---------------------------------------------------------
# 3. Basic structure
# ---------------------------------------------------------

print("\n1. Dataset structure")
print("-" * 70)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ---------------------------------------------------------
# 4. Check duplicate Year + Segment combinations
# ---------------------------------------------------------

print("\n2. Duplicate Year + Segment check")
print("-" * 70)

duplicates = df[
    df.duplicated(
        subset=["year", "segment"],
        keep=False
    )
]

if duplicates.empty:
    print("PASS — No duplicate Year + Segment combinations.")
else:
    print("FAIL — Duplicate combinations found:")
    print(
        duplicates[
            ["year", "segment"]
        ].to_string(index=False)
    )


# ---------------------------------------------------------
# 5. Check required fields
# ---------------------------------------------------------

required_columns = [
    "year",
    "segment",
    "external_revenue_eur_m",
    "total_revenue_eur_m",
    "ebit_eur_m",
    "average_fte",
    "operating_cash_flow_eur_m",
    "total_capex_eur_m",
    "segment_assets_eur_m",
    "source_id"
]

print("\n3. Required-column check")
print("-" * 70)

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if not missing_columns:
    print("PASS — All required columns are present.")
else:
    print("FAIL — Missing columns:")
    print(missing_columns)


# ---------------------------------------------------------
# 6. Check critical missing values
# ---------------------------------------------------------

critical_columns = [
    "year",
    "segment",
    "external_revenue_eur_m",
    "total_revenue_eur_m",
    "ebit_eur_m",
    "average_fte",
    "operating_cash_flow_eur_m",
    "total_capex_eur_m",
    "segment_assets_eur_m"
]

print("\n4. Critical missing-value check")
print("-" * 70)

missing_values = df[critical_columns].isna().sum()

if missing_values.sum() == 0:
    print("PASS — No critical missing values.")
else:
    print("FAIL — Missing values found:")
    print(
        missing_values[
            missing_values > 0
        ]
    )


# ---------------------------------------------------------
# 7. Check business logic
# ---------------------------------------------------------

print("\n5. Business-logic checks")
print("-" * 70)

problems = []


# External revenue should not exceed total revenue
invalid_revenue = df[
    df["external_revenue_eur_m"]
    > df["total_revenue_eur_m"]
]

if not invalid_revenue.empty:
    problems.append(
        "External revenue exceeds total revenue."
    )


# FTE should be positive
invalid_fte = df[
    df["average_fte"] <= 0
]

if not invalid_fte.empty:
    problems.append(
        "Average FTE is zero or negative."
    )


# Capex should not be negative
invalid_capex = df[
    df["total_capex_eur_m"] < 0
]

if not invalid_capex.empty:
    problems.append(
        "Negative total capex found."
    )


# Assets should not be negative
invalid_assets = df[
    df["segment_assets_eur_m"] < 0
]

if not invalid_assets.empty:
    problems.append(
        "Negative segment assets found."
    )


if not problems:
    print("PASS — Business-logic checks passed.")
else:
    print("FAIL:")
    for problem in problems:
        print(f"- {problem}")


# ---------------------------------------------------------
# 8. Check expected segments
# ---------------------------------------------------------

print("\n6. Segment check")
print("-" * 70)

expected_segments = {
    "Express",
    "Global Forwarding Freight",
    "Supply Chain",
    "eCommerce",
    "Post & Parcel Germany"
}

actual_segments = set(
    df["segment"].unique()
)

if actual_segments == expected_segments:
    print("PASS — All five operating divisions are present.")
else:
    print("CHECK — Segment list differs.")
    print("Expected:", expected_segments)
    print("Actual:", actual_segments)


# ---------------------------------------------------------
# 9. Check years
# ---------------------------------------------------------

print("\n7. Year check")
print("-" * 70)

expected_years = {2024, 2025}

actual_years = set(
    df["year"].unique()
)

if actual_years == expected_years:
    print("PASS — Dataset contains 2024 and 2025.")
else:
    print("CHECK — Unexpected years found.")
    print("Expected:", expected_years)
    print("Actual:", actual_years)


# ---------------------------------------------------------
# 10. Display source coverage
# ---------------------------------------------------------

print("\n8. Source coverage")
print("-" * 70)

print(
    df["source_id"]
    .value_counts()
    .to_string()
)


# ---------------------------------------------------------
# 11. Final status
# ---------------------------------------------------------

print("\nFinal result")
print("=" * 70)

if (
    duplicates.empty
    and not missing_columns
    and missing_values.sum() == 0
    and not problems
    and actual_segments == expected_segments
    and actual_years == expected_years
):
    print("✅ DATASET VALIDATION PASSED")
else:
    print("⚠️ DATASET VALIDATION NEEDS REVIEW")