# Concept Brief Generation Prompt

You are generating a pre-feasibility concept brief for an energy project in {{city_name}}.

## Context

You have access to:
- Site selection results (top candidate zones with scores and characteristics)
- Technology selection results (shortlisted technologies with sizing and cost ranges)
- Research findings in data/research/
- City documents in city_data/

## Task

Generate a concise concept brief (1-2 pages) that includes:

1. **Project Overview** — what, where, why
2. **Site Assessment** — top candidate zone(s), key characteristics, constraints addressed
3. **Technology Recommendation** — recommended technology, sizing ranges, rationale
4. **Estimated Impact** — emissions reduction potential, beneficiary reach, resilience benefits
5. **Cost Indicative Range** — CAPEX range, LCOE comparison to grid tariff
6. **Financing Pathway** — suitable financing archetypes, next steps for funding
7. **Key Risks and Mitigation** — top 3-5 risks with suggested mitigation
8. **Next Steps** — what's needed to move from pre-feasibility to detailed feasibility

## Output Format

Markdown document following the template in outputs/templates/concept-brief.md

## Rules

- Pre-feasibility scope — be clear about what's estimated vs. confirmed
- Cite data sources for key figures
- Use ranges, not single-point estimates
- Write for a city official or funder audience — clear, non-technical language
- Keep it concise — 1-2 pages maximum
