# Context

Baseline context that informs energy project site selection and technology decisions. This is the analytical foundation — everything upstream of the scoring and matching logic.

Context is organized by **dimension**, not just geography. A good pre-feasibility analysis needs to understand the landscape from multiple angles before proposing sites or technologies.

## Structure

```
context/
├── geographic/             Spatial and socioeconomic context by scale
│   ├── brazil/             National energy profile, grid mix, market structure
│   ├── rio-grande-do-sul/  State energy profile, grid infrastructure, tariffs
│   └── porto-alegre/       City energy situation, demand, climate action plans
│
├── technology/             Technology landscape and opportunities
│                           What's been deployed, what's emerging, local supply chain,
│                           performance data from comparable deployments
│
├── financing/              Funder landscape and preferences
│                           DFI priorities, climate fund eligibility, funder track records,
│                           what types of projects get funded, ticket sizes, co-financing
│                           requirements, past approvals
│
├── regulatory/             Policy and regulatory environment
│                           Energy regulations, net metering rules, environmental licensing,
│                           PPP frameworks, tax incentives, concession models
│
└── projects/               Reference projects and precedents
                            Past energy projects that have been funded/implemented in the
                            region — what worked, what didn't, scale, funder, technology,
                            lessons learned
```

## How Context Feeds Into Analysis

```
context/geographic/     → Site selection constraints, demand estimation
context/technology/     → Technology catalog validation, local feasibility
context/financing/      → Financing archetype selection, funder targeting
context/regulatory/     → Constraint definitions, implementation timeline
context/projects/       → Benchmarking, risk calibration, sizing validation
```

## File Formats

- **PDFs and reports**: Original source documents (keep as-is for provenance)
- **Markdown summaries**: Structured summaries of key findings from source documents
- **JSON**: Structured data extracted from context (e.g., tariff tables, project lists)

When adding a new document, prefer creating a markdown summary alongside the source file so agents and analysis scripts can parse it without PDF extraction.

## Naming Convention

Use descriptive names with date or version when relevant:
```
porto-alegre-plac-executive-summary-v7-en.pdf
brazil-energy-matrix-2024.md
bndes-climate-fund-eligibility-2025.md
porto-alegre-solar-rooftop-pilot-2023.md
```
