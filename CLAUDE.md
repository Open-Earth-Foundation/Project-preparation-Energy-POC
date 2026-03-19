# CLAUDE.md

## Project

Energy Project Preparation PoC — action selection, site selection, and technology selection at pre-feasibility scope for Porto Alegre, Brazil.

## Key Context

- The application UI lives in Geo-Layer-Viewer (github.com/joaquinOEF/Geo-Layer-Viewer)
- This repo is documentation, data, analysis, and agent tooling — not a standalone app
- Python 3.11+ for analysis scripts, JSON for data, Markdown for docs/prompts
- Pre-feasibility scope: ranges and archetypes, not engineering precision
- `context/` contains baseline context organized by dimension (geographic, technology, financing, regulatory, projects)
- See agents.md for agent role definitions and rules

## Important Files

### Data
- `data/energy-action-catalog.json` — action archetypes (upstream of site/tech selection)
- `data/energy-tech-catalog.json` — technology archetypes and parameters
- `data/layers-energy-mapping.json` — maps Geo-Layer-Viewer layers to energy use cases
- `data/site-constraint-types.json` — constraint definitions for site filtering
- `data/scoring-weights.json` — scoring weight configuration for site ranking
- `data/financing-archetypes.json` — financing archetype definitions
- `data/research/` — curated benchmarks and external data (e.g., `benchmarks/solar-pv-brazil-2024.json`, `ccglobal-energy-actions.json`)

### Context
- `context/` — baseline context: geographic, technology, financing, regulatory, reference projects
- `context/geographic/porto-alegre/` — PLAC documents (executive summary, work plan), YAML action lists
- `context/geographic/rio-grande-do-sul/` — state-level energy context
- `context/geographic/brazil/` — national energy plan

### Analysis
- `analysis/action-selection/` — action scoring pipeline: context signals, scoring, CCGlobal integration
- `analysis/site-selection/` — candidate zones, constraint filtering, site scoring
- `analysis/technology-selection/` — tech matching, sizing estimates
- `analysis/shared/geo_client.py` — Geo-Layer-Viewer API wrapper
- `analysis/shared/global_api_client.py` — CityCatalyst Global API wrapper
- `analysis/shared/data_loader.py` — reference data loading and validation
- `analysis/shared/types.py` — shared dataclasses (SiteCharacteristics, ScoredZone, TechnologyMatch, Patch, etc.)

### Agent
- `agent/orchestrator.py` — agent orchestrator (prompt loading, context preparation, LLM dispatch)
- `agent/patches.py` — patch creation, application, and serialization logic
- `agent/prompts/` — versioned prompt templates (action-analysis, site-analysis, tech-recommendation, constraint-check, concept-brief, research-synthesis)
- `agent/tools/` — tool definitions for agent use

### Outputs
- `outputs/templates/` — Markdown templates (site-summary, tech-shortlist, concept-brief)
- `outputs/generators/` — Python generators that populate templates from analysis results

### Schemas & Docs
- `schemas/` — JSON Schema contracts: action-selection, site-selection, technology-selection, project-context, patch
- `docs/architecture.md` — system architecture and data flow
- `docs/data-sources.md` — catalog of external data sources
- `docs/methodology/` — methodology docs (site-selection, technology-selection, scoring-model, constraints-taxonomy)
- `docs/references/` — reference material (GPC energy sector)

### Policy Research
- `grid_policy/` — Porto Alegre energy/climate legal framework and PV energy selling analysis

### Config
- `.env.example` — environment variable template (API URLs, LLM config)
- `pyproject.toml` — project config (Python 3.11+, pytest, black)
- `requirements.txt` — Python dependencies (requests, jsonschema, anthropic, pytest)

## Rules

- Never hardcode Geo-Layer-Viewer layer IDs — always reference `data/layers-energy-mapping.json`
- All structured data must have a matching schema in `schemas/`
- Research findings go in `data/research/` with source attribution and dates
- Agent suggestions use the patch format defined in `schemas/patch.json`
- Keep `agents.md` in sync when adding new agent capabilities or tools
- Context signals for action scoring are in `analysis/action-selection/context_signals.py` — update when new context is added

## Commands

- Run tests: `pytest tests/`
- Run action selection: `python -m analysis.action-selection.run_action_selection --city "BR POA"`
- Run action selection (local catalog only): `python -m analysis.action-selection.run_action_selection --city "BR POA" --no-ccglobal`
- Validate data files: `python -m analysis.shared.data_loader --validate`
- Test geo client connection: `python -m analysis.shared.geo_client --test`
- Run agent orchestrator: `python -m agent.orchestrator --prompt site-analysis --city "Porto Alegre"`

## Commit Conventions

- `feat:` new analysis capability or agent tool
- `data:` reference data addition or update
- `research:` new research entry
- `docs:` documentation change
- `prompt:` prompt template change (always note what changed and why)
- `schema:` schema change (may break downstream)
- `fix:` bug fix in analysis or tooling
- `test:` test addition or fix
