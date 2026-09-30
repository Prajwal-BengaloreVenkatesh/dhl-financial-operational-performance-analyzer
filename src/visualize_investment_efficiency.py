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
    / "dhl_investment_efficiency.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "images"
    / "06_investment_vs_ebit.png"
)


# ---------------------------------------------------------
# 2. Load data
# ---------------------------------------------------------

try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Could not find:\n{INPUT_FILE}\n"
        "Run analyze_investment_efficiency.py first."
    )


# ---------------------------------------------------------
# 3. Validate
# ---------------------------------------------------------

required_columns = [
    "year",
    "segment",
    "total_capex_eur_m",
    "ebit_eur_m"
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
# 4. Keep operating divisions
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
# 5. Create chart
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 7))

for year in [2024, 2025]:

    year_data = df[df["year"] == year]

    ax.scatter(
        year_data["total_capex_eur_m"],
        year_data["ebit_eur_m"],
        s=100,
        label=str(year)
    )

    for _, row in year_data.iterrows():
        ax.annotate(
            row["segment"],
            (
                row["total_capex_eur_m"],
                row["ebit_eur_m"]
            ),
            xytext=(7, 7),
            textcoords="offset points"
        )


# ---------------------------------------------------------
# 6. Labels
# ---------------------------------------------------------

ax.set_xlabel("Total Capex (€ million)")
ax.set_ylabel("EBIT (€ million)")

ax.set_title(
    "DHL Group — Total Capex vs EBIT by Division"
)

ax.legend()

ax.grid(
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