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
    / "dhl_workforce_productivity_analysis.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "images"
    / "04_workforce_vs_ebit_productivity.png"
)


# ---------------------------------------------------------
# 2. Load data
# ---------------------------------------------------------

try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Could not find:\n{INPUT_FILE}\n"
        "Run analyze_workforce_productivity.py first."
    )


# ---------------------------------------------------------
# 3. Validate columns
# ---------------------------------------------------------

required_columns = [
    "segment",
    "fte_growth_pct",
    "ebit_per_fte_change_pct"
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
# 4. Create chart
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 7))

ax.scatter(
    df["fte_growth_pct"],
    df["ebit_per_fte_change_pct"],
    s=100
)


# Add division labels
for _, row in df.iterrows():
    ax.annotate(
        row["segment"],
        (
            row["fte_growth_pct"],
            row["ebit_per_fte_change_pct"]
        ),
        xytext=(7, 7),
        textcoords="offset points"
    )


# Zero reference lines
ax.axhline(
    0,
    linestyle="--",
    alpha=0.5
)

ax.axvline(
    0,
    linestyle="--",
    alpha=0.5
)


# Labels
ax.set_xlabel("FTE Growth (%)")
ax.set_ylabel("EBIT per FTE Change (%)")

ax.set_title(
    "DHL Group — Workforce Change vs EBIT per FTE Change (2024–2025)"
)

ax.grid(
    alpha=0.2
)

fig.tight_layout()


# ---------------------------------------------------------
# 5. Save chart
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