"""README charts: demand vs capacity trend, and simulation results."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
DATA, DOCS = ROOT / "data" / "processed", ROOT / "docs"
DOCS.mkdir(exist_ok=True)

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e6e5e0"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "text.color": INK, "axes.edgecolor": GRID,
    "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
    "axes.spines.right": False, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "axes.axisbelow": True,
})

# 1. Demand vs supply, indexed to Jan 2025 = 100
p = pd.read_csv(DATA / "london_pharmacy_month.csv", parse_dates=["month"])
m = p.groupby("month").agg(items=("items", "sum"), pharmacy_first=("pharmacy_first", "sum"),
                           pharmacies=("CONTRACTOR_CODE", "nunique"))
m["items_3m"] = m["items"].rolling(3).mean()
m["pf_3m"] = m["pharmacy_first"].rolling(3).mean()
m = m.dropna()
idx = lambda s: 100 * s / s.iloc[0]
fig, ax = plt.subplots(figsize=(9, 4.2))
series = [("Pharmacy First consultations", idx(m["pf_3m"]), ORANGE),
          ("Prescription items", idx(m["items_3m"]), BLUE),
          ("Pharmacies open", idx(m["pharmacies"]), AQUA)]
for label, s, c in series:
    ax.plot(m.index, s, color=c, lw=2, label=label)
    ax.annotate(f"{label}  {s.iloc[-1]:.0f}", (m.index[-1], s.iloc[-1]), xytext=(6, 0),
                textcoords="offset points", va="center", color=INK2, fontsize=9)
ax.axhline(100, color=GRID, lw=1)
ax.set_xlim(m.index[0], m.index[-1] + pd.Timedelta(days=150))
ax.set_ylabel("Index (Mar 2025 = 100)")
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.grid(axis="y", color=GRID, lw=0.8)
ax.legend(loc="upper left", frameon=False)
ax.set_title("London: clinical demand is growing faster than prescriptions, with no new pharmacies\n"
             "3-month rolling average, indexed", loc="left", fontsize=11.5, color=INK)
fig.tight_layout()
fig.savefig(DOCS / "demand_vs_capacity.png", dpi=160)
plt.close(fig)

# 2. Simulation: waits by scenario for the busy pharmacy
r = pd.read_csv(DATA / "simulation_results.csv")
busy = r[r.demand_level.str.startswith("Busy")].iloc[::-1]
fig, ax = plt.subplots(figsize=(9, 4))
y = range(len(busy))
h = 0.36
ax.barh([i + h / 2 + 0.01 for i in y], busy["avg_wait_min"], height=h, color=BLUE, label="Average wait")
ax.barh([i - h / 2 - 0.01 for i in y], busy["p95_wait_min"], height=h, color=ORANGE, label="95th-percentile wait")
for i, (a, b) in enumerate(zip(busy["avg_wait_min"], busy["p95_wait_min"])):
    ax.text(a + 0.6, i + h / 2, f"{a:.0f} min", va="center", fontsize=9, color=INK2)
    ax.text(b + 0.6, i - h / 2, f"{b:.0f} min", va="center", fontsize=9, color=INK2)
ax.set_yticks(list(y), busy["scenario"], color=INK2)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}"))
ax.set_xlabel("Minutes waiting for a prescription")
ax.grid(axis="x", color=GRID, lw=0.8)
ax.legend(loc="lower right", frameon=False)
ax.set_title("Busy pharmacy: A + B together cuts the longest waits from 48 to 20 min",
             loc="left", fontsize=11.5, color=INK)
fig.tight_layout()
fig.savefig(DOCS / "simulation_waits.png", dpi=160)
plt.close(fig)
print("charts saved")
