# Scoring Model

## Site Scoring

Multi-criteria weighted sum approach. Each candidate zone receives a score from 0-100.

### Formula

```
score = sum(weight_i * normalized_value_i) * 100 - sum(penalties)
```

Where:
- `weight_i` = criterion weight from `data/scoring-weights.json`
- `normalized_value_i` = layer value normalized to 0-1 range
- `penalties` = soft constraint penalties

### Normalization

```
normalized = clamp((value - min) / (max - min), 0, 1)
```

For inverted criteria (e.g., flood risk where lower is better):
```
normalized = 1 - clamp((value - min) / (max - min), 0, 1)
```

### Weight Adjustment

Default weights are starting points. They should be adjusted based on:
- City priorities (equity vs efficiency vs speed)
- Technology focus (ground-mount solar weights land availability higher)
- Regulatory context (some constraints become hard in certain jurisdictions)

## Technology Scoring

Qualitative scoring on 0-100 scale for each criterion, then weighted sum.

Criteria are assessed as:
- **Excellent** (80-100): Strong fit, low risk
- **Good** (60-79): Adequate fit, manageable risk
- **Fair** (40-59): Possible but with significant caveats
- **Poor** (0-39): Not recommended without major mitigation

## Maturity Tiers

Overall project readiness is classified as:

| Tier | Score Range | Meaning |
|------|------------|---------|
| Ready | 75-100 | Strong candidate — proceed to detailed feasibility |
| Promising | 50-74 | Good potential — needs further investigation on flagged issues |
| Conditional | 25-49 | Viable only with specific conditions met |
| Not recommended | 0-24 | Fundamental constraints — consider alternative sites/technologies |
