# Feeder Flexibility Engine

**Yuva Yodha Hackathon (Schneider Electric) — Challenge 03: Grid Reliability, Renewable Intermittency**

A software system that detects renewable-generation shortfalls at the feeder level, classifies their cause, dispatches a shared community battery to protect critical loads, and alerts the DISCOM with a recommended action — built for a 5-feeder, 50-household neighbourhood network.

**Live dashboard demo:** https://feeder-flexibility-engine-fc0776.netlify.app

## The problem
Solar and wind generation drops unpredictably with clouds, nightfall and monsoon weather. Low-income urban and peri-urban neighbourhoods are hit hardest, relying on diesel generators that cost roughly ₹11,800/household/month. Today's tools treat forecasting, fault detection and load management as separate systems.

## Our solution
A connected pipeline: simulated feeder data → anomaly classification (weather dip vs equipment fault) → load prioritisation and battery dispatch → DISCOM dashboard, with a unit-economics and ownership model proving affordability.

## Results (from our simulation)
- **88.3% reduction** in average shortfall hours (3.64 → 0.43 hrs/day/feeder), tested across 3 scenarios: no system (8.03 hrs), load-shedding only (3.64 hrs), full system (0.43 hrs)
- **100% detection accuracy**, zero false alarms, across 26 real shortfall events in a 30-day simulation
- **₹550/household/month** under our shared-battery model, vs **₹11,800/household/month** for individual diesel generators — a 95% reduction
- Advance-warning forecasting flagged 21% of simulated hours ahead of a shortfall
- **Honest limitation:** critical-load shortfalls are not yet evenly distributed across feeders (Feeder 5 saw ~2.6x more unserved critical load than Feeder 1) — a planned refinement for the prototype phase

## How to run

### Track A (simulation)
```bash
cd track-a-simulation
pip install pandas numpy
python 01_dataset_generator.py
python 02_anomaly_classifier.py
python 03_dispatch_and_metrics.py
python 04_generate_plots.py
python 05_enhancements.py
```
Each script reads the previous step's output and writes its own CSV into `data/`.

### Track B (dashboard)
Open `track-b-dashboard/dashboard/dashboard.html` directly in any browser — no build step required. Live version: https://feeder-flexibility-engine-fc0776.netlify.app

## Team
- **Saloni Kadam** — DISCOM dashboard, unit economics, ownership/O&M model, architecture design
- **Sadeem Khan** — Data simulation, anomaly detection, dispatch logic, reliability metrics
