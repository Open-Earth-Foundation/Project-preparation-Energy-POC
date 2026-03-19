"""Multi-criteria site scoring.

Applies weighted scoring to candidate zones that have passed constraint filtering.
Uses weights and normalization parameters from data/scoring-weights.json.

Usage:
    python -m analysis.site_selection.site_scoring --city BR_POA

Inputs:
    - Filtered candidate zones with layer values
    - Scoring weights from data/scoring-weights.json

Outputs:
    - Ranked list of scored zones (0-100 scale)
"""

from analysis.shared.data_loader import load_scoring_weights
from analysis.shared.types import ScoredZone


def normalize(value: float, min_val: float, max_val: float, invert: bool = False) -> float:
    """Normalize a value to 0-1 range.

    Args:
        value: Raw value.
        min_val: Expected minimum.
        max_val: Expected maximum.
        invert: If True, higher raw values produce lower normalized scores.

    Returns:
        Normalized value clamped to [0, 1].
    """
    if max_val == min_val:
        return 0.5
    normalized = (value - min_val) / (max_val - min_val)
    normalized = max(0, min(1, normalized))
    return 1 - normalized if invert else normalized


def score_zone(zone: dict, weights_config: dict) -> ScoredZone:
    """Score a single zone using weighted multi-criteria analysis.

    Args:
        zone: Zone dict with layer_values and constraint results.
        weights_config: Site scoring weights from scoring-weights.json.

    Returns:
        ScoredZone with overall score and breakdown.
    """
    weights = weights_config["siteScoring"]["weights"]
    layer_values = zone.get("layer_values", {})
    score_breakdown = {}
    total_score = 0

    for criterion_name, criterion_config in weights.items():
        weight = criterion_config["weight"]
        layer_id = criterion_config.get("layerId", "")
        value_field = criterion_config.get("valueField")
        invert = criterion_config.get("invert", False)
        norm = criterion_config.get("normalization", {})

        # Get raw value from layer data
        raw_value = layer_values.get(layer_id)
        if raw_value is None and value_field:
            raw_value = layer_values.get(f"{layer_id}_{value_field}")

        if raw_value is not None and norm:
            normalized = normalize(raw_value, norm.get("min", 0), norm.get("max", 1), invert)
        else:
            normalized = 0.5  # Default for missing data

        weighted = normalized * weight
        score_breakdown[criterion_name] = round(normalized * 100, 1)
        total_score += weighted

    # Apply soft constraint penalties
    penalty = zone.get("total_penalty", 0)
    final_score = max(0, total_score * 100 - penalty)

    return ScoredZone(
        zone_id=zone["id"],
        name=zone["name"],
        score=round(final_score, 1),
        score_breakdown=score_breakdown,
        constraint_flags=[
            r["id"] for r in zone.get("constraint_results", []) if not r["passed"]
        ],
    )


def score_and_rank_zones(zones: list[dict]) -> list[ScoredZone]:
    """Score and rank all candidate zones.

    Args:
        zones: Filtered zones with layer_values and constraint results.

    Returns:
        List of ScoredZone sorted by score descending.
    """
    weights_config = load_scoring_weights()
    scored = [score_zone(z, weights_config) for z in zones]
    scored.sort(key=lambda z: z.score, reverse=True)
    return scored


if __name__ == "__main__":
    import argparse
    import json
    from dataclasses import asdict

    parser = argparse.ArgumentParser(description="Score and rank candidate zones")
    parser.add_argument("--city", default="BR_POA", help="City locode")
    args = parser.parse_args()

    # In practice, zones come from candidate_zones.py → constraint_filter.py
    # This stub demonstrates the scoring interface
    print(f"Site scoring for {args.city}")
    print("Run candidate_zones.py → constraint_filter.py → site_scoring.py for full pipeline")
