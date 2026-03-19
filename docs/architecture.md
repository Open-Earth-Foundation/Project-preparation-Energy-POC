# Architecture

## Overview

This repo is the **energy domain layer** for the Energy Project Preparation PoC. It does not contain application code — the UI and geospatial platform live in the [Geo-Layer-Viewer](https://github.com/joaquinOEF/Geo-Layer-Viewer) repo.

## System Components

### Geo-Layer-Viewer (external)
- React + Leaflet interactive map with 66+ geospatial data layers
- Express API serving layer data from OEF S3 catalog, OSM, IBGE, GTFS
- Raster tile decoding (RGB-encoded value tiles for climate indices)
- Spatial query engine (vector x raster intersections)
- Target city: Porto Alegre, Brazil

### This Repo
- **Reference data** (`data/`): Technology catalog, constraint definitions, scoring weights, layer-to-energy mapping
- **Research store** (`data/research/`): Curated benchmarks, policies, case studies — both human-curated and agent-generated
- **Analysis scripts** (`analysis/`): Python scripts for site scoring, tech matching, sizing estimates
- **Agent tooling** (`agent/`): Prompt templates and tool definitions for AI-assisted analysis
- **Output generators** (`outputs/`): Templates and scripts to produce site summaries, tech shortlists, concept briefs
- **Schemas** (`schemas/`): JSON Schema contracts for all structured data

### CityCatalyst Global API (external)
- City emissions data by GPC sector
- City metadata and boundaries
- Endpoint: `https://ccglobal.openearth.dev`

## Data Flow

```
1. Geo-Layer-Viewer provides geospatial layer data via Express API
        │
        ▼
2. analysis/shared/geo_client.py fetches layer values for candidate zones
        │
        ▼
3. analysis/site-selection/ applies constraints + scoring from data/*.json
        │
        ▼
4. Ranked candidate zones feed into technology matching
        │
        ▼
5. analysis/technology-selection/ matches tech archetypes from energy-tech-catalog.json
        │
        ▼
6. outputs/generators/ produce site summary, tech shortlist, concept brief
```

## Agent Integration

AI agents operate in human-in-the-loop mode:
1. Agent reads project context + geo data
2. Agent proposes structured patches (see `schemas/patch.json`)
3. Human reviews and accepts/modifies/rejects each patch
4. Accepted patches update project context

Prompt templates are stored in `agent/prompts/` and versioned in git for auditability.

## Key Design Decisions

1. **JSON-first reference data**: Easy to edit, review in PRs, and version. DB-backed later if needed.
2. **Layer mapping indirection**: `data/layers-energy-mapping.json` decouples this repo from Geo-Layer-Viewer layer IDs.
3. **Pre-feasibility scope**: All estimates use ranges and archetypes, never single-point engineering values.
4. **Schema contracts**: Every structured output has a JSON Schema so agents and scripts produce consistent data.
