import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10

# Load data
clf_df = pd.read_csv("feeder_classified_dataset.csv", parse_dates=["timestamp"])
disp_df = pd.read_csv("feeder_dispatch_results.csv", parse_dates=["timestamp"])

# -------------------------------------------------------------
# PLOT 1: Weather Dip vs. Equipment Fault Classification
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

# Scenario A: Regional Weather Dip (Day 6)
day6_f1 = clf_df[(clf_df["feeder_id"] == "Feeder_1") & (clf_df["timestamp"].dt.day == 6)]
ax1.plot(day6_f1["timestamp"].dt.hour, day6_f1["solar_irradiance"] / 10.0, label="Irradiance (scaled /10)", color="#f39c12", linestyle="--", linewidth=2)
ax1.plot(day6_f1["timestamp"].dt.hour, day6_f1["generation_kw"], label="Generation (kW)", color="#27ae60", linewidth=2.5)
ax1.axvspan(11, 14, color="#e67e22", alpha=0.25, label="Detected: Weather Dip")
ax1.set_title("Scenario A: Correlated Weather Dip (Feeder 1)", fontweight="bold")
ax1.set_xlabel("Hour of Day")
ax1.set_ylabel("Power / Irradiance Index")
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend(loc="upper left")

# Scenario B: Equipment Fault (Day 14, Feeder 3)
day14_f3 = clf_df[(clf_df["feeder_id"] == "Feeder_3") & (clf_df["timestamp"].dt.day == 14)]
ax2.plot(day14_f3["timestamp"].dt.hour, day14_f3["solar_irradiance"] / 10.0, label="Irradiance (scaled /10)", color="#f39c12", linestyle="--", linewidth=2)
ax2.plot(day14_f3["timestamp"].dt.hour, day14_f3["generation_kw"], label="Generation (kW)", color="#c0392b", linewidth=2.5)
ax2.axvspan(10, 15, color="#e74c3c", alpha=0.25, label="Detected: Equipment Fault")
ax2.set_title("Scenario B: Hardware Fault Under Clear Sky (Feeder 3)", fontweight="bold")
ax2.set_xlabel("Hour of Day")
ax2.grid(True, linestyle=":", alpha=0.6)
ax2.legend(loc="upper left")

plt.tight_layout()
fig.savefig("fig1_anomaly_classification.png", dpi=300)
print("Saved: fig1_anomaly_classification.png")

# -------------------------------------------------------------
# PLOT 2: BESS Dispatch & Load Protection Impact
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
day14_disp = disp_df[(disp_df["feeder_id"] == "Feeder_3") & (disp_df["timestamp"].dt.day == 14)]

ax.plot(day14_disp["timestamp"].dt.hour, day14_disp["critical_load_kw"], label="Critical Load (Essential)", color="#2c3e50", linewidth=2)
ax.plot(day14_disp["timestamp"].dt.hour, day14_disp["generation_kw"], label="PV Generation (Trip at 10h)", color="#e74c3c", linestyle="--", linewidth=2)
ax.fill_between(day14_disp["timestamp"].dt.hour, day14_disp["critical_load_kw"], day14_disp["generation_kw"], 
                where=(day14_disp["critical_load_kw"] > day14_disp["generation_kw"]), 
                color="#e74c3c", alpha=0.2, label="Baseline Critical Outage Window")

# Secondary axis for Battery State of Charge
ax_soc = ax.twinx()
ax_soc.plot(day14_disp["timestamp"].dt.hour, day14_disp["bess_soc_pct"], label="BESS State of Charge (%)", color="#2980b9", linewidth=2.5)
ax_soc.set_ylabel("Battery SoC (%)", color="#2980b9", fontweight="bold")
ax_soc.tick_params(axis='y', labelcolor="#2980b9")
ax_soc.set_ylim(0, 105)

ax.set_title("BESS Emergency Dispatch Preserving Critical Feeder Load", fontweight="bold")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Power Demand / Generation (kW)")
ax.grid(True, linestyle=":", alpha=0.5)

lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax_soc.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.tight_layout()
fig.savefig("fig2_dispatch_resilience.png", dpi=300)
print("Saved: fig2_dispatch_resilience.png")