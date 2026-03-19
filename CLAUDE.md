# CLAUDE.md

## Project

Energy Project Preparation PoC — site selection and technology selection at pre-feasibility scope for Porto Alegre, Brazil.

## Key Context

- The application UI lives in Geo-Layer-Viewer (github.com/joaquinOEF/Geo-Layer-Viewer)
- This repo is documentation, data, analysis, and agent tooling — not a standalone app
- Python for analysis scripts, JSON for data, Markdown for docs/prompts
- Pre-feasibility scope: ranges and archetypes, not engineering precision
- `city_data/` contains Porto Alegre PLAC (climate action plan) documents
- See agents.md for agent role definitions and rules

## Important Files

- `data/layers-energy-mapping.json` — maps Geo-Layer-Viewer layers to energy use cases
- `data/energy-tech-catalog.json` — technology archetypes and parameters
- `schemas/` — JSON Schema contracts for all structured data
- `agent/prompts/` — versioned prompt templates (always note changes)
- `analysis/shared/geo_client.py` — Geo-Layer-Viewer API wrapper
- `analysis/shared/global_api_client.py` — CityCatalyst Global API wrapper

## Rules

- Never hardcode Geo-Layer-Viewer layer IDs — always reference `data/layers-energy-mapping.json`
- All structured data must have a matching schema in `schemas/`
- Research findings go in `data/research/` with source attribution and dates
- Agent suggestions use the patch format defined in `schemas/patch.json`
- Keep `agents.md` in sync when adding new agent capabilities or tools

## Commands

- Run tests: `pytest tests/`
- Validate data files: `python -m analysis.shared.data_loader --validate`
- Test geo client connection: `python -m analysis.shared.geo_client --test`

## Commit Conventions

- `feat:` new analysis capability or agent tool
- `data:` reference data addition or update
- `research:` new research entry
- `docs:` documentation change
- `prompt:` prompt template change (always note what changed and why)
- `schema:` schema change (may break downstream)
- `fix:` bug fix in analysis or tooling
- `test:` test addition or fix
