# agents.md — Energy Project Preparation PoC

## Project Overview

Energy project preparation PoC focused on site selection and technology selection at pre-feasibility scope. This repo provides documentation, reference data, analysis scripts, and AI agent tooling. The application UI lives in the [Geo-Layer-Viewer](https://github.com/joaquinOEF/Geo-Layer-Viewer) repo.

**Target city**: Porto Alegre, Brazil (BR POA)
**Scope**: Pre-feasibility / concept-note — use ranges, archetypes, and "good enough" defaults, not full engineering design.

## Architecture Rules

- This repo does NOT contain application code — the app is Geo-Layer-Viewer
- Analysis scripts in `analysis/` talk to Geo-Layer-Viewer via `analysis/shared/geo_client.py`
- All reference data lives in `data/` as JSON — keep it human-editable and git-versioned
- Schemas in `schemas/` define the contracts between analysis, agents, and outputs
- Prompt templates in `agent/prompts/` must be versioned and auditable
- Agent suggestions use the patch format defined in `schemas/patch.json`
- Never hardcode Geo-Layer-Viewer layer IDs — use `data/layers-energy-mapping.json`
- Pre-feasibility scope: use ranges, archetypes, and defaults — not engineering precision

## External Dependencies

| Service | Client | Purpose |
|---------|--------|---------|
| Geo-Layer-Viewer API | `analysis/shared/geo_client.py` | Geospatial layers, raster values, spatial queries |
| CityCatalyst Global API | `analysis/shared/global_api_client.py` | City emissions data, metadata |
| OEF S3 Tile Catalog | via Geo-Layer-Viewer proxy | Raster tile access |

## Agent Roles

### 1. Research Agent

**Purpose**: Gather, synthesize, and store research on energy topics
**Scope**: Web search, literature review, benchmark collection, policy analysis

**Rules**:
- Store findings as structured JSON in `data/research/`
- Always include source URLs, retrieval dates, and confidence notes
- Never overwrite existing research — append with timestamps
- Use `agent/prompts/research-synthesis.md` as the base prompt
- Tag each finding with relevant component (`site-selection` / `technology-selection`)

### 2. Site Analysis Agent

**Purpose**: Analyze geospatial data to identify and score candidate sites
**Scope**: Query Geo-Layer-Viewer layers, apply constraints, run scoring

**Rules**:
- Use `analysis/shared/geo_client.py` to access geo data — never call APIs directly
- Reference `data/layers-energy-mapping.json` for layer relevance
- Apply constraints from `data/site-constraint-types.json`
- Use scoring weights from `data/scoring-weights.json`
- Output must conform to `schemas/site-selection.json`

### 3. Technology Agent

**Purpose**: Recommend and size energy technologies for selected sites
**Scope**: Match tech to site, estimate sizing, assess feasibility

**Rules**:
- Reference `data/energy-tech-catalog.json` for technology archetypes
- Use pre-feasibility ranges, not engineering precision
- Cross-reference site constraints (e.g., roof area limits rooftop PV capacity)
- Output must conform to `schemas/technology-selection.json`

### 4. Output Agent

**Purpose**: Generate structured deliverables from analysis results
**Scope**: Site summaries, tech shortlists, concept briefs

**Rules**:
- Use templates in `outputs/templates/` as structure
- Cite data sources and analysis provenance
- Keep outputs concise — concept-note scope, not full PDD
- Generated outputs go to `outputs/examples/` for review

### 5. Review Agent

**Purpose**: Review changes, validate data quality, check consistency

**Rules**:
- Verify JSON data files parse correctly and match their schemas
- Check that analysis scripts handle missing data gracefully
- Ensure prompt templates haven't changed without changelog entry
- Flag scoring weight changes (they affect all site rankings)
- Verify `geo_client.py` calls match current Geo-Layer-Viewer API endpoints

## File Conventions

| Type | Location | Format |
|------|----------|--------|
| Reference data | `data/*.json` | Flat JSON, git-versioned, human-editable |
| Research | `data/research/<category>/<topic>.json` | Structured JSON with provenance |
| Analysis scripts | `analysis/<component>/<script>.py` | Python |
| Shared clients | `analysis/shared/*.py` | Python |
| Prompts | `agent/prompts/*.md` | Markdown, auditable |
| Tool definitions | `agent/tools/*.py` | Python |
| Schemas | `schemas/*.json` | JSON Schema |
| Output templates | `outputs/templates/*.md` | Markdown |
| Generated outputs | `outputs/examples/*.md` | Markdown |
| Tests | `tests/test_*.py` | pytest |

## Commit Conventions

| Prefix | Use |
|--------|-----|
| `feat:` | New analysis capability or agent tool |
| `data:` | Reference data addition or update |
| `research:` | New research entry |
| `docs:` | Documentation change |
| `prompt:` | Prompt template change (always note what changed and why) |
| `schema:` | Schema change (may break downstream) |
| `fix:` | Bug fix in analysis or tooling |
| `test:` | Test addition or fix |
