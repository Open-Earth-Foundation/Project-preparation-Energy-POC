"""Tests for site scoring logic."""

import pytest

from analysis.site_selection.site_scoring import normalize, score_zone
from analysis.shared.data_loader import load_scoring_weights


class TestNormalize:
    def test_mid_value(self):
        assert normalize(50, 0, 100) == 0.5

    def test_min_value(self):
        assert normalize(0, 0, 100) == 0.0

    def test_max_value(self):
        assert normalize(100, 0, 100) == 1.0

    def test_below_min_clamps(self):
        assert normalize(-10, 0, 100) == 0.0

    def test_above_max_clamps(self):
        assert normalize(150, 0, 100) == 1.0

    def test_inverted(self):
        assert normalize(0, 0, 100, invert=True) == 1.0
        assert normalize(100, 0, 100, invert=True) == 0.0

    def test_equal_min_max(self):
        assert normalize(50, 50, 50) == 0.5


class TestScoreZone:
    def test_zone_with_all_values(self):
        zone = {
            "id": "test-zone",
            "name": "Test Zone",
            "layer_values": {
                "solar-neighbourhoods": 1500,
                "flood-risk-index": 0.2,
                "dynamic-world": 0.7,
                "viirs-night-lights": 30,
                "ghsl-population": 5000,
                "ibge-indicators": 25,
            },
            "constraint_results": [],
            "total_penalty": 0,
        }

        weights = load_scoring_weights()
        scored = score_zone(zone, weights)

        assert scored.zone_id == "test-zone"
        assert 0 <= scored.score <= 100
        assert isinstance(scored.score_breakdown, dict)

    def test_zone_with_penalty(self):
        zone = {
            "id": "penalized-zone",
            "name": "Penalized Zone",
            "layer_values": {},
            "constraint_results": [{"id": "flood-risk-moderate", "passed": False, "penalty": 20}],
            "total_penalty": 20,
        }

        weights = load_scoring_weights()
        scored = score_zone(zone, weights)

        # Score should be reduced by penalty
        zone_no_penalty = {**zone, "total_penalty": 0}
        scored_no_penalty = score_zone(zone_no_penalty, weights)

        assert scored.score < scored_no_penalty.score
