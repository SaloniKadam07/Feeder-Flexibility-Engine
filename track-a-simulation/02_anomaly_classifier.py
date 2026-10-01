import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

def detect_and_classify(df):
    """
    Classifies grid states:
    - Normal
    - Weather Dip: Irradiance drops > 50% below expected clear-sky solar curve during peak hours.
    - Equipment Fault: Local generation collapses to ~0 despite high solar irradiance.
    """
    predictions = []

    for _, row in df.iterrows():
        irr = row["solar_irradiance"]
        gen = row["generation_kw"]
        cap = row["pv_capacity_kw"]
        hr = row["timestamp"].hour

        # Theoretical clear-sky benchmark for this exact hour
        clear_sky_expected = max(0.0, 1000.0 * np.sin(np.pi * (hr - 6) / 12.0)) if 6 <= hr <= 18 else 0.0

        if 8 <= hr <= 17 and clear_sky_expected > 200:
            # Check 1: Equipment Fault
            # Clear sky exists (>250 W/m²), but output drops to near zero (<5% capacity)
            if irr > 250 and gen < (cap * 0.05):
                predictions.append("Equipment Fault")

            # Check 2: Weather Dip
            # Cloud bank blocks >60% of expected sunlight during peak hours, generation drops in tandem
            elif (irr < clear_sky_expected * 0.40) and (gen < cap * 0.30):
                predictions.append("Weather Dip")

            else:
                predictions.append("Normal")
        else:
            predictions.append("Normal")

    df["predicted_event"] = predictions
    return df

if __name__ == "__main__":
    df = pd.read_csv("feeder_simulated_dataset.csv", parse_dates=["timestamp"])
    classified_df = detect_and_classify(df)

    output_path = "feeder_classified_dataset.csv"
    classified_df.to_csv(output_path, index=False)
    print(f"Refined classification saved to: {output_path}\n")

    print("--- UPDATED CLASSIFICATION REPORT ---")
    print(classification_report(classified_df["ground_truth_event"], classified_df["predicted_event"], zero_division=0))
    
    print("--- UPDATED CONFUSION MATRIX ---")
    labels = ["Normal", "Weather Dip", "Equipment Fault"]
    cm = confusion_matrix(classified_df["ground_truth_event"], classified_df["predicted_event"], labels=labels)
    cm_df = pd.DataFrame(cm, index=[f"Actual {l}" for l in labels], columns=[f"Pred {l}" for l in labels])
    print(cm_df)