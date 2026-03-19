# Action Analysis Prompt

You are analyzing energy actions for a city's pre-feasibility assessment. Your task is to evaluate which high-impact energy actions should be prioritized, based on baseline context.

## Inputs

- **City**: {{city_name}} ({{city_locode}})
- **Context documents**: Contents of `context/` directory for this city
- **Action catalog**: `data/energy-action-catalog.json`
- **Scoring weights**: `data/scoring-weights.json` → `actionScoring` section

## Your Task

1. **Read all context dimensions** — geographic, technology, financing, regulatory, and reference projects. Extract key signals:
   - What are the top energy problems?
   - What has the city/state already committed to?
   - What do funders in this region prioritize?
   - What regulatory enablers or barriers exist?

2. **Evaluate each action** in the catalog against the context signals:
   - Which supportive signals match?
   - Are there any blocking signals?
   - Does the action align with existing commitments?
   - Is there a financing pathway available?

3. **Score and rank** using the weighted criteria in scoring-weights.json.

4. **Build a portfolio** — actions don't exist in isolation. Identify:
   - Which actions pair well (e.g., solar + storage, efficiency + solar)
   - Which actions are prerequisites for others
   - Whether the portfolio addresses the key problems holistically

5. **Output** a structured result conforming to `schemas/action-selection.json`.

## Rules

- Pre-feasibility scope: use ranges and archetypes, not precise numbers
- Always cite which context documents informed your signals
- If a blocking signal is present, mark the action as "conditional" with a clear note on what needs to change
- Actions aligned with existing city commitments should get a scoring boost
- The portfolio should be actionable — avoid more than 5 priority actions

## Output Format

Propose your result as a structured patch to the project context's `actionSelection` field, following the patch format in `schemas/patch.json`.
