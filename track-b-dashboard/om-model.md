# Ownership, Operations & Maintenance Model

## Ownership
The DISCOM operates the shared community battery directly, as an extension of its existing feeder-level infrastructure, rather than through a separate neighbourhood committee or a private micro-entrepreneur.

## Why DISCOM as Operator
We considered three ownership models for the shared battery: a neighbourhood committee, a private micro-entrepreneur, and the DISCOM itself.

- A **committee** model requires building new governance and technical capacity from scratch, adding delay and risk for a community least able to absorb either.
- A **micro-entrepreneur** model introduces a new, unregulated billing relationship on top of households' existing electricity bills, adding complexity without a clear advantage.
- The **DISCOM** already maintains feeder-level equipment, already bills these households monthly, and already carries regulatory accountability for reliable supply — making it the lowest-friction, most accountable operator, rather than requiring new institutions to be built around it.

## Operations
- The DISCOM monitors the feeder-flexibility dashboard in real time.
- On a detected shortfall, the DISCOM's dispatch logic automatically prioritises critical loads (refrigeration, lighting, medical devices) and dispatches the shared battery.
- Battery maintenance, monitoring, and eventual replacement are handled by the DISCOM, the same as any other grid asset under its care.

## Pricing
- A flat fee of ₹550/household/month is added to each household's existing electricity bill.
- This replaces the ~₹11,800/household/month households currently spend on diesel generator fuel and upkeep — a 95% reduction.
- No new payment infrastructure is required, since billing already runs through the DISCOM.

## Fair Access — Honest Finding
Our dispatch rules currently prioritise critical loads **by load type** (critical vs flexible) but do not yet balance shortfalls **evenly across feeders**. In our 30-day simulation, Feeder 5 experienced roughly 2.6x more unserved critical load than Feeder 1.

This is a known gap, not a resolved claim. Addressing cross-feeder equity — for example through load-balancing rules that account for each feeder's historical shortfall burden — is a planned refinement for the prototype phase (Oct 11–Nov 22).

## Summary
| Aspect | Model |
|---|---|
| Operator | DISCOM |
| Billing | Flat ₹550/household/month, via existing electricity bill |
| Baseline cost (diesel genset) | ~₹11,800/household/month |
| Savings | ~95% |
| Fair access status | Fair by load type; not yet fair across feeders (known limitation) |

## Known Risks / What We'd Validate First
Our most fragile assumption is the 3 hrs/day genset baseline — real household backup behavior varies by season, income, and generator access, and our simulation uses one fixed average. In a real pilot, the first thing we'd measure is actual household backup usage patterns over at least one full month, including monsoon, to confirm whether our affordability comparison (₹550 vs ₹11,800) holds at the extremes, not just the average case.
