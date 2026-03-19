# Site Selection Methodology

## Overview

Identify and rank candidate zones for energy infrastructure within a city boundary using multi-criteria geospatial analysis.

## Process

### 1. Define Study Area
- Fetch city boundary from Geo-Layer-Viewer (`/api/geospatial/boundary`)
- Optionally focus on specific neighbourhoods or districts

### 2. Generate Analysis Grid
- Divide study area into grid cells (e.g., 500m x 500m)
- Or use existing administrative boundaries (neighbourhoods, census tracts)

### 3. Apply Hard Constraints (Exclusion)
Filter out zones that fail hard constraints (see `data/site-constraint-types.json`):
- High flood risk (FRI >= 0.7)
- Protected areas / forests / wetlands
- Permanent water bodies
- Insufficient solar resource (GHI < 1200 kWh/m2/year for solar)
- Very dense urban areas (for ground-mount only)

### 4. Score Remaining Zones
Apply weighted scoring using criteria from `data/scoring-weights.json`:

| Criterion | Weight | Layer | Direction |
|-----------|--------|-------|-----------|
| Solar resource (PVOUT) | 0.25 | solar-neighbourhoods | Higher = better |
| Flood risk | 0.15 | flood-risk-index | Lower = better |
| Land availability | 0.20 | dynamic-world | More suitable classes = better |
| Grid proximity | 0.15 | viirs-night-lights | Higher = better |
| Population density | 0.15 | ghsl-population | Higher = more beneficiaries |
| Social vulnerability | 0.10 | ibge-indicators | Higher poverty = more need |

### 5. Apply Soft Constraint Penalties
Subtract penalty points for soft constraints:
- Moderate flood risk: -20 points
- Steep slope: -15 points

### 6. Rank and Output
- Sort zones by final score (0-100)
- Output top N candidate zones with score breakdown
- Flag any soft constraints triggered

## Normalization

All layer values are normalized to 0-1 range before applying weights:
```
normalized = (value - min) / (max - min)
```
Min/max values are defined in `data/scoring-weights.json`.

## Limitations

- Pre-feasibility scope: grid-level analysis, not parcel-level
- Proxy indicators (e.g., night lights for grid proximity) are approximations
- Scoring weights are defaults — should be adjusted per project context
- Does not account for land ownership, permitting, or community acceptance
