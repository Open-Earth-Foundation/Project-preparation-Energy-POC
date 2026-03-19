# agents.md — Energy Project Preparation PoC

## Project Overview

Energy project preparation PoC focused on action selection, site selection, and technology selection at pre-feasibility scope. This repo provides documentation, reference data, analysis scripts, and AI agent tooling. The application UI lives in the [Geo-Layer-Viewer](https://github.com/joaquinOEF/Geo-Layer-Viewer) repo.

**Target city**: Porto Alegre, Brazil (BR POA)
**Scope**: Pre-feasibility / concept-note — use ranges, archetypes, and "good enough" defaults, not full engineering design.

## Architecture Rules

- This repo does NOT contain application code — the app is Geo-Layer-Viewer
- `context/` holds baseline context organized by dimension (geographic, technology, financing, regulatory, projects) — always consult before analysis
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
| CityCatalyst Global API | `analysis/shared/global_api_client.py` | City emissions data, metadata, CCGlobal energy actions |
| OEF S3 Tile Catalog | via Geo-Layer-Viewer proxy | Raster tile access |
| Anthropic API | `agent/orchestrator.py` | LLM calls for agent prompts (requires ANTHROPIC_API_KEY) |

## Analysis Pipeline

The analysis flows through three stages, each with its own scripts and schema:

```
1. Action Selection (analysis/action-selection/)
   ├── context_signals.py — Extract geographic, regulatory, financing signals from context
   ├── ccglobal_extract.py — Normalize CCGlobal energy actions into catalog format
   ├── action_scoring.py — Multi-criteria scoring (6 criteria, weighted)
   └── run_action_selection.py — Orchestrate full pipeline, output JSON
        │
        ▼
2. Site Selection (analysis/site-selection/)
   ├── candidate_zones.py — Identify candidate zones from geo layers
   ├── constraint_filter.py — Apply hard/soft constraints from site-constraint-types.json
   └── site_scoring.py — Score and rank zones using scoring-weights.json
        │
        ▼
3. Technology Selection (analysis/technology-selection/)
   ├── tech_matching.py — Match tech archetypes to site characteristics
   └── sizing_estimates.py — Pre-feasibility capacity and cost ranges
```

### Action Selection Scoring Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Context Alignment | 0.25 | How well action addresses identified problems and matches supportive signals |
| Existing Commitment Alignment | 0.20 | Action aligns with city/state plans (PLAC, TEJ, etc.) |
| Impact Potential | 0.20 | Emissions reduction + co-benefits (resilience, equity, cost savings) |
| Financing Readiness | 0.15 | Funder priorities match, financing archetypes available |
| Implementation Readiness | 0.10 | Prerequisites achievable, technology proven, timeline feasible |
| Portfolio Synergy | 0.10 | Action complements other high-scoring actions |

### Recommendation Tiers

- **priority** (score >= 70): Include in primary action portfolio
- **include** (score >= 55): Complementary actions that strengthen the portfolio
- **conditional** (score >= 40): Include if specific conditions are met
- **defer** (score < 40): Not recommended at this stage

## Agent Roles

### 1. Research Agent

**Purpose**: Gather, synthesize, and store research on energy topics
**Scope**: Web search, literature review, benchmark collection, policy analysis

**Rules**:
- Store structured findings (JSON with provenance) in `data/research/`
- Store analytical documents and reports in the appropriate `context/` subdirectory:
  - Geographic/spatial context → `context/geographic/<scale>/`
  - Technology landscape → `context/technology/`
  - Funder preferences, past approvals → `context/financing/`
  - Policy and regulatory → `context/regulatory/`
  - Reference projects → `context/projects/`
- Always include source URLs, retrieval dates, and confidence notes
- Never overwrite existing research — append with timestamps
- Use `agent/prompts/research-synthesis.md` as the base prompt
- Tag each finding with relevant component (`action-selection` / `site-selection` / `technology-selection`)

### 2. Action Analysis Agent

**Purpose**: Evaluate and select energy actions for the city's project portfolio
**Scope**: Context signal extraction, action scoring, portfolio construction

**Rules**:
- Use `analysis/action-selection/context_signals.py` to extract signals from context
- Reference `data/energy-action-catalog.json` for local action archetypes
- Integrate CCGlobal actions via `analysis/action-selection/ccglobal_extract.py`
- Update context signals when new context documents are added
- Output must conform to `schemas/action-selection.json`
- Use `agent/prompts/action-analysis.md` as the base prompt

### 3. Site Analysis Agent

**Purpose**: Analyze geospatial data to identify and score candidate sites
**Scope**: Query Geo-Layer-Viewer layers, apply constraints, run scoring

**Rules**:
- Use `analysis/shared/geo_client.py` to access geo data — never call APIs directly
- Reference `data/layers-energy-mapping.json` for layer relevance
- Apply constraints from `data/site-constraint-types.json`
- Use scoring weights from `data/scoring-weights.json`
- Output must conform to `schemas/site-selection.json`
- Use `agent/prompts/site-analysis.md` and `agent/prompts/constraint-check.md` as base prompts

### 4. Technology Agent

**Purpose**: Recommend and size energy technologies for selected sites
**Scope**: Match tech to site, estimate sizing, assess feasibility

**Rules**:
- Reference `data/energy-tech-catalog.json` for technology archetypes
- Use pre-feasibility ranges, not engineering precision
- Cross-reference site constraints (e.g., roof area limits rooftop PV capacity)
- Reference `data/financing-archetypes.json` for financing compatibility
- Output must conform to `schemas/technology-selection.json`
- Use `agent/prompts/tech-recommendation.md` as the base prompt

### 5. Output Agent

**Purpose**: Generate structured deliverables from analysis results
**Scope**: Site summaries, tech shortlists, concept briefs

**Rules**:
- Use templates in `outputs/templates/` as structure (site-summary.md, tech-shortlist.md, concept-brief.md)
- Use generators in `outputs/generators/` to populate templates programmatically
- Cite data sources and analysis provenance
- Keep outputs concise — concept-note scope, not full PDD
- Generated outputs go to `outputs/examples/` for review
- Use `agent/prompts/concept-brief.md` as the base prompt

### 6. Review Agent

**Purpose**: Review changes, validate data quality, check consistency

**Rules**:
- Verify JSON data files parse correctly and match their schemas
- Check that analysis scripts handle missing data gracefully
- Ensure prompt templates haven't changed without changelog entry
- Flag scoring weight changes (they affect all site rankings)
- Verify `geo_client.py` calls match current Geo-Layer-Viewer API endpoints
- Validate that context signals in `context_signals.py` stay consistent with context documents

## Agent Orchestration

The agent orchestrator (`agent/orchestrator.py`) manages prompt loading and context preparation:

1. Loads a prompt template from `agent/prompts/` and substitutes variables (e.g., `{{city_name}}`)
2. Gathers project context via `analysis/shared/data_loader.py` (tech catalog, constraints, scoring weights, layer mapping, research)
3. Calls the LLM (configurable via `LLM_MODEL` env var, defaults to `claude-sonnet-4-6`)
4. Returns structured response with proposed patches

Patches (`agent/patches.py`) follow a human-in-the-loop workflow:
- Agent creates patches with `create_patch()` (target component, field path, value, rationale, confidence, sources)
- Human reviews and sets status to `accepted` / `rejected`
- Accepted patches are applied via `apply_patch()` using dot-path navigation

## Shared Types

Core dataclasses are defined in `analysis/shared/types.py`:

| Type | Purpose |
|------|---------|
| `SiteCharacteristics` | Zone properties: area, solar GHI/DNI/PVOUT, flood risk, built-up density, population density |
| `ConstraintResult` | Constraint evaluation: passed/failed, severity (hard/soft), penalty |
| `ScoredZone` | Ranked zone with composite score, breakdown, constraint flags |
| `TechnologyMatch` | Tech recommendation: feasibility score, capacity/output/CAPEX/LCOE ranges |
| `Patch` | Agent suggestion: target component/field, proposed value, rationale, confidence, status |
| `Range` | Min/max with unit |
| `GeoPoint` / `GeoBounds` | Coordinate types |
| `LayerValue` | Value from a geo layer |

Enums: `ConstraintSeverity` (hard/soft), `TechnologyCategory` (solar_pv, battery_storage, grid_upgrade, efficiency, distributed_generation, hybrid), `FloodRisk`, `BuiltUpDensity`

## File Conventions

| Type | Location | Format |
|------|----------|--------|
| Context docs | `context/<dimension>/<topic>.md` | Markdown, PDFs, YAML |
| Reference data | `data/*.json` | Flat JSON, git-versioned, human-editable |
| Research | `data/research/<category>/<topic>.json` | Structured JSON with provenance |
| Analysis scripts | `analysis/<component>/<script>.py` | Python |
| Shared clients | `analysis/shared/*.py` | Python |
| Prompts | `agent/prompts/*.md` | Markdown, auditable |
| Agent core | `agent/*.py` | Python (orchestrator, patches) |
| Tool definitions | `agent/tools/*.py` | Python |
| Schemas | `schemas/*.json` | JSON Schema |
| Output templates | `outputs/templates/*.md` | Markdown |
| Output generators | `outputs/generators/*.py` | Python |
| Generated outputs | `outputs/examples/*.md` | Markdown |
| Methodology docs | `docs/methodology/*.md` | Markdown |
| Architecture docs | `docs/*.md` | Markdown |
| Policy research | `grid_policy/*.md` | Markdown |
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
