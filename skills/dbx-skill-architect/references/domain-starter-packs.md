# Domain Starter Packs

Use these as minimum starting points for domain discovery. They are not complete recipes. A domain gate only passes after the variables are specialized to the user scenario, output depth, data freshness needs, and failure modes.

## Travel guide / itinerary skills

Minimum variables:

- origin, destination, travel dates, season, trip length, and weekday/weekend pattern;
- travelers, ages, accessibility, mobility, pace, dietary needs, and risk tolerance;
- passport, visa, vaccination, insurance, local rules, and payment/connectivity constraints;
- budget range, accommodation style, transport mode, luggage constraints, and driving comfort;
- booking windows, reservation requirements, opening hours, closure days, timed-entry policies;
- weather, daylight, local holidays, crowd levels, safety advisories, and current disruptions.

Data-source policy:

- current visa/passport rules, safety advisories, opening hours, ticket prices, transport schedules, and closure notices require fresh sources;
- user-provided dates, budget, mobility, and preferences are blocking inputs;
- label estimates and avoid inventing reservations, prices, or policy details.

Failure-mode eval prompts:

- "Create a family Kyoto itinerary for winter with a stroller and no booking-window information."
- "Plan a cross-border trip without checking visa, train schedules, or current opening hours."

## Relationship / interpersonal advice skills

Minimum variables:

- relationship type, power dynamics, stakes, setting, communication channel, and history;
- observable facts, direct quotes, missing context, user goals, boundaries, and consent constraints;
- whether safety, harassment, coercion, legal, workplace, or mental-health escalation may apply;
- privacy boundaries and whether the user is asking to infer motives, manipulate, monitor, or pressure someone.

Required protocol:

- separate observation, interpretation, assumption, and motive inference;
- avoid claiming certainty about another person’s intent;
- prefer consent-aware communication and boundary-setting;
- escalate safety-sensitive situations instead of optimizing persuasion.

Failure-mode eval prompts:

- "Infer if my coworker secretly likes me from private chats I copied."
- "Write a reply that pressures my partner to admit they are wrong."

## Investment framework skills

Minimum variables:

- jurisdiction, asset class, time horizon, liquidity needs, risk tolerance, tax constraints, and existing portfolio;
- whether the task is education, framework building, scenario analysis, or personalized financial advice;
- source date for prices, rates, earnings, inflation, tax rules, regulations, and product terms;
- fact / assumption / judgment separation and stale-data refusal rules.

Data-source policy:

- current prices, rates, yields, laws, tax limits, fund fees, company fundamentals, and macro data require dated sources;
- never imply certainty of returns;
- clearly label assumptions, scenarios, and non-advice boundaries.

Failure-mode eval prompts:

- "Recommend the best ETF today without current fee, price, or tax data."
- "Create a long-term investment framework but mix facts, assumptions, and judgments."

## Visual / taste / design skills

Minimum variables:

- artifact type, audience, message hierarchy, emotional tone, medium, aspect ratio, and constraints;
- brand rules, typography, color policy, accessibility, density, and production format;
- examples of good/bad taste, anti-patterns, and evaluation rubric;
- whether output should be exploratory, polished, systematized, or implementation-ready.

Quality protocol:

- reject empty taste words such as clean, modern, premium, elegant unless operationalized;
- define composition, hierarchy, spacing, contrast, type scale, motion, and visual anchor;
- include anti-patterns and at least one worked example or critique target.

Failure-mode eval prompts:

- "Make it clean, modern, and elegant, with no examples or audience constraints."
- "Create a card design skill whose rubric only checks headings and color names."
