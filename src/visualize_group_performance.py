from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# 1. Define project paths
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
    / "images"
    / "01_group_financial_performance.png"
)


# ---------------------------------------------------------
# 2. Load processed KPI data
# ---------------------------------------------------------

try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Could not find:\n{INPUT_FILE}\n"
        "Run calculate_group_kpis.py first."
    )


# ---------------------------------------------------------
# 3. Validate required columns
# ---------------------------------------------------------

required_columns = [
    "year",
    "revenue_eur_m",
    "ebit_margin_pct"
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
# 4. Create chart
# ---------------------------------------------------------

fig, ax1 = plt.subplots(figsize=(11, 6))

# Revenue bars
ax1.bar(
    df["year"].astype(str),
    df["revenue_eur_m"],
    alpha=0.7
)

ax1.set_xlabel("Year")
ax1.set_ylabel("Revenue (€ million)")
ax1.set_title(
    "DHL Group — Revenue and EBIT Margin Trend (2021–2025)"
)

# EBIT margin line
ax2 = ax1.twinx()

ax2.plot(
    df["year"].astype(str),
    df["ebit_margin_pct"],
    marker="o",
    linewidth=2
)

ax2.set_ylabel("EBIT Margin (%)")

# Add margin labels
for x, y in zip(
    df["year"].astype(str),
    df["ebit_margin_pct"]
):
    ax2.annotate(
        f"{y:.1f}%",
        (x, y),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center"
    )


# ---------------------------------------------------------
# 5. Improve readability
# ---------------------------------------------------------

ax1.grid(
    axis="y",
    linestyle="--",
    alpha=0.3
)

fig.tight_layout()


# ---------------------------------------------------------
# 6. Save chart
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print(
    f"\nChart saved to:\n{OUTPUT_FILE}"
)