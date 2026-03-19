# Intervention: Solar Mandate Policies for Residential and Commercial Buildings

**Parent Action:** POA-E-06 — Sustainable Buildings (Private Sector Leverage)
**C40 HIA:** 14 — Renewable Energy Mandates for Buildings
**City:** Porto Alegre (BR POA)
**Date:** 2026-03-19

---

## Intervention Definition

Implement regulatory and fiscal policies that mandate and incentivize distributed solar PV adoption on residential and commercial buildings in Porto Alegre. This is a **policy intervention**, not a capital project — the city creates the rules; the private sector makes the investment.

**Two building segments:**

| Segment | Building Stock (POA) | 2030 Target | 2040 Target | 2050 Target |
|---------|---------------------|-------------|-------------|-------------|
| **Residential** | 456,770 households (br_ibge) | 8% with distributed renewables | 25% | 40% |
| **Commercial** | Included in built-up stock (ghsl_built_up) | 10% with distributed renewables | 30% | 50% |

---

## What C40 Calls This

> **HIA 14:** "City is implementing renewable energy mandates for buildings"
> **Sector:** Energy and Buildings
> **Source:** `high-impact-actions.csv`, ID 14

C40 defines this as a single high-impact action. Porto Alegre delivers it through three coordinated policy instruments drawn from PLAC sub-actions:

| Policy Instrument | PLAC Sub-Action | What It Does |
|-------------------|-----------------|--------------|
| **Sustainable Certification Program** (Decree 21.789/2022) | 6.1 — Promote certification | Sets technical criteria. Awards points for solar PV, efficient lighting, NbS. Already active. |
| **Building Code Update** | 6.4 — Mandatory energy/water efficiency criteria | Makes solar-readiness or solar installation a code requirement for new builds. Short-term timeline. |
| **IPTU Sustentavel** (property tax incentive) | 6.6 — Expand fiscal incentives | Reduces property tax for buildings that install solar PV or meet certification thresholds. Drives retrofit adoption. |

The combination of mandate (code) + incentive (IPTU) + standard (certification) is what makes this a complete renewable energy mandate in C40 terms.

**Alignment strength:** Direct. POA goes beyond what C40 requires — it pairs mandates with fiscal incentives, creating both a regulatory push and an economic pull.

---

## How It Relates to the Municipal Plan (PLAC)

This intervention is a **subset of POA-E-06** focused specifically on the solar policy instruments for residential and commercial buildings. Within the PLAC architecture:

```
PLAC — POA Baixo Carbono (Strategic Axis)
└── POA-E-06 — Sustainable Buildings (full action)
    ├── Sub-action 6.1 — Certification promotion        ← THIS INTERVENTION
    ├── Sub-action 6.4 — Building Code update            ← THIS INTERVENTION
    ├── Sub-action 6.5 — Renewable energy studies        ← THIS INTERVENTION
    ├── Sub-action 6.6 — IPTU Sustentável expansion      ← THIS INTERVENTION
    ├── Sub-action 6.2 — Mandatory certification (new)   (related but broader)
    └── Sub-action 6.3 — Monitoring & evaluation         (supporting)
```

**Lead institution:** SMAMUS
**Partners:** SMP (urban planning), SMF (finance/fiscal incentives)

---

## Enabling Framework

This intervention does not operate alone. It depends on an active state-level policy stack:

| Level | Instrument | Role |
|-------|-----------|------|
| **Federal** | Brazil MMGD (net metering) | Allows distributed generation up to 5 MW with grid credit. Makes solar economically viable for building owners. |
| **State** | Lei Estadual 14.898/2016 — Solar Energy Incentives | RS state policy that reduces barriers for solar adoption. |
| **State** | Decreto Estadual 53.160/2016 — RS Energias Renováveis | State renewable energy program providing regulatory support. |
| **State** | RS-E-03 — Renewable Energy Policy Package | Ranked #1 in cost-effectiveness (R$4/tCO2e). Enables 200 MWp of solar across POA. Already active. |
| **Municipal** | Decree 21.789/2022 | Sustainability Certification Program. Already in effect. |
| **Municipal** | POA-E-06 sub-actions 6.1, 6.4, 6.5, 6.6 | The specific policy instruments in this intervention. |

---

## Key Numbers

| Metric | Value | Source |
|--------|-------|--------|
| Government cost | R$6M (program administration + incentive design) | PLAC cost-effectiveness |
| Private investment enabled | R$658M | PLAC cost-effectiveness |
| Leverage ratio | 1:110 (R$1 govt → R$110 private) | PLAC cost-effectiveness |
| Installed capacity by 2030 | 146.2 MWp (residential + commercial + industrial) | PLAC targets |
| Annual generation | 205,400 MWh | PLAC cost-effectiveness |
| Annual GHG avoided | 26,702 tCO2e | PLAC cost-effectiveness |
| Cost per tCO2e (govt) | R$9 | PLAC cost-effectiveness |
| Private payback | 4.0 years | PLAC cost-effectiveness |
| Solar resource (POA) | 1,405 kWh/kWp/year (GHI 1,500-1,700 kWh/m²/yr) | global_solar_atlas |
| CAPEX benchmark | R$4,500/kWp (ABSOLAR 2024) | solar-pv-brazil-2024.json |
| Grid tariff | R$0.80/kWh (CEEE Equatorial 2024) | PLAC methodology |
| Grid emission factor | 0.130 tCO2e/MWh (BR South) | SEEG 2022 |

---

## Residential vs. Commercial Segments

| Dimension | Residential | Commercial |
|-----------|-------------|------------|
| **2030 target** | 8% of households (~36,542 HH) | 10% of commercial buildings |
| **Typical system size** | 3-5 kWp per household | 20-200 kWp per building |
| **Primary policy lever** | IPTU Sustentavel (tax incentive) | Building Code mandate + certification |
| **Payback driver** | High residential tariff (R$0.80/kWh) | Energy cost reduction + green certification value |
| **Adoption barrier** | Upfront cost for homeowners | Split incentive (tenant vs. owner) |
| **Equity consideration** | Target IPTU incentives to low-income neighborhoods using br_ibge census data | Less equity concern; focus on high-consumption zones |

---

## Connection to Broader C40 and PLAC Actions

This solar mandate intervention also partially delivers on:

| C40 HIA | Connection |
|---------|------------|
| **HIA 12** — Grid decarbonization | 146 MWp of distributed solar directly decarbonizes the building-scale grid |
| **HIA 16** — Retrofit programs for private buildings | IPTU Sustentavel drives solar retrofits on existing buildings |
| **HIA 10** — Building energy codes toward net zero | Building Code update (sub-action 6.4) is a step toward net-zero new construction |
| **HIA 29** — Cool surfaces | Solar + green roof hybrid installations are incentivized through the certification program |

Within PLAC, it connects to:
- **POA-E-07** — Public buildings solar (government leads by example)
- **POA-E-08** — Sustainable Logistics Plan (behavioral/institutional support)
- **RS-E-03** — State solar policy (enabling regulatory framework)
- **RS-E-04** — Carbon market (potential revenue stream for certified buildings)

---

## Source Files

| File | Relevant Content |
|------|-----------------|
| `context/geographic/porto-alegre/porto-alegre-energy-actions-plac-2024.yaml` lines 76-209 | POA-E-06 full action, sub-actions, targets, cost-effectiveness |
| `context/geographic/porto-alegre/porto-alegre-energy-actions-plac-2024.yaml` lines 615-686 | RS-E-03 state solar policy package |
| `analysis/action-selection/high-impact-actions.csv` line 15 | C40 HIA 14 definition |
| `data/research/benchmarks/solar-pv-brazil-2024.json` | Solar PV cost and resource benchmarks |
| `data/energy-action-catalog.json` lines 1-43 | `solar-public-buildings` archetype (related technology) |
| `analysis/action-selection/selected-action_sustainable-buildings.md` | Full parent action profile |
