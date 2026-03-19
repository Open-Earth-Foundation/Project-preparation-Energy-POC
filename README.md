# Energy Project Preparation PoC

Energy project preparation tool focused on **site selection** and **technology selection** at pre-feasibility / concept-note scope. Part of the [CityCatalyst](https://github.com/Open-Earth-Foundation/CityCatalyst) ecosystem by [Open Earth Foundation](https://openearth.org).

## Scope

This PoC helps cities move from prioritized climate actions to finance-ready energy project concepts. It operates at pre-feasibility scope: ranges, archetypes, checklists, and "good enough" defaults — not full engineering design.

**Current focus**: Porto Alegre, Brazil (BR POA)

### Components

1. **Site Selection** — Identify and score candidate zones using geospatial data, constraints, and multi-criteria analysis
2. **Technology Selection** — Match energy technologies (solar PV, storage, grid upgrades, efficiency bundles, distributed generation) to site characteristics

## Architecture

This repo is the **energy domain brain** — documentation, reference data, analysis scripts, and AI agent tooling. The application UI lives in the [Geo-Layer-Viewer](https://github.com/joaquinOEF/Geo-Layer-Viewer) repo.

```
┌──────────────────────────────┐     ┌────────────────────────────────┐
│  Geo-Layer-Viewer (app)      │     │  This repo (energy domain)     │
│                              │     │                                │
│  React + Leaflet map         │     │  docs/      methodology        │
│  66+ geospatial layers       │◄────│  data/      reference data     │
│  Raster decode + spatial     │     │  analysis/  scoring scripts    │
│  Express API                 │     │  agent/     AI prompts+tools   │
│                              │     │  outputs/   report generators  │
└──────────┬───────────────────┘     └──────────┬─────────────────────┘
           │                                    │
           ▼                                    ▼
  ┌─────────────────────┐           ┌─────────────────────┐
  │ OEF S3 Tile Catalog │           │ CityCatalyst Global  │
  │ OSM / IBGE / GTFS   │           │ API (emissions)      │
  └─────────────────────┘           └─────────────────────┘
```

## Repo Structure

```
city_data/             City-specific documents (PLAC climate action plan)
docs/                  Architecture, methodology, data source catalog
data/                  Reference data (JSON) + curated research
  research/            Benchmarks, policies, case studies
analysis/              Python analysis scripts
  site-selection/      Candidate zones, constraint filtering, scoring
  technology-selection/ Tech matching, sizing estimates
  shared/              API clients (Geo-Layer-Viewer, Global API), data loaders
agent/                 AI agent integration
  prompts/             Versioned prompt templates
  tools/               Agent tool definitions
outputs/               Report templates and generators
schemas/               JSON Schema contracts for all structured data
tests/                 Python tests
```

## Setup

```bash
# Clone
git clone https://github.com/Open-Earth-Foundation/Project-preparation-Energy-POC.git
cd Project-preparation-Energy-POC

# Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Edit .env with your API URLs and keys

# Run tests
pytest tests/
```

## External Dependencies

| Service | Purpose | Required |
|---------|---------|----------|
| [Geo-Layer-Viewer](https://github.com/joaquinOEF/Geo-Layer-Viewer) | Geospatial layers, raster values, spatial queries | Yes |
| [CityCatalyst Global API](https://github.com/Open-Earth-Foundation/CityCatalyst-global-data) | City emissions data, metadata | Yes |
| [Climate TRACE](https://climatetrace.org) | Facility-level emissions | Optional |

## License

MIT
