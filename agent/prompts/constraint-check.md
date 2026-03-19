# Constraint Check Prompt

You are verifying the consistency and completeness of constraint analysis for energy site selection in {{city_name}}.

## Context

- Constraint definitions: data/site-constraint-types.json
- Layer mapping: data/layers-energy-mapping.json
- Current site selection results provided below

## Task

Review the constraint analysis and check for:

1. **Missing constraints** — are there important constraints not yet defined? (e.g., airport buffer zones, heritage sites, grid capacity limits)
2. **Threshold reasonableness** — are the thresholds in constraint definitions appropriate for {{city_name}}?
3. **Data gaps** — which constraints couldn't be evaluated due to missing layer data?
4. **Inconsistencies** — do any site scores seem inconsistent with their constraint results?

## Output

Provide findings as a list of issues with severity (blocker / warning / info) and recommended actions.
