"""Tests for constraint filtering logic."""

import pytest

from analysis.site_selection.constraint_filter import evaluate_constraint
from analysis.shared.types import ConstraintSeverity


class TestEvaluateConstraint:
    def test_hard_constraint_triggered(self):
        constraint = {
            "id": "flood-risk-high",
            "severity": "hard",
            "layerId": "flood-risk-index",
            "operator": "gte",
            "threshold": 0.7,
        }
        result = evaluate_constraint(constraint, 0.85)
        assert not result.passed
        assert result.severity == ConstraintSeverity.HARD

    def test_hard_constraint_passes(self):
        constraint = {
            "id": "flood-risk-high",
            "severity": "hard",
            "layerId": "flood-risk-index",
            "operator": "gte",
            "threshold": 0.7,
        }
        result = evaluate_constraint(constraint, 0.3)
        assert result.passed

    def test_soft_constraint_returns_penalty(self):
        constraint = {
            "id": "flood-risk-moderate",
            "severity": "soft",
            "layerId": "flood-risk-index",
            "operator": "gte",
            "threshold": 0.4,
            "scorePenalty": 20,
        }
        result = evaluate_constraint(constraint, 0.5)
        assert not result.passed
        assert result.penalty == 20

    def test_missing_data_passes_by_default(self):
        constraint = {
            "id": "test",
            "severity": "hard",
            "layerId": "some-layer",
            "operator": "gte",
            "threshold": 0.5,
        }
        result = evaluate_constraint(constraint, None)
        assert result.passed

    def test_in_operator(self):
        constraint = {
            "id": "protected-area",
            "severity": "hard",
            "layerId": "dynamic-world",
            "operator": "in",
            "threshold": ["forest", "wetland"],
        }
        result = evaluate_constraint(constraint, "forest")
        assert not result.passed

    def test_in_operator_passes(self):
        constraint = {
            "id": "protected-area",
            "severity": "hard",
            "layerId": "dynamic-world",
            "operator": "in",
            "threshold": ["forest", "wetland"],
        }
        result = evaluate_constraint(constraint, "grassland")
        assert result.passed
