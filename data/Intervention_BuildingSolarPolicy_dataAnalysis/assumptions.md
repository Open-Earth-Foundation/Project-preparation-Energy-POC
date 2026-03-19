# Intervention Design Assumptions — Building Solar Mandate Policy

**Intervention:** Solar Mandate Policies for Residential and Commercial Buildings
**Parent Action:** POA-E-06 — Sustainable Buildings (Private Sector Leverage)
**C40 HIA:** 14 — Renewable Energy Mandates for Buildings
**City:** Porto Alegre (BR POA)
**Date:** 2026-03-19

---

## Purpose

This document records the assumptions made when identifying geospatial datasets needed to design the solar mandate policy intervention described in `analysis/action-selection/intervention_solar-mandate-residential-commercial.md`. These assumptions drive the data requirements in the accompanying CSV.

---

## Intervention Design Assumptions

### A1 — The policy applies citywide but with spatially differentiated rules

The solar mandate is not a blanket requirement. The building code update (Sub-action 6.4) and IPTU Sustentável incentive (Sub-action 6.6) will need **zoning-aware thresholds** — for example, stricter mandates in high-solar-resource zones and larger incentives in low-income areas. This means the policy design requires spatial data to define where different rules apply and at what intensity.

### A2 — Residential and commercial segments require separate spatial targeting

The intervention document defines two building segments with different targets (8% residential vs. 10% commercial by 2030), different system sizes (3–5 kWp vs. 20–200 kWp), and different policy levers (tax incentive vs. code mandate). Designing these requires data to **spatially distinguish residential from commercial building stock**, which drives the need for building footprint and land-use classification data.

### A3 — Equity-weighted incentive design is a core requirement

The intervention document explicitly states: "Target IPTU incentives to low-income neighborhoods using br_ibge census data." This means the IPTU Sustentável program will spatially modulate incentive levels based on socioeconomic indicators. Designing this requires granular income, housing quality, and social vulnerability data at the neighborhood or census-tract level.

### A4 — Rooftop solar feasibility must be assessed at building scale

Since this is a rooftop-mounted distributed generation policy (not ground-mount solar farms), the technical feasibility assessment requires **building-level or block-level data**: roof area, roof orientation/tilt, shading from adjacent structures, and structural capacity proxies. The geospatial-data repo provides built-up density at 100m resolution (GHSL), which is useful for aggregate estimation but insufficient for building-level mandate design.

### A5 — Grid hosting capacity determines where mandates are technically feasible

A solar mandate that exceeds local grid hosting capacity creates curtailment and safety issues. The policy design must identify **grid-constrained zones** where mandates should be phased or accompanied by storage requirements. This requires distribution grid topology data (substation locations, feeder capacity) that goes beyond the night-lights proxy available in the geospatial-data repo.

### A6 — Existing solar adoption informs where to focus new mandates

Areas with high existing distributed generation penetration need different policy treatment than areas with near-zero adoption. ANEEL's distributed generation registry provides installation-level data that can be geocoded. This helps avoid mandating what is already happening and focus incentives where adoption is lagging.

### A7 — New construction vs. retrofit requires different spatial data

The building code update (Sub-action 6.4) applies to **new construction**, so the policy needs to know where new development is planned or permitted. The IPTU Sustentável incentive drives **retrofits on existing buildings**, so it needs data on the existing building stock, age, and condition. These are distinct spatial datasets.

### A8 — Flood and climate risk affect long-term system viability

Solar PV systems have 25-year lifespans. The policy should not mandate installations in areas with high flood risk or extreme climate exposure without requiring resilience measures. Flood risk projections (2030s, 2050s) from the geospatial-data repo are relevant for long-term policy design.

### A9 — Heritage and architectural protection constrains mandate scope

Porto Alegre has historic districts and protected buildings where solar panel installation may be restricted or require special permits. The policy must exclude or create special provisions for heritage zones. This requires data on listed buildings and historic preservation areas from IPHAE (state) and IPHAN (federal).

### A10 — Solar resource variation within the city affects mandate stringency

While Porto Alegre has good overall solar resource (GHI 1,500–1,700 kWh/m²/yr), there is meaningful intra-city variation due to topography, urban shading, and microclimate. The policy should calibrate minimum system sizes and performance expectations by zone. The Global Solar Atlas data in the geospatial-data repo provides this at ~1km resolution.

### A11 — The municipal zoning plan (PDDUA) defines what can be mandated where

Porto Alegre's Plano Diretor de Desenvolvimento Urbano Ambiental (PDDUA) defines land-use zones, building height limits, and floor-area ratios. The solar mandate must be consistent with these zoning rules — for example, building code requirements can only apply in zones that permit the relevant building types. The PDDUA spatial data is essential but not in the geospatial-data repo.

### A12 — Electricity consumption patterns inform incentive calibration

The IPTU Sustentável incentive and payback calculations depend on local electricity consumption levels. Areas with higher consumption per building have faster payback and need less incentive. Spatially resolved consumption data (from the utility CEEE Equatorial or ANEEL) helps calibrate incentive levels.

### A13 — Temperature extremes affect PV performance derating

The intervention's energy yield estimates (1,405 kWh/kWp/year) are based on average conditions. In areas with higher temperature extremes, PV panel efficiency drops (typically 0.3–0.5%/°C above 25°C). ERA5 temperature data from the geospatial-data repo enables spatially differentiated performance expectations.

---

## Summary of Data Categories

| Category | Policy Design Purpose |
|----------|----------------------|
| Solar resource | Mandate stringency calibration by zone |
| Building stock | Identify eligible buildings, estimate rooftop area |
| Land use / zoning | Define where mandates apply, segment residential vs. commercial |
| Socioeconomic | Equity-weighted incentive design (IPTU Sustentável) |
| Grid infrastructure | Identify hosting capacity constraints |
| Climate / hazard risk | Long-term viability and resilience requirements |
| Existing solar adoption | Avoid redundant mandates, target lagging areas |
| New construction permits | Target building code update to growth areas |
| Heritage / protected sites | Exclude or create special provisions |
| Electricity consumption | Calibrate incentive levels for payback |
