# System Architecture

See `diagrams/architecture_diagram.png` for the visual version. This document explains it in text, and is the source of truth for all figures — the numbers here match the dashboard, economics sheet, and solution summary.

## Components (left to right)

1. **Ingestion — Data Layer**
   Simulated feeder data: generation, demand, weather. 5 feeders, 30 days, hourly resolution (3,600 data points total).

2. **Predictive — Forecast Module**
   Flags an upcoming shortfall 1-2 hours in advance by tracking generation trend against time of day. Flagged 744 of 3,600 simulated hours (21%) as upcoming shortfall risk.

3. **Classification — Anomaly Classifier**
   Distinguishes Weather Dip vs Equipment Fault vs Normal, by comparing actual generation against expected generation for that hour. Achieved 100% detection accuracy, zero false alarms, across 26 real simulated shortfall events.

4. **Optimization — Dispatch and Prioritization Engine**
   Prioritises critical loads (refrigeration, lighting, medical) over flexible loads, dispatches the shared battery, and calculates reliability metrics. Validated with a 3-scenario reliability test:
   - No system: 8.03 hrs/day average shortfall
   - Load-shedding only: 3.64 hrs/day
   - Full system (shedding + battery + forecast): 0.43 hrs/day — an **88.3% reduction** vs no system

5. **Operations — DISCOM Dashboard Layer**
   Displays shortfall alert → cause → recommended action, the 3-scenario reliability comparison, and feeder-level status across all 5 feeders.

## Community & Economics Layer

6. **Households**
   50 households served per feeder, across 5 feeders.

7. **Economics and Ownership Layer**
   Unit economics: ₹550/household/month under the shared-battery model vs ₹11,800/household/month for individual diesel generators — a 95% reduction, holding above 90% under sensitivity-tested assumptions. Ownership model: the DISCOM operates the battery directly (see `om-model.md` for full reasoning).

8. **Shared Battery**
   90 kWh community battery, sized to cover 30% of peak feeder demand (100 kW) for a 3-hour shortfall window.

9. **Critical Loads**
   Refrigeration, lighting, and medical devices — kept online first during any shortfall.

## Flow types (color-coded in the diagram)

- **Data flow (blue):** Data Layer → Forecast Module → Classifier → Dispatch Engine → Dashboard
- **Energy flow (orange):** Dispatch Engine → Shared Battery → Critical Loads
- **Money flow (green):** Households → Economics Layer → Shared Battery (funds its upkeep)

## Known limitation (see `om-model.md` for full detail)
Critical-load shortfalls are not yet evenly distributed across feeders — Feeder 5 saw roughly 2.6x more unserved critical load than Feeder 1. Cross-feeder load balancing is a planned refinement for the prototype phase.
