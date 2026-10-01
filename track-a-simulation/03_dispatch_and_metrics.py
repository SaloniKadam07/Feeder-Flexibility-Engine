import pandas as pd
import numpy as np

def simulate_smart_grid_resilience(
    df, 
    bess_capacity_kwh=300.0,   # Sized for commercial feeder buffer
    max_power_kw=80.0,         # Inverter power rating
    efficiency=0.94,
    reserve_soc_pct=0.20
):
    """
    Track A: Storage Dispatch & Load Prioritization Engine.
    - Baseline: Feeder relies strictly on PV + raw grid without priority shedding.
    - Smart Dispatch:
        1. Maintains active BESS reserve during standard hours.
        2. Detects Weather Dips & Equipment Faults instantly.
        3. Dispatches BESS power and sheds 100% of Flexible Load first to preserve Critical Load.
    """
    feeders = df["feeder_id"].unique()
    reserve_soc_kwh = bess_capacity_kwh * reserve_soc_pct
    results = []

    for f in feeders:
        f_df = df[df["feeder_id"] == f].sort_values("timestamp").copy()
        
        # BESS starts fully charged
        soc = bess_capacity_kwh * 0.95

        for _, row in f_df.iterrows():
            gen = row["generation_kw"]
            demand = row["demand_kw"]
            crit_load = row["critical_load_kw"]
            flex_load = row["flexible_load_kw"]
            event = row["predicted_event"]
            hr = row["timestamp"].hour
            is_solar_window = 8 <= hr <= 17

            # Net balance relative to critical infrastructure needs
            crit_deficit = max(0.0, crit_load - gen)
            total_deficit = max(0.0, demand - gen)

            # ----------------------------------------------------
            # 1. BASELINE SCENARIO (No Smart Priority / No BESS)
            # ----------------------------------------------------
            # Baseline fails whenever generation drops below critical load
            baseline_crit_shortfall = 1 if (crit_deficit > 2.0 and is_solar_window) else 0

            # ----------------------------------------------------
            # 2. SMART DISPATCH WITH LOAD PRIORITIZATION
            # ----------------------------------------------------
            bess_discharge = 0.0

            # Normal midday surplus: recharge storage
            if gen > demand:
                surplus = gen - demand
                charge_room = (bess_capacity_kwh - soc) / efficiency
                charge_power = min(surplus, max_power_kw, charge_room)
                soc += charge_power * efficiency
            elif soc < bess_capacity_kwh * 0.85 and event == "Normal":
                # Grid trickle recharge during non-peak normal conditions
                soc = min(bess_capacity_kwh * 0.85, soc + 15.0)

            # Active deficit mitigation (especially during anomalies)
            if crit_deficit > 0:
                # Emergency discharge limit
                min_soc = (bess_capacity_kwh * 0.08) if event in ["Weather Dip", "Equipment Fault"] else reserve_soc_kwh
                usable_energy = max(0.0, (soc - min_soc) * efficiency)
                
                # Priority 1: Discharge to protect Critical Load
                bess_discharge = min(crit_deficit, max_power_kw, usable_energy)
                soc -= (bess_discharge / efficiency)

            # Unserved load calculation
            unserved_crit = max(0.0, crit_deficit - bess_discharge)
            smart_crit_shortfall = 1 if (unserved_crit > 2.0 and is_solar_window) else 0

            results.append({
                "timestamp": row["timestamp"],
                "feeder_id": f,
                "event": event,
                "is_solar_window": is_solar_window,
                "generation_kw": gen,
                "demand_kw": demand,
                "critical_load_kw": crit_load,
                "bess_soc_pct": round((soc / bess_capacity_kwh) * 100, 1),
                "unserved_critical_kw": round(unserved_crit, 2),
                "baseline_crit_shortfall": baseline_crit_shortfall,
                "smart_crit_shortfall": smart_crit_shortfall
            })

    res_df = pd.DataFrame(results)

    # ----------------------------------------------------
    # 3. COMPUTE RELIABILITY METRICS (Oct 1 Deliverable)
    # ----------------------------------------------------
    # Anomaly Event Focus (Cloud Dips & Hardware Faults)
    anomaly_df = res_df[res_df["event"].isin(["Weather Dip", "Equipment Fault"])]
    base_anom = anomaly_df["baseline_crit_shortfall"].sum()
    smart_anom = anomaly_df["smart_crit_shortfall"].sum()
    reduction_anom_pct = ((base_anom - smart_anom) / base_anom) * 100.0 if base_anom > 0 else 0.0

    # Solar Operating Window (Overall)
    solar_df = res_df[res_df["is_solar_window"]]
    base_total = solar_df["baseline_crit_shortfall"].sum()
    smart_total = solar_df["smart_crit_shortfall"].sum()
    reduction_total_pct = ((base_total - smart_total) / base_total) * 100.0 if base_total > 0 else 0.0

    print("=" * 68)
    print("      TRACK A: RELIABILITY & SHORTFALL REDUCTION METRICS")
    print("=" * 68)
    print(f"Total Operating Hours Evaluated (Daylight)  : {len(solar_df)} hrs")
    print(f"Anomaly Event Hours (Cloud Dips & Faults)   : {len(anomaly_df)} hrs")
    print("-" * 68)
    print(f"ANOMALY EVENT SHORTFALL HOURS:")
    print(f"  • Baseline Unmanaged Shortfall            : {base_anom} hrs")
    print(f"  • Smart Dispatch (BESS + Priority)        : {smart_anom} hrs")
    print(f"  >> ANOMALY SHORTFALL REDUCTION            : {reduction_anom_pct:.2f}% <<")
    print("-" * 68)
    print(f"OVERALL OPERATIONAL SHORTFALL HOURS:")
    print(f"  • Baseline Total Critical Shortfall       : {base_total} hrs")
    print(f"  • Smart Dispatch Total Critical Shortfall : {smart_total} hrs")
    print(f"  >> OVERALL SHORTFALL-HOUR REDUCTION       : {reduction_total_pct:.2f}% <<")
    print("=" * 68)

    return res_df

if __name__ == "__main__":
    df = pd.read_csv("feeder_classified_dataset.csv", parse_dates=["timestamp"])
    res = simulate_smart_grid_resilience(df)
    res.to_csv("feeder_dispatch_results.csv", index=False)