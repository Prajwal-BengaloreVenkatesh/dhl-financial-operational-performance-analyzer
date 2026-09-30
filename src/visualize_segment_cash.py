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
    / "dhl_segment_cash_generation.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "images"
    / "05_segment_cash_generation.png"
)


# ---------------------------------------------------------
# 2. Load data
# ---------------------------------------------------------

try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Could not find:\n{INPUT_FILE}\n"
        "Run analyze_segment_cash.py first."
    )


# ---------------------------------------------------------
# 3. Keep required columns
# ---------------------------------------------------------

required_columns = [
    "year",
    "segment",
    "ocf_margin_pct",
    "cash_conversion_pct"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ---------------------------------------------------------
# 4. Reshape data
# ---------------------------------------------------------

margin_pivot = df.pivot(
    index="segment",
    columns="year",
    values="ocf_margin_pct"
)

conversion_pivot = df.pivot(
    index="segment",
    columns="year",
    values="cash_conversion_pct"
)


# ---------------------------------------------------------
# 5. Create Operating Cash Flow Margin chart
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 7))

x = range(len(margin_pivot.index))
width = 0.35

ax.bar(
    [i - width / 2 for i in x],
    margin_pivot[2024],
    width=width,
    label="2024"
)

ax.bar(
    [i + width / 2 for i in x],
    margin_pivot[2025],
    width=width,
    label="2025"
)


# ---------------------------------------------------------
# 6. Add labels
# ---------------------------------------------------------

ax.set_xticks(list(x))
ax.set_xticklabels(
    margin_pivot.index,
    rotation=20,
    ha="right"
)

ax.set_ylabel("Operating Cash Flow Margin (%)")

ax.set_title(
    "DHL Group — Operating Cash Flow Margin by Division"
)

ax.legend()

ax.grid(
    axis="y",
    alpha=0.2
)

fig.tight_layout()


# ---------------------------------------------------------
# 7. Save
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