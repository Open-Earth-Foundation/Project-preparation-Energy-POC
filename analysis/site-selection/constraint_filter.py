"""Filter candidate zones by constraint definitions.

Applies hard constraints (exclusion) and soft constraints (penalties)
from data/site-constraint-types.json.

Usage:
    python -m analysis.site_selection.constraint_filter

Inputs:
    - Candidate zones from candidate_zones.py
    - Constraint definitions from data/site-constraint-types.json

Outputs:
    - Filtered zones with constraint results attached
"""

import operator
from typing import Any

from analysis.shared.data_loader import load_constraints
from analysis.shared.types import ConstraintResult, ConstraintSeverity

OPERATORS = {
    "gt": operator.gt,
    "gte": operator.ge,
    "lt": operator.lt,
    "lte": operator.le,
    "eq": operator.eq,
    "ne": operator.ne,
}


def evaluate_constraint(constraint: dict, layer_value: Any) -> ConstraintResult:
    """Evaluate a single constraint against a layer value.

    Args:
        constraint: Constraint definition from site-constraint-types.json.
        layer_value: The value from the geo layer for this zone.

    Returns:
        ConstraintResult indicating pass/fail and any penalty.
    """
    if layer_value is None:
        # Missing data — cannot evaluate, pass by default
        return ConstraintResult(
            constraint_id=constraint["id"],
            passed=True,
            severity=ConstraintSeverity(constraint["severity"]),
            description=f"No data for {constraint['layerId']}",
        )

    op_name = constraint.get("operator")
    threshold = constraint.get("threshold")

    if op_name == "in":
        triggered = layer_value in threshold
    elif op_name == "not_in":
        triggered = layer_value not in threshold
    elif op_name in OPERATORS:
        triggered = OPERATORS[op_name](layer_value, threshold)
    else:
        triggered = False

    severity = ConstraintSeverity(constraint["severity"])
    passed = not triggered

    return ConstraintResult(
        constraint_id=constraint["id"],
        passed=passed,
        severity=severity,
        penalty=constraint.get("scorePenalty", 0) if not passed and severity == ConstraintSeverity.SOFT else 0,
        description=constraint.get("description", ""),
    )


def filter_zones(
    zones: list[dict],
    technology_id: str | None = None,
) -> list[dict]:
    """Apply all constraints to candidate zones.

    Args:
        zones: List of zone dicts with layer_values.
        technology_id: If provided, only apply constraints relevant to this tech.

    Returns:
        Zones that pass all hard constraints, with soft constraint results attached.
    """
    constraints = load_constraints()

    # Filter constraints by applicable technology if specified
    if technology_id:
        constraints = [
            c for c in constraints
            if "applicableTech" not in c or technology_id in c["applicableTech"]
        ]

    filtered = []
    for zone in zones:
        layer_values = zone.get("layer_values", {})
        results = []
        excluded = False

        for constraint in constraints:
            layer_id = constraint.get("layerId", "")
            value = layer_values.get(layer_id)

            result = evaluate_constraint(constraint, value)
            results.append(result)

            if not result.passed and result.severity == ConstraintSeverity.HARD:
                excluded = True
                break

        if not excluded:
            zone["constraint_results"] = [
                {"id": r.constraint_id, "passed": r.passed, "penalty": r.penalty}
                for r in results
            ]
            zone["total_penalty"] = sum(r.penalty for r in results)
            filtered.append(zone)

    return filtered
