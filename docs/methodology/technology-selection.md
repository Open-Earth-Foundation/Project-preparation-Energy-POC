# Technology Selection Methodology

## Overview

Match energy technology archetypes to candidate site characteristics and estimate pre-feasibility sizing ranges.

## Process

### 1. Characterize Site
Extract from site selection outputs and geo layer data:
- Solar resource (GHI, DNI, PVOUT)
- Available area (from land cover analysis)
- Land cover type (built-up, barren, grassland, etc.)
- Built-up density (rural → dense urban)
- Flood risk level
- Grid proximity (night lights proxy)
- Population density
- Existing infrastructure (schools, hospitals, transit)

### 2. Filter Applicable Technologies
From `data/energy-tech-catalog.json`, filter technologies by site requirements:
- Solar PV (ground): needs open land, min GHI, low flood risk
- Solar PV (rooftop): needs built-up area, min GHI
- Battery storage: needs low flood risk, grid connection
- Grid upgrade: needs existing grid infrastructure
- Efficiency bundle: needs existing buildings
- Distributed micro-gen: suitable for underserved/peri-urban areas

### 3. Score Technologies
For each applicable technology, score on:

| Criterion | Weight | Source |
|-----------|--------|--------|
| Site match | 0.30 | How well site characteristics match tech requirements |
| Cost effectiveness | 0.25 | LCOE range vs local tariff |
| Implementation readiness | 0.20 | Regulatory framework, local capacity |
| Impact potential | 0.15 | Emissions reduction, beneficiary reach |
| Risk profile | 0.10 | Technical, regulatory, financial risks |

### 4. Estimate Sizing Ranges
For shortlisted technologies, produce pre-feasibility ranges:
- **Capacity**: min-max range based on available area and tech parameters
- **Output**: estimated annual production based on capacity factor ranges
- **Area required**: space needs at min and max capacity
- **Cost**: CAPEX and LCOE ranges from tech catalog

### 5. Identify Financing Fit
Cross-reference with `data/financing-archetypes.json` to flag which financing mechanisms are suitable for each technology option.

## Example: Solar PV Ground-Mount

```
Site: neighbourhood with 50,000 m2 suitable land, GHI 1650 kWh/m2/year
Tech: solar-pv-ground

Capacity range:
  min: 50,000 / 20,000 = 2.5 MWp (conservative area/MW)
  max: 50,000 / 10,000 = 5.0 MWp (efficient area/MW)

Output range:
  min: 2,500 kW * 1,314 h (CF 0.15) = 3,285 MWh/year
  max: 5,000 kW * 1,752 h (CF 0.20) = 8,760 MWh/year

CAPEX range:
  min: 2,500 * $700 = $1.75M
  max: 5,000 * $1,200 = $6.0M
```

## Limitations

- Uses archetype parameters, not vendor-specific data
- Sizing is indicative only — full feasibility requires engineering studies
- Cost data is regional averages, not site-specific quotes
- Does not account for interconnection costs, land acquisition, or permitting
