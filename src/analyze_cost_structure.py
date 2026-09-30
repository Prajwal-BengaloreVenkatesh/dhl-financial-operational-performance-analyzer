from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


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
    / "dhl_cost_structure_change.csv"
)

CHART_FILE = (
    PROJECT_ROOT
    / "images"
    / "03_segment_cost_structure_change.png"
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
# 5. Create 2024 / 2025 comparison
# ---------------------------------------------------------

pivot = df.pivot(
    index="segment",
    columns="year",
    values=[
        "material_cost_pct",
        "staff_cost_pct",
        "ebit_margin_pct"
    ]
)


# Flatten column names
pivot.columns = [
    f"{metric}_{year}"
    for metric, year in pivot.columns
]


pivot = pivot.reset_index()


# ---------------------------------------------------------
# 6. Calculate changes in percentage points
# ---------------------------------------------------------

pivot["material_cost_change_pp"] = (
    pivot["material_cost_pct_2025"]
    - pivot["material_cost_pct_2024"]
)

pivot["staff_cost_change_pp"] = (
    pivot["staff_cost_pct_2025"]
    - pivot["staff_cost_pct_2024"]
)

pivot["ebit_margin_change_pp"] = (
    pivot["ebit_margin_pct_2025"]
    - pivot["ebit_margin_pct_2024"]
)


# ---------------------------------------------------------
# 7. Round
# ---------------------------------------------------------

change_columns = [
    "material_cost_change_pp",
    "staff_cost_change_pp",
    "ebit_margin_change_pp"
]

for column in change_columns:
    pivot[column] = pivot[column].round(2)


# ---------------------------------------------------------
# 8. Display key results
# ---------------------------------------------------------

print("\nDHL Segment Cost Structure Changes")
print("=" * 100)

print(
    pivot[
        [
            "segment",
            "material_cost_pct_2024",
            "material_cost_pct_2025",
            "material_cost_change_pp",
            "staff_cost_pct_2024",
            "staff_cost_pct_2025",
            "staff_cost_change_pp",
            "ebit_margin_change_pp"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# 9. Save analysis
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

pivot.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# 10. Create chart
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 7))

x = range(len(pivot))

ax.bar(
    [i - 0.2 for i in x],
    pivot["material_cost_change_pp"],
    width=0.2,
    label="Material Cost % Change"
)

ax.bar(
    x,
    pivot["staff_cost_change_pp"],
    width=0.2,
    label="Staff Cost % Change"
)

ax.bar(
    [i + 0.2 for i in x],
    pivot["ebit_margin_change_pp"],
    width=0.2,
    label="EBIT Margin Change"
)


# Zero reference line
ax.axhline(
    0,
    linestyle="--",
    alpha=0.5
)


ax.set_xticks(list(x))
ax.set_xticklabels(
    pivot["segment"],
    rotation=20,
    ha="right"
)

ax.set_ylabel("Change (percentage points)")

ax.set_title(
    "DHL Segment Cost Structure and EBIT Margin Changes (2024–2025)"
)

ax.legend()

ax.grid(
    axis="y",
    alpha=0.2
)

fig.tight_layout()


# ---------------------------------------------------------
# 11. Save chart
# ---------------------------------------------------------

CHART_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

plt.savefig(
    CHART_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print(
    f"\nAnalysis saved to:\n{OUTPUT_FILE}"
)

print(
    f"Chart saved to:\n{CHART_FILE}"
)