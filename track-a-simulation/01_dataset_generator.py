import numpy as np
import pandas as pd

def generate_feeder_data(n_feeders=5, days=30, seed=42):
    np.random.seed(seed)
    timestamps = pd.date_range(start="2026-09-01", periods=days * 24, freq="h")
    records = []

    for f_id in range(1, n_feeders + 1):
        # Feeder capacities
        pv_capacity_kw = 40 + (f_id * 10)   # 50 kW to 90 kW
        base_demand_kw = 35 + (f_id * 8)    # Baseline demand per feeder

        for t in timestamps:
            hour = t.hour
            
            # 1. Environmental factors (Weather)
            clear_sky_irr = max(0, 1000 * np.sin(np.pi * (hour - 6) / 12)) if 6 <= hour <= 18 else 0.0
            cloud_factor = np.clip(np.random.normal(1.0, 0.12), 0.05, 1.0)
            irradiance = round(clear_sky_irr * cloud_factor, 2)
            temperature = round(24 + 7 * np.sin(np.pi * (hour - 8) / 12) + np.random.normal(0, 0.4), 2)

            # 2. Demand Profile (Morning + Evening peaks)
            morning_peak = 25 * np.exp(-((hour - 9) ** 2) / 6)
            evening_peak = 35 * np.exp(-((hour - 20) ** 2) / 6)
            demand_kw = round(base_demand_kw + morning_peak + evening_peak + np.random.normal(0, 2.5), 2)

            # 3. Solar Generation (with temperature loss coefficient)
            temp_derating = 1 - 0.004 * (temperature - 25)
            pv_gen = max(0.0, pv_capacity_kw * (irradiance / 1000.0) * temp_derating)
            generation_kw = round(pv_gen, 2)

            # 4. Load Prioritization Split
            critical_load_kw = round(demand_kw * 0.60, 2)
            flexible_load_kw = round(demand_kw * 0.40, 2)

            records.append({
                "timestamp": t,
                "feeder_id": f"Feeder_{f_id}",
                "solar_irradiance": irradiance,
                "ambient_temp": temperature,
                "pv_capacity_kw": pv_capacity_kw,
                "generation_kw": generation_kw,
                "demand_kw": demand_kw,
                "critical_load_kw": critical_load_kw,
                "flexible_load_kw": flexible_load_kw,
                "ground_truth_event": "Normal"
            })

    df = pd.DataFrame(records)

    # 5. Inject Anomaly Scenarios
    # Scenario A: Regional Weather Dip (Day 6, 11:00 - 14:00 across multiple feeders)
    weather_mask = (df["timestamp"].dt.day == 6) & (df["timestamp"].dt.hour.between(11, 14))
    df.loc[weather_mask, "solar_irradiance"] = (df.loc[weather_mask, "solar_irradiance"] * 0.2).round(2)
    df.loc[weather_mask, "generation_kw"] = (df.loc[weather_mask, "generation_kw"] * 0.2).round(2)
    df.loc[weather_mask, "ground_truth_event"] = "Weather Dip"

    # Scenario B: Inverter/Equipment Fault (Day 14, 10:00 - 15:00 on Feeder_3 only)
    fault_mask = (df["feeder_id"] == "Feeder_3") & (df["timestamp"].dt.day == 14) & (df["timestamp"].dt.hour.between(10, 15))
    df.loc[fault_mask, "generation_kw"] = 0.0
    df.loc[fault_mask, "ground_truth_event"] = "Equipment Fault"

    df["net_load_kw"] = (df["demand_kw"] - df["generation_kw"]).round(2)
    return df

if __name__ == "__main__":
    df = generate_feeder_data(n_feeders=5, days=30)
    output_path = "feeder_simulated_dataset.csv"
    df.to_csv(output_path, index=False)
    print(f"Success! Saved {len(df)} rows across 5 feeders to {output_path}")
    print("\nEvent breakdown in generated dataset:")
    print(df["ground_truth_event"].value_counts())