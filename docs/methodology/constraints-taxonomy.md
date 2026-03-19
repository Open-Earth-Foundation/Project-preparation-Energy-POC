# Constraints Taxonomy

## Constraint Types

### Geographic
Physical site characteristics that limit or exclude certain technologies.
- Flood zones (high/moderate risk)
- Steep terrain (slope > 15 degrees)
- Water bodies
- Dense urban areas (for ground-mount)

### Regulatory
Legal or policy constraints on land use and development.
- Protected / conservation areas
- Buffer zones (airports, heritage sites)
- Zoning restrictions
- Environmental licensing requirements

### Technical
Infrastructure and resource limitations.
- Insufficient solar resource
- No grid connection available
- Inadequate grid capacity for injection
- Site access limitations

### Budget
Financial constraints that affect technology viability.
- Maximum CAPEX available
- Required payback period
- Minimum IRR threshold

### Social
Community and equity considerations (typically not exclusionary).
- Informal settlements (special engagement needed)
- Community opposition risk
- Displacement risk
- Cultural heritage sensitivity

## Severity Levels

### Hard Constraints
Exclusionary — zones failing hard constraints are removed from consideration entirely.
Examples: high flood risk for ground-mount, water bodies, protected forests.

### Soft Constraints
Penalty-based — zones trigger a score reduction but remain in the candidate set.
Examples: moderate flood risk, steep slope, grid distance.

## Constraint Configuration

Constraints are defined in `data/site-constraint-types.json` with:
- `layerId`: which Geo-Layer-Viewer layer to evaluate
- `operator`: comparison operator (gt, gte, lt, lte, eq, ne, in, not_in)
- `threshold`: the threshold value for triggering the constraint
- `applicableTech`: which technologies this constraint applies to (if not all)
- `scorePenalty`: points deducted for soft constraints
