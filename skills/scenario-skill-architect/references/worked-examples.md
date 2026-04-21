# Worked Examples

## Contents

- Travel itinerary planner: domain discovery first
- Product launch news release: full package after domain contract
- Relationship clarification: safer redesign

## 1. Travel itinerary planner: domain discovery first

Raw request:

> I want to create a skill for writing travel guides.

Correct architect behavior:

- Hard gates likely pass: travel guides are recurring and can be evaluated.
- Domain substance gates are unknown: target user, output depth, domain variables, data policy, hidden pitfalls, expert rubric, and examples are missing.
- Route: `create/domain_discovery`, not `create/full_skill`.

Questions to ask:

1. Is the artifact an executable itinerary, inspiration guide, booking-prep plan, content post, or agency-style travel proposal?
2. Who is the user: solo traveler, couple, family with children, elders, budget traveler, luxury traveler, business traveler?
3. Must the output include time blocks, transfer distance/time, budget, hotel-zone logic, ticket/reservation checklist, weather fallback, walking intensity, and backup plans?
4. Which facts may be estimated and which require live verification?
5. What common pitfalls should the skill prevent?
6. Can you provide one good travel plan and one bad plan?

Provisional domain content contract:

```yaml
domain_content_contract:
  target_user: unknown
  artifact_type: "travel itinerary or guide, exact type unknown"
  output_depth: unknown
  required_variables:
    - dates_or_trip_length
    - origin_and_destination
    - traveler_profile
    - budget_range
    - transport_preference
    - accommodation_zone_logic
    - time_blocks
    - transfer_time_distance
    - ticket_or_reservation_needs
    - weather_and_backup_plan
  hidden_failure_modes:
    - "Looks complete but has impossible transfer timing"
    - "No budget split or hidden cost handling"
    - "No holiday/crowd/reservation warning"
    - "No mobility or walking-load adaptation"
  data_source_policy:
    realtime_required:
      - ticket prices
      - train/flight schedules
      - opening hours
      - holiday closures
      - weather
    can_estimate_with_label:
      - rough meal budget
      - approximate local transfer time
    must_not_fabricate:
      - exact prices
      - exact schedules
      - hotel availability
  expert_quality_checks:
    - "Can a traveler execute this day by day?"
    - "Are time, money, transport, and fatigue visible?"
    - "Are alternatives and verification tasks clear?"
  worked_examples_needed:
    - "one complete itinerary"
    - "one surface-level bad guide"
  domain_eval_cases:
    - "holiday trip with crowd/reservation risk"
    - "family/elder trip with mobility constraints"
    - "budget-limited trip requiring trade-offs"
```

Do not finalize the skill until discovery is answered or assumptions are explicitly accepted.

## 2. Product launch news release

A full package is allowed only after domain contract covers audience, announcement type, facts, metrics, quotes, embargo, legal review, brand voice, and media target. Failure knowledge must include fabricated quotes, unsupported metrics, excessive marketing tone, and missing news hook.

## 3. Relationship clarification

Requests to infer hidden intent from private monitoring should not become a skill. Redesign as a consent-aware communication clarification workflow that separates observed words, hypotheses, uncertainty, and non-manipulative next steps.
