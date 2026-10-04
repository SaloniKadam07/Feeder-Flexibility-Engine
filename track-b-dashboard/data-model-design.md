# Data & Model Design

## Dataset Schema
Simulated hourly data across 5 feeders, 30 days (3,600 rows), with these columns:

| Column | Meaning |
|---|---|
| `timestamp` | Hour of simulation |
| `feeder_id` | Feeder_1 through Feeder_5 |
| `solar_irradiance`, `ambient_temp` | Weather inputs driving generation |
| `pv_capacity_kw` | Installed solar capacity for that feeder |
| `generation_kw` | Simulated actual power generated that hour |
| `demand_kw` | Total household demand that hour |
| `critical_load_kw` | Portion of demand that is critical (fridge, lighting, medical) |
| `flexible_load_kw` | Portion of demand that can be shed/shifted |
| `ground_truth_event` | True cause (Normal / Weather Dip / Equipment Fault) — known because data is simulated |
| `predicted_event` | Classifier's guess at the cause |
| `net_load_kw` | demand_kw − generation_kw |
| `unserved_critical_kw` | Critical load left unpowered even after battery dispatch |
| `baseline_crit_shortfall` / `smart_crit_shortfall` | Whether a shortfall occurred, with vs without the system |
| `forecast_warning_flag` | Whether the system predicted this hour's shortfall 1-2 hrs in advance |
| `scen_a/b/c_shortfall` | Shortfall outcome under each of the 3 tested scenarios |

## Classification Model (rule-based, not ML)
The classifier distinguishes three states by comparing actual generation against expected generation for that hour (based on solar irradiance):

- **Normal:** generation roughly matches expected output for current weather
- **Weather Dip:** generation drops significantly below expected, but the drop is gradual/partial and consistent with reduced irradiance (clouds)
- **Equipment Fault:** generation drops to near-zero abruptly, inconsistent with gradual weather-driven loss

This was chosen over a machine-learning model because: (a) the dataset is small (30 days), (b) rule-based logic is fully transparent and auditable by a DISCOM operator, and (c) it achieved 100% accuracy on our simulated test set, so added model complexity wasn't justified.

## Dispatch Logic
On a detected shortfall: critical loads are served first from available generation + battery; if a deficit remains, flexible loads are shed; the shared battery discharges to cover critical loads up to its available state of charge.
