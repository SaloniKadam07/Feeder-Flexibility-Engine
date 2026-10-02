# Feeder Flexibility Engine — Solution Summary

**Yuva Yodha Hackathon (Schneider Electric) — Challenge 03: Grid Reliability, Renewable Intermittency**

## The Problem
Solar and wind generation drops unpredictably with clouds, nightfall and monsoon weather. Low-income urban and peri-urban neighbourhoods are hit hardest, currently relying on diesel generators costing roughly ₹11,800/household/month.

## Our Solution
A software pipeline for a 5-feeder, 50-household neighbourhood network: detects shortfalls, classifies the cause (weather dip vs equipment fault), prioritises critical loads, dispatches a shared battery, and alerts the DISCOM with a recommended action.

## Key Results

| Metric | Result |
|---|---|
| Shortfall hours reduced | 3.64 → 0.43 hrs/day/feeder (**88.3%**) |
| Detection accuracy | **100%** (26 real events, 0 false alarms) |
| Cost per household | ₹550/month vs ₹11,800/month (**95% cheaper**) |
| Forecast coverage | 21% of hours flagged 1-2 hrs ahead |
| 3-scenario comparison | No system: 8.03 hrs → Shedding only: 3.64 hrs → Full system: 0.43 hrs |

## Ownership & Affordability
The DISCOM operates the shared battery directly, billing a flat ₹550/household/month through existing infrastructure, replacing individual diesel generator costs.

## Honest Limitation
Critical-load shortfalls are not yet evenly distributed across feeders (Feeder 5 saw ~2.6x more unserved critical load than Feeder 1) — a planned refinement for the prototype phase.

## Team
**Saloni Kadam** — DISCOM dashboard, economics, O&M model, architecture
**Sadeem Khan** — Simulation, detection, dispatch logic

## Links
- Live dashboard: https://feeder-flexibility-engine-fc0776.netlify.app
- Repo: https://github.com/SaloniKadam07/Feeder-Flexibility-Engine