# Site & Technology Selection UI — MVP PRD + Implementation Prompts

**Project:** Energy Project Preparation Module — Porto Alegre Solar PV
**Target repo:** Geo-Layer-Viewer (github.com/joaquinOEF/Geo-Layer-Viewer)
**Scope:** MVP, ~2 hours build time

---

## Overview

A city user (Porto Alegre municipal staff) needs to act on two solar PV interventions. This UI surfaces the right geospatial data and lets them make decisions — no backend, client-side state only.

**Two interventions:**
1. **Municipal Solar Portfolio** — Select a priority scope for rooftop solar on city-owned buildings (POA-E-07)
2. **Building Solar Regulation** — IPTU Sustentável incentive design for commercial buildings, with geospatial assessment and scenario modeling (POA-E-06)

**User persona:** City planner who controls municipal buildings and can design policy. Not a GIS expert.

---

## Intervention 1 — Municipal Solar Portfolio

### What it is
Porto Alegre has ~500 schools + ~60 municipal buildings eligible for rooftop solar. The city needs to decide which buildings to prioritize for the first phase.

### Key metrics (from PLAC POA-E-07)
- Total portfolio: 37 MWp, R$166.5M investment, R$41.6M/year savings, 6,759 tCO2e/year avoided, 4-year payback
- Solar resource: 1,405 kWh/kWp/year (GHI 1,500–1,700 kWh/m²/yr)
- CAPEX benchmark: R$4,500/kWp

### Priority tiers
| Tier | Buildings | Description |
|------|-----------|-------------|
| **High** | Top 20% by score | Largest rooftops, highest solar resource, lowest flood risk |
| **Medium** | Next 40% | Good potential, moderate constraints |
| **Low** | Remaining 40% | Lower return, include for full city coverage |
| All three = full portfolio |

### Building score criteria (from `data/scoring-weights.json`)
Solar resource (25%) + Land availability (20%) + Flood risk (15%) + Grid proximity (15%) + Population density (15%) + Social vulnerability (10%)

### Building data model
```typescript
interface MunicipalBuilding {
  id: string
  name: string              // e.g. "EMEF João Pessoa"
  type: "school" | "facility"
  lat: number
  lng: number
  score: number             // 0–100
  priorityTier: "high" | "medium" | "low"
  roofAreaM2: number
  capacityKwp: number
  annualGenerationMwh: number
  capexBrl: number
  annualSavingsBrl: number
  paybackYears: number
  co2AvoidedTonsPerYear: number
  solarGhi: number          // kWh/m²/year
  floodRisk: "low" | "moderate" | "high"
  neighborhood: string
}
```

### UX Flow
1. User opens "Municipal Solar Portfolio" intervention card
2. Side panel opens with 3 tabs: **High Priority** / **Medium** / **Low**
3. Map highlights buildings color-coded by selected tier(s)
4. Each tab shows: building list + aggregate summary cards (total capacity, investment, savings, CO2)
5. Clicking a building on map or list opens a detail card (name, score, capacity, savings, payback)
6. "Select this scope" button confirms the tier selection

---

## Intervention 2 — Building Solar Regulation

### What it is
The city is designing solar regulation for buildings via three policy instruments: IPTU Sustentável (property tax incentive), Building Certification, and Building Code update. The MVP focuses on IPTU Sustentável for **commercial buildings only** — the city wants to identify which neighborhoods offer the best trade-off between solar energy potential and IPTU revenue forfeited.

### Key metrics (from PLAC POA-E-06)
- Target: 146.2 MWp by 2030 (10% commercial buildings)
- Leverage: R$1 govt → R$110 private investment
- 26,702 tCO2e/year avoided, R$9/tCO2e govt cost
- Commercial: 20–200 kWp/building

### Policy instruments (landing page)
| Instrument | Status | Description |
|-----------|--------|-------------|
| **IPTU Sustentável** | Active (clickable) | Property tax discount to incentivize commercial solar PV |
| **Building Certification** | Coming soon (disabled) | Sustainability certification requirements |
| **Building Code** | Coming soon (disabled) | Mandatory solar in new construction |

### IPTU Sustentável — 3 tabs

#### Tab 1: Geospatial Assessment

**Map visualization:**
- City divided by neighborhoods/zones, color-coded into 3 tiers:
  - **High potential** (green) — highest energy creation potential + lowest current IPTU revenue → best ROI for the city
  - **Medium potential** (amber) — moderate cross-score
  - **Low potential** (gray) — low energy potential or high IPTU revenue at stake
- **Commercial buildings** shown as interactive markers within each neighborhood
- **Residential buildings** shown as grayed-out, non-clickable markers (visible for context but not actionable)

**Cross-analysis logic:**
The priority ranking combines two factors:
1. **Solar energy potential** of commercial buildings in the neighborhood (kWp based on solar exposure + building footprints)
2. **Current IPTU revenue** from commercial buildings in the neighborhood (R$/year)

Best neighborhoods = high solar potential + low IPTU revenue (city forfeits less revenue for more energy impact).

**Neighborhood detail card** (shown when clicking a neighborhood):
- Neighborhood name and tier badge
- Number of commercial buildings
- Total solar energy potential (kWp) based on solar exposure and building footprints
- Current annual IPTU revenue from commercial buildings (R$/year)
- **Scenario A — 5% IPTU discount:**
  - Revenue lost per year (R$)
  - Estimated PV capacity installed (kWp) — based on assumed adoption rate from the incentive
  - Estimated annual energy generation (MWh/year)
  - CO2 avoided (tCO2e/year)
- **Scenario B — 10% IPTU discount:**
  - Revenue lost per year (R$)
  - Estimated PV capacity installed (kWp) — higher adoption rate assumed
  - Estimated annual energy generation (MWh/year)
  - CO2 avoided (tCO2e/year)

#### Tab 2: Similar Projects

A list of reference projects from other cities/states that implemented IPTU-based solar incentives:
- Each entry shows: city/state name, program name, brief summary of results and learnings (2–3 sentences), and a "Learn more" link
- Mock data for MVP (3–4 examples from Brazilian cities that have IPTU Verde/Sustentável programs)

#### Tab 3: Next Steps

**Primary next step — Grid capacity assessment:**
- Prominent card explaining that the selected high-potential neighborhoods need grid capacity validation before implementation
- Suggested approach: "Request a joint technical assessment with [local energy distributor — CEEE Equatorial] to evaluate feeder capacity, transformer headroom, and interconnection requirements for the priority neighborhoods"
- Action items: schedule meeting, share neighborhood list, request capacity data per feeder

**Other pending data to collect:**
- Updated commercial building registry with roof area measurements
- Current IPTU billing records by neighborhood (to validate revenue estimates)
- Historical solar permit data (existing PV installations in commercial buildings)
- Heritage/preservation zone boundaries (some neighborhoods may have restrictions)
- Flood risk overlay for long-term PV investment viability

---

## Dashboard / Landing

A simple landing view before either intervention:

- **Header:** "Porto Alegre — Solar PV Interventions"
- **Two cards side by side:**
  - Card 1: Municipal Solar Portfolio — shows key metrics (37 MWp, 560 buildings, R$41.6M/yr savings, 6,759 tCO2e/yr)
  - Card 2: Building Solar Regulation — shows key metrics (146.2 MWp target, 1:110 leverage ratio, 26,702 tCO2e/yr)
- Clicking a card opens the respective intervention panel

---

## Implementation Prompts

Use these prompts sequentially in the Geo-Layer-Viewer repo.

---

### Prompt 1 — Intervention Dashboard + Municipal Solar Portfolio

```
Create a Solar PV Intervention module in this React/TypeScript/Leaflet app.

## What to build

### 1. Intervention Dashboard (new route `/interventions` or as a new right-side panel)
Two clickable cards:
- "Municipal Solar Portfolio" — 37 MWp | 560 buildings | R$41.6M/yr savings | 6,759 tCO2e/yr avoided
- "Building Solar Regulation" — 146.2 MWp target | 1:110 leverage | 26,702 tCO2e/yr avoided

Style: dark theme (bg-background), brand color #001fa8. Use shadcn Card components.

### 2. Municipal Solar Portfolio side panel (Sheet from shadcn, right side)
When the first card is clicked, open a side panel with:

**Header:** "Municipal Solar Portfolio" with a close button

**3 tabs** (shadcn Tabs): "High Priority" / "Medium" / "Low"
- High = top 20% scored buildings (~112 buildings)
- Medium = next 40% (~224 buildings)
- Low = remaining 40% (~224 buildings)

**Summary cards** at top of each tab (4 metrics in a 2x2 grid):
- Total capacity (MWp)
- Total investment (R$ M)
- Annual savings (R$ M/yr)
- CO2 avoided (tCO2e/yr)

**Building list** below summary: scrollable list of buildings. Each row:
- Building name + type icon (school/facility)
- Score badge (0–100, color-coded: green >70, yellow 50–70, red <50)
- Capacity (kWp) and annual savings (R$/yr)
- Clicking a row selects the building

**Map interaction:**
- When a tab is selected, highlight buildings on the map:
  - High = blue markers (#001fa8)
  - Medium = amber markers
  - Low = gray markers
- Clicking a map marker selects the building and scrolls the list to it

**Building detail card** (appears at bottom of panel when a building is selected):
- Name, neighborhood, type
- Score, capacity (kWp), roof area (m²)
- Annual generation (MWh), annual savings (R$), payback (years), CO2 avoided (tCO2e/yr)
- Solar GHI (kWh/m²/yr), flood risk badge

**"Select this scope" button** at panel bottom:
- Confirms the currently active tab as the selected portfolio scope
- Shows a toast: "High Priority scope selected — 112 buildings, 7.4 MWp"

## Data
Seed with mock data matching this TypeScript interface:
```typescript
interface MunicipalBuilding {
  id: string
  name: string
  type: "school" | "facility"
  lat: number
  lng: number
  score: number
  priorityTier: "high" | "medium" | "low"
  roofAreaM2: number
  capacityKwp: number
  annualGenerationMwh: number
  capexBrl: number
  annualSavingsBrl: number
  paybackYears: number
  co2AvoidedTonsPerYear: number
  solarGhi: number
  floodRisk: "low" | "moderate" | "high"
  neighborhood: string
}
```
Generate 20 realistic sample buildings across Porto Alegre (lat ~-30.03, lng ~-51.23) spread across tiers. Use realistic Porto Alegre neighborhood names (Moinhos de Vento, Bom Fim, Petrópolis, etc.). Capacity range: schools 30–80 kWp, facilities 100–300 kWp.

## Tech notes
- Use shadcn Sheet, Tabs, Card, Badge, ScrollArea, Button, Separator
- State: React useState (client-side only, no DB)
- Map: Leaflet CircleMarker for buildings, color by tier
- Keep component in client/src/components/interventions/MunicipalSolarPanel.tsx
```

---

### Prompt 2 — Building Solar Regulation (IPTU Sustentável)

```
Add the second intervention: Building Solar Regulation with IPTU Sustentável focus.

## What to build

A side panel (shadcn Sheet, right side) that opens when "Building Solar Regulation" card is clicked.

### Landing: 3 policy instrument buttons
Show 3 buttons/cards stacked vertically:
1. **"IPTU Sustentável"** — clickable, styled as primary action. Subtitle: "Property tax discount for commercial solar PV"
2. **"Building Certification"** — disabled/grayed out with a "Coming soon" badge
3. **"Building Code"** — disabled/grayed out with a "Coming soon" badge

When "IPTU Sustentável" is clicked, show 3 tabs below:

### Tab 1: Geospatial Assessment

**Map visualization:**
- Divide the city map by neighborhoods/zones into 3 tiers, color-coded:
  - High potential = green
  - Medium potential = amber
  - Low potential = gray
- The tier ranking is a cross-analysis: **highest solar energy potential on commercial buildings** × **lowest current IPTU revenue** from those buildings. Best = high energy + low revenue (city forfeits less for more impact).
- Show **commercial buildings** as interactive colored markers (match neighborhood tier color)
- Show **residential buildings** as grayed-out, non-clickable markers (visible for spatial context but not actionable). Add a legend note: "Residential — not in scope"

**Neighborhood detail card** (opens when clicking a neighborhood polygon or any commercial building in it):
- Neighborhood name + tier badge (High/Medium/Low)
- Number of commercial buildings
- Total solar energy potential (kWp) — based on solar exposure + building footprints
- Current annual IPTU revenue from commercial buildings (R$/year)
- **Two scenario cards side by side:**

  **Scenario A — 5% IPTU Discount:**
  | Metric | Value |
  |--------|-------|
  | Revenue lost/year | R$ [calculated] |
  | Estimated PV installed | [X] kWp |
  | Annual generation | [X] MWh/year |
  | CO2 avoided | [X] tCO2e/year |

  **Scenario B — 10% IPTU Discount:**
  | Metric | Value |
  |--------|-------|
  | Revenue lost/year | R$ [calculated] |
  | Estimated PV installed | [X] kWp |
  | Annual generation | [X] MWh/year |
  | CO2 avoided | [X] tCO2e/year |

  Assumptions for mock data:
  - 5% discount → ~15% adoption rate among commercial buildings
  - 10% discount → ~30% adoption rate
  - Average commercial system: 50 kWp
  - 1,405 kWh/kWp/year generation
  - 0.183 tCO2/MWh grid emission factor

### Tab 2: Similar Projects

A scrollable list of 4 reference projects:

1. **Salvador, BA — IPTU Verde** — Since 2015, property tax discounts up to 10% for buildings with sustainability features including solar. Over 500 commercial properties enrolled. Key learning: adoption accelerated when combined with simplified permitting.
   - Link: "Learn more →"

2. **Guarulhos, SP — IPTU Verde** — Offers 5–20% IPTU discount for green buildings. Commercial uptake higher than residential due to faster payback. Key learning: larger buildings (>500m²) adopt at 3× rate of smaller ones.
   - Link: "Learn more →"

3. **Recife, PE — IPTU Sustentável** — 5–10% discount program launched 2020. Focus on commercial and mixed-use. Key learning: pairing with low-interest BNDES financing doubled adoption.
   - Link: "Learn more →"

4. **Belo Horizonte, MG — IPTU Verde** — Property tax incentive linked to sustainability certification. Key learning: clear technical guidelines for PV installation reduced application processing time by 60%.
   - Link: "Learn more →"

Each card: city name as title, 2–3 sentence summary, "Learn more →" link (placeholder URL for MVP).

### Tab 3: Next Steps

**Primary next step card** (prominent, with an icon):
- Title: "Define Grid Capacity for Priority Neighborhoods"
- Body: "Before implementing the IPTU Sustentável incentive, the selected high-potential neighborhoods need grid capacity validation. The local distribution grid may have feeder or transformer limitations that constrain how much distributed solar can be interconnected."
- **Suggested approach:** "Request a joint technical assessment with CEEE Equatorial (the local energy distributor) to evaluate: feeder capacity and current loading, transformer headroom for reverse power flow, interconnection requirements and timelines for each priority neighborhood."
- Call-to-action button: "Download neighborhood list for distributor" (generates a simple text/CSV of selected neighborhoods + estimated kWp)

**Other pending data** (bulleted list):
- Updated commercial building registry with roof area measurements
- Current IPTU billing records by neighborhood (to validate revenue estimates)
- Historical solar permit data (existing PV installations in commercial buildings)
- Heritage/preservation zone boundaries (some neighborhoods may have installation restrictions)
- Flood risk overlay for long-term PV investment viability assessment

## Data model
```typescript
interface Neighborhood {
  id: string
  name: string
  tier: "high" | "medium" | "low"
  bounds: [number, number][]     // polygon coords for neighborhood boundary
  commercialBuildings: number
  residentialBuildings: number
  solarPotentialKwp: number      // total commercial solar potential
  iptuRevenueBrl: number         // annual IPTU from commercial buildings
  avgSolarGhi: number            // kWh/m²/year
  scenario5pct: {
    revenueLostBrl: number
    pvInstalledKwp: number
    annualGenerationMwh: number
    co2AvoidedTons: number
  }
  scenario10pct: {
    revenueLostBrl: number
    pvInstalledKwp: number
    annualGenerationMwh: number
    co2AvoidedTons: number
  }
}

interface CommercialBuilding {
  id: string
  neighborhoodId: string
  lat: number
  lng: number
  type: "commercial"
  roofAreaM2: number
  solarPotentialKwp: number
}

interface ResidentialBuilding {
  id: string
  neighborhoodId: string
  lat: number
  lng: number
  type: "residential"
  // No other fields needed — these are display-only, grayed out
}
```

Generate mock data for 10 Porto Alegre neighborhoods with realistic names (Centro Histórico, Moinhos de Vento, Cidade Baixa, Bom Fim, Petrópolis, Menino Deus, Floresta, Auxiliadora, Santana, Partenon). Spread across tiers: 3 high, 4 medium, 3 low. Each neighborhood has 5–15 commercial buildings and 10–30 residential buildings as markers.

## Tech notes
- Component: client/src/components/interventions/SolarRegulationPanel.tsx
- shadcn Sheet, Tabs, Card, Badge, Button, ScrollArea, Separator
- Map: Leaflet Polygon for neighborhoods (colored by tier), CircleMarker for buildings
- Commercial markers: colored by tier, clickable
- Residential markers: gray (#9ca3af), not clickable, lower opacity (0.4)
- State: React useState (client-side only, no DB)
- Selected neighborhood stored in state, detail card renders based on selection
```

---

### Prompt 3 — Wire up + Polish (if time allows)

```
Wire up the two intervention panels to the main app and polish.

1. Add an "Interventions" button to the existing toolbar/nav — opens the dashboard
2. When a neighborhood is selected in the Regulation panel, highlight its polygon on the map and zoom to it
3. When a portfolio scope is selected in Panel 1, show a persistent summary chip somewhere visible on the map (e.g. "High Priority scope: 112 buildings selected")
4. Make sure both panels can be open one at a time (closing one opens the other if user navigates back to dashboard)
5. Mobile: panels should be full-width on small screens
6. Add a simple "Reset" option to each panel to clear selections
7. "Download neighborhood list" button in Next Steps tab generates a simple CSV with neighborhood name, tier, commercial buildings count, solar potential kWp
```

---

## Reference Data

| Source | Key numbers |
|--------|------------|
| `context/geographic/porto-alegre/porto-alegre-energy-actions-plac-2024.yaml` | POA-E-07 (municipal buildings) and POA-E-06 (policy) metrics |
| `data/research/benchmarks/solar-pv-brazil-2024.json` | R$4,500/kWp, 1,405 kWh/kWp/yr |
| `data/layers-energy-mapping.json` | Layer IDs for solar, flood, IBGE, built-up, night lights |
| `analysis/action-selection/intervention_solar-mandate-residential-commercial.md` | Policy intervention definition and assumptions |
| `data/Intervention_BuildingSolarPolicy_dataAnalysis/assumptions.md` | Design assumptions behind IPTU Sustentável scenarios |
