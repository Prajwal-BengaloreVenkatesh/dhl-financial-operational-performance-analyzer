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
    / "dhl_segment_financials_kpi.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dhl_segment_performance_2024_2025.csv"
)

CHART_FILE = (
    PROJECT_ROOT
    / "images"
    / "02_segment_revenue_vs_ebit_growth.png"
)


# ---------------------------------------------------------
# 2. Load processed data
# ---------------------------------------------------------

try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Could not find:\n{INPUT_FILE}\n"
        "Run calculate_segment_kpis.py first."
    )


# ---------------------------------------------------------
# 3. Keep only operating divisions
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
# 4. Separate 2024 and 2025
# ---------------------------------------------------------

df_2024 = df[df["year"] == 2024].copy()
df_2025 = df[df["year"] == 2025].copy()


df_2024 = df_2024.set_index("segment")
df_2025 = df_2025.set_index("segment")


# ---------------------------------------------------------
# 5. Build comparison table
# ---------------------------------------------------------

analysis = pd.DataFrame(index=operating_divisions)

analysis["revenue_2024_eur_m"] = (
    df_2024["external_revenue_eur_m"]
)

analysis["revenue_2025_eur_m"] = (
    df_2025["external_revenue_eur_m"]
)

analysis["revenue_change_eur_m"] = (
    analysis["revenue_2025_eur_m"]
    - analysis["revenue_2024_eur_m"]
)

analysis["revenue_growth_pct"] = (
    analysis["revenue_change_eur_m"]
    / analysis["revenue_2024_eur_m"]
    * 100
)


analysis["ebit_2024_eur_m"] = (
    df_2024["ebit_eur_m"]
)

analysis["ebit_2025_eur_m"] = (
    df_2025["ebit_eur_m"]
)

analysis["ebit_change_eur_m"] = (
    analysis["ebit_2025_eur_m"]
    - analysis["ebit_2024_eur_m"]
)

analysis["ebit_growth_pct"] = (
    analysis["ebit_change_eur_m"]
    / analysis["ebit_2024_eur_m"]
    * 100
)


# ---------------------------------------------------------
# 6. Calculate EBIT margin change
# ---------------------------------------------------------

analysis["ebit_margin_2024_pct"] = (
    df_2024["ebit_margin_pct"]
)

analysis["ebit_margin_2025_pct"] = (
    df_2025["ebit_margin_pct"]
)

analysis["ebit_margin_change_pp"] = (
    analysis["ebit_margin_2025_pct"]
    - analysis["ebit_margin_2024_pct"]
)


# ---------------------------------------------------------
# 7. Round values
# ---------------------------------------------------------

percentage_columns = [
    "revenue_growth_pct",
    "ebit_growth_pct",
    "ebit_margin_2024_pct",
    "ebit_margin_2025_pct",
    "ebit_margin_change_pp"
]

for column in percentage_columns:
    analysis[column] = analysis[column].round(2)

analysis = analysis.reset_index()

analysis = analysis.rename(
    columns={"index": "segment"}
)


# ---------------------------------------------------------
# 8. Save comparison table
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

analysis.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# 9. Display results
# ---------------------------------------------------------

print("\nDHL Segment Performance: 2024 vs 2025")
print("=" * 110)

print(
    analysis[
        [
            "segment",
            "revenue_change_eur_m",
            "revenue_growth_pct",
            "ebit_change_eur_m",
            "ebit_growth_pct",
            "ebit_margin_change_pp"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# 10. Create Revenue Growth vs EBIT Growth chart
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 7))

ax.scatter(
    analysis["revenue_growth_pct"],
    analysis["ebit_growth_pct"],
    s=100
)


# Add division names
for _, row in analysis.iterrows():
    ax.annotate(
        row["segment"],
        (
            row["revenue_growth_pct"],
            row["ebit_growth_pct"]
        ),
        xytext=(7, 7),
        textcoords="offset points"
    )


# Reference lines
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


ax.set_xlabel("External Revenue Growth (%)")
ax.set_ylabel("EBIT Growth (%)")

ax.set_title(
    "DHL Group — Segment Revenue Growth vs EBIT Growth (2024–2025)"
)

ax.grid(
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
    f"\nComparison table saved to:\n{OUTPUT_FILE}"
)

print(
    f"Chart saved to:\n{CHART_FILE}"
)