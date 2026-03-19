# Site Assessment Summary

## Project
- **City**: {{city_name}} ({{city_locode}})
- **Analysis Date**: {{analysis_date}}

## Study Area
- **Boundary**: {{study_area_description}}
- **Total Area**: {{total_area_km2}} km2
- **Zones Analyzed**: {{total_zones}}
- **Zones Passing Constraints**: {{zones_passing}}

## Top Candidate Zones

### Zone 1: {{zone_1_name}}
- **Score**: {{zone_1_score}}/100
- **Solar Resource (GHI)**: {{zone_1_ghi}} kWh/m2/year
- **Land Cover**: {{zone_1_landcover}}
- **Flood Risk**: {{zone_1_flood_risk}}
- **Population Density**: {{zone_1_pop_density}} people/km2
- **Constraints Flagged**: {{zone_1_flags}}

### Zone 2: {{zone_2_name}}
(same structure)

### Zone 3: {{zone_3_name}}
(same structure)

## Constraint Summary
| Constraint | Type | Zones Excluded |
|-----------|------|---------------|
| {{constraint_rows}} |

## Data Sources Used
| Layer | Source | Resolution |
|-------|--------|-----------|
| {{layer_rows}} |

## Limitations and Gaps
- {{limitations}}

## Recommendation
{{recommendation}}
