# Site & Technology Selection UI — MVP PRD + Implementation Prompts

**Project:** Energy Project Preparation Module — Porto Alegre Solar PV
**Target repo:** Geo-Layer-Viewer (github.com/joaquinOEF/Geo-Layer-Viewer)
**Scope:** MVP, ~2 hours build time

---

## Overview

A city user (Porto Alegre municipal staff) needs to act on two solar PV interventions. This UI surfaces the right geospatial data and lets them make decisions — no backend, client-side state only.

**Two interventions:**
1. **Municipal Solar Portfolio** — Select a priority scope for rooftop solar on city-owned buildings (POA-E-07)
2. **Building Solar Policy Design** — Answer guided questions to shape the residential/commercial solar mandate (POA-E-06)

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

## Intervention 2 — Building Solar Policy Design

### What it is
The city is designing a solar mandate for residential/commercial buildings via three policy instruments: Building Code update, Sustainability Certification, and IPTU Sustentável (property tax incentive). This questionnaire helps the city planner understand which geospatial factors should shape the policy.

### Key metrics (from PLAC POA-E-06)
- Target: 146.2 MWp by 2030 (8% residential HH, 10% commercial buildings)
- Leverage: R$1 govt → R$110 private investment
- 26,702 tCO2e/year avoided, R$9/tCO2e govt cost
- Residential: 3–5 kWp/household | Commercial: 20–200 kWp/building

### Policy questions (6 questions, each with a linked map layer)

| # | Question | Layer to toggle | Why it matters |
|---|----------|----------------|----------------|
| Q1 | Should the mandate apply citywide or only in high-solar zones? | `solar-neighbourhoods` (PVOUT) | Solar resource varies; stricter mandates make sense where resource is best |
| Q2 | Should low-income neighborhoods get larger IPTU tax discounts? | `ibge-indicators` (income/poverty) | Equity design — PLAC explicitly targets low-income areas for incentives |
| Q3 | Should the policy prioritize new construction, retrofits, or both? | `ghsl-built` (built-up density) | Building code only applies to new builds; IPTU drives retrofits |
| Q4 | Should flood-risk areas require resilience measures before qualifying? | `flood-risk-index` | PV systems last 25 years — flood risk is a long-term viability factor |
| Q5 | Should historic/heritage districts be excluded from the mandate? | *(no layer — note data gap)* | Porto Alegre has protected districts where panel installation is restricted |
| Q6 | Should areas with higher electricity consumption get lower incentives (faster payback anyway)? | `viirs-night-lights` (grid/consumption proxy) | Calibrates incentive levels — high-consumption zones need less subsidy |

### UX Flow
1. User opens "Building Solar Policy" intervention card
2. Side panel opens with step-by-step questions (progress indicator: 1 of 6)
3. Each question has: question text, brief explanation, answer options (Yes/No/Partial), and a **"View on map"** button that toggles the relevant layer
4. User can navigate back/forward through questions
5. Final step: summary of policy choices with referenced layers
6. "Export summary" button copies a text summary to clipboard

---

## Dashboard / Landing

A simple landing view before either intervention:

- **Header:** "Porto Alegre — Solar PV Interventions"
- **Two cards side by side:**
  - Card 1: Municipal Solar Portfolio — shows key metrics (37 MWp, 560 buildings, R$41.6M/yr savings, 6,759 tCO2e/yr)
  - Card 2: Building Solar Policy — shows key metrics (146.2 MWp target, 1:110 leverage ratio, 26,702 tCO2e/yr)
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
- "Building Solar Policy" — 146.2 MWp target | 1:110 leverage | 26,702 tCO2e/yr avoided

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

### Prompt 2 — Building Solar Policy Questionnaire

```
Add the second intervention: Building Solar Policy Design questionnaire.

## What to build

A side panel (shadcn Sheet, right side) that opens when "Building Solar Policy" card is clicked.

**Header:** "Building Solar Policy Design" | Progress indicator: "Step 2 of 6"

**Step-by-step questions** (one question visible at a time):

For each question, show:
1. Question text (large, readable)
2. 2-sentence explanation of why this matters
3. Answer options as toggle buttons: Yes / Partial / No
4. A "View on map" button that toggles the relevant geo layer

**The 6 questions:**

Q1: "Apply the mandate citywide or only in high-solar zones?"
- Explanation: Solar resource varies across Porto Alegre (GHI 1,500–1,700 kWh/m²/yr). Zones with best resource can support stricter minimum system sizes.
- Map layer: solar-neighbourhoods (toggle PVOUT layer)

Q2: "Give larger IPTU tax discounts in low-income neighborhoods?"
- Explanation: The PLAC explicitly targets IPTU Sustentável incentives toward low-income areas. This addresses the upfront cost barrier for homeowners.
- Map layer: ibge-indicators (toggle income/poverty layer)

Q3: "Target new construction, existing buildings (retrofits), or both?"
- Options: New only / Retrofits only / Both
- Explanation: Building Code update applies to new construction only. IPTU Sustentável is the primary driver for retrofits on existing buildings.
- Map layer: ghsl-built (built-up density, proxy for existing stock concentration)

Q4: "Require flood resilience measures for buildings in flood-risk zones?"
- Explanation: Solar PV systems last 25 years. High-risk flood zones may see increased flooding by 2050. Resilience measures protect the investment.
- Map layer: flood-risk-index

Q5: "Exclude heritage/historic districts from the solar mandate?"
- Explanation: Porto Alegre has protected historic districts where panel installation may be restricted by IPHAE and IPHAN.
- Map layer: none — show a note: "Heritage boundary data not yet in platform — flag for planning review"

Q6: "Reduce incentives in areas with high electricity consumption (they have faster payback anyway)?"
- Explanation: Buildings with high consumption reach payback in ~3 years without large incentives. Redirecting subsidies to lower-consumption areas improves equity.
- Map layer: viirs-night-lights (proxy for grid/consumption density)

**Navigation:** Back / Next buttons. Next is disabled until an answer is selected.

**Summary step** (after Q6):
- Show all 6 questions with the user's answers
- Show a "Referenced layers" section listing the layers used
- "Export summary" button — copies a formatted text to clipboard:
  ```
  Porto Alegre — Building Solar Policy Design
  Date: [today]

  Q1 Mandate scope: [answer]
  Q2 Equity targeting: [answer]
  Q3 Building type: [answer]
  Q4 Flood resilience: [answer]
  Q5 Heritage exclusion: [answer]
  Q6 Incentive calibration: [answer]

  Key metrics: 146.2 MWp target | 26,702 tCO2e/yr | R$9/tCO2e govt cost
  ```

## State
```typescript
interface PolicyAnswer {
  questionId: string
  answer: "yes" | "partial" | "no" | string  // string for Q3 which has 3 options
}
// useState<PolicyAnswer[]>([])
```

## Tech notes
- Component: client/src/components/interventions/PolicyDesignPanel.tsx
- shadcn Sheet, Button, Progress (or manual step dots), Separator, Badge
- "View on map" calls existing layer toggle mechanism (check how EvidenceDrawer handles this)
- Client-side only, no persistence
```

---

### Prompt 3 — Wire up + Polish (if time allows)

```
Wire up the two intervention panels to the main app and polish.

1. Add an "Interventions" button to the existing toolbar/nav — opens the dashboard
2. When "View on map" is clicked in the policy panel, actually toggle the layer using the existing layer config system (layer IDs are in client/src/data/layer-configs.ts)
3. When a portfolio scope is selected in Panel 1, show a persistent summary chip somewhere visible on the map (e.g. "High Priority scope: 112 buildings selected")
4. Make sure both panels can be open one at a time (closing one opens the other if user navigates back to dashboard)
5. Mobile: panels should be full-width on small screens
6. Add a simple "Reset" option to each panel to clear selections
```

---

## Reference Data

| Source | Key numbers |
|--------|------------|
| `context/geographic/porto-alegre/porto-alegre-energy-actions-plac-2024.yaml` | POA-E-07 (municipal buildings) and POA-E-06 (policy) metrics |
| `data/research/benchmarks/solar-pv-brazil-2024.json` | R$4,500/kWp, 1,405 kWh/kWp/yr |
| `data/layers-energy-mapping.json` | Layer IDs for solar, flood, IBGE, built-up, night lights |
| `analysis/action-selection/intervention_solar-mandate-residential-commercial.md` | Policy intervention definition and assumptions |
| `data/Intervention_BuildingSolarPolicy_dataAnalysis/assumptions.md` | 13 design assumptions behind the 6 policy questions |
