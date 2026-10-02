# System Architecture

See `diagrams/architecture_diagram.png` for the visual version. This document explains it in text.

## Components (left to right)

1. **Data Layer** — Simulated feeder data: generation, demand, weather, across 5 feeders, 30 days hourly.
2. **Detection Engine** — Anomaly classifier distinguishing weather dip vs equipment fault vs normal, using generation-vs-expected comparison (100% accuracy on simulated test set).
3. **Dispatch and Prioritization Engine** — Prioritises critical loads (refrigeration, lighting, medical), sheds flexible loads, dispatches the shared battery, and calculates reliability metrics.
4. **DISCOM Dashboard Layer** — Displays shortfall alert → cause → recommended action, plus the 3-scenario reliability comparison and feeder-level status.
5. **Economics and Ownership Layer** — Unit economics (₹550 vs ₹11,800/household/month) and the O&M model (DISCOM as operator).

## Flow types (color-coded in the diagram)

- **Data flow (blue):** Data Layer → Detection Engine → Dispatch Engine → Dashboard
- **Energy flow (orange):** Dispatch Engine → Shared Battery → Critical Loads
- **Money flow (green):** Households → Economics Layer → Shared Battery (funds its upkeep)

## Not yet shown in the diagram (added after it was drawn)
Two features were added to the pipeline after this diagram was finalized, and aren't visually represented yet:
- **Advance warning / forecasting** — sits inside the Detection Engine, flagging shortfalls 1-2 hours ahead
- **3-scenario comparison logic** — sits inside the Dispatch Engine, used to produce the no-system/shedding-only/full-system results

