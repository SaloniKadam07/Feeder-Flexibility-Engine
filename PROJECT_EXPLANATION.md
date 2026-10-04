# Feeder Flexibility Engine — Full Project Explanation

## What problem are we solving?

In India, more and more electricity is coming from solar and wind power instead of coal. This is good for the environment, but there's a catch: solar and wind power isn't always available. When it's cloudy, or when the sun sets, or during monsoon season, the amount of power these sources generate drops suddenly and unpredictably.

This becomes a real problem for ordinary neighbourhoods, especially low-income ones. When power drops, people lose electricity for their fridges (so food spoils), their lights, their medical equipment, and their small shops can't function. Right now, most families deal with this by buying their own diesel generator — but running a diesel generator is expensive, roughly ₹11,800 every month per household, which is a huge burden for families who don't have much money to spare.

Another problem: the tools that exist today to deal with this treat everything separately. One tool might just predict weather, another might just detect faults, another might manage which appliances get power — but nothing combines all of this into one smart, affordable system built specifically for ordinary neighbourhoods.

## What did we actually build?

We built a software system (not physical hardware) that acts like a "smart manager" for a small neighbourhood's electricity. Think of it as one continuous pipeline with five steps:

### Step 1: We created realistic practice data
Since we don't have access to a real neighbourhood's actual electricity data, we built a simulation — basically, realistic pretend data that behaves like a real neighbourhood would. We simulated 5 different "feeders" (a feeder is just the technical term for one local power line that supplies a group of about 50 households) over 30 days, tracking how much power was generated and used every single hour.

### Step 2: We taught the system to predict problems before they happen
Our system looks at the pattern of power generation and can tell, 1 to 2 hours in advance, when a shortage is likely coming — for example, it knows that in the evening, solar power naturally drops while people's electricity use goes up. In our simulation, this early-warning system successfully flagged about 1 in every 5 hours as a coming risk, ahead of time.

### Step 3: We built a "detective" that figures out WHY power dropped
When power actually does drop, the system doesn't just say "there's a problem" — it figures out the likely cause. Is this just because of clouds (a weather dip), or did something actually break (an equipment fault)? This matters because the fix is completely different: for a weather dip, you just wait it out and use backup power; for a fault, you need to send a technician. Our detective got this right 100% of the time in our tests, with zero mistakes.

### Step 4: We built a decision-maker that protects what matters most
When there isn't enough power for everyone, our system automatically decides what to prioritize. It keeps the truly essential things running first — fridges, lights, and medical devices — while temporarily turning off less essential things like water heaters. To make this possible without expensive new infrastructure, we designed the idea of a shared community battery: instead of every house buying its own expensive backup generator, the whole neighbourhood shares one battery, which is far cheaper per household.

### Step 5: We built a screen for the electricity company to see everything
Finally, we built a dashboard — a webpage that an electricity company employee can look at. It clearly shows: which neighbourhood areas are currently having problems, why, what the system is doing about it, and how much things have actually improved. It's not just raw numbers; it's designed so a non-technical person can understand at a glance what's happening and why.

## What did we actually prove with numbers?

We didn't just build an idea — we tested it and got real results from our simulated data:

- **Reliability improved by 88.3%** — before any system, a neighbourhood averaged about 8 hours of power shortage per day; with our full system running (prediction + smart battery use), that dropped to under half an hour per day.
- **Our "detective" was 100% accurate** — it correctly identified every single real shortage event in our test data, with zero false alarms.
- **It's roughly 95% cheaper than the current solution** — a shared battery costs each household about ₹550 per month, compared to about ₹11,800 per month for an individual diesel generator. We even tested this under worse-case assumptions (more expensive batteries, less generator use) and the savings stayed above 90% even then.

## Who would actually run this, and who pays?

We decided the electricity company itself (called a DISCOM) should be the one to operate the shared battery — not a new community group or a random local businessperson. We chose this because the electricity company already has the staff, equipment, and billing systems in place; this way, families just pay a small flat fee (₹550/month) added to their regular electricity bill, without any new complicated payment system.

## What are we honest about — what doesn't work perfectly yet?

We found something important while testing: right now, our system doesn't share the benefits perfectly evenly across all 5 feeders — one particular feeder ended up with more unresolved shortages than the others. Rather than hiding this or pretending everything is perfect, we reported it honestly as a known limitation that we plan to fix in the next phase of development.

## What makes our idea different from what already exists?

We researched what's already being done in India. We found a few examples — like a big battery project in Delhi (BRPL Kilokari) and a community battery pilot by Tata Power — but these are either large utility-owned systems, or they assume households already own their own batteries (which most low-income households don't). Our idea is different because it's specifically sized for neighbourhoods that don't already own any storage, and it connects everything — prediction, detection, decision-making, and utility communication — into one complete, affordable system, rather than just one piece of the puzzle.

## What's the bigger-picture impact?

If this were actually deployed, it would mean: families get reliable power at a fraction of what they currently spend, the electricity company gets an easy way to manage problems without expensive infrastructure upgrades, and it helps India use the clean solar/wind power it's already generating more efficiently, instead of wasting it or needing to build even more power plants.
