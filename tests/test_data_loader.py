"""Tests for reference data loading and validation."""

import json
from pathlib import Path

import pytest

from analysis.shared.data_loader import (
    load_tech_catalog,
    load_constraints,
    load_scoring_weights,
    load_layer_mapping,
    load_financing_archetypes,
    validate_data_files,
)

DATA_DIR = Path(__file__).parent.parent / "data"


class TestDataFilesExist:
    """Verify all expected data files exist and parse correctly."""

    def test_validate_all_data_files(self):
        results = validate_data_files()
        for name, ok in results.items():
            assert ok, f"Data file {name} failed validation"

    def test_tech_catalog_valid_json(self):
        with open(DATA_DIR / "energy-tech-catalog.json") as f:
            data = json.load(f)
        assert "technologies" in data
        assert len(data["technologies"]) > 0

    def test_constraints_valid_json(self):
        with open(DATA_DIR / "site-constraint-types.json") as f:
            data = json.load(f)
        assert "constraints" in data

    def test_scoring_weights_valid_json(self):
        with open(DATA_DIR / "scoring-weights.json") as f:
            data = json.load(f)
        assert "siteScoring" in data
        assert "technologyScoring" in data

    def test_layer_mapping_valid_json(self):
        with open(DATA_DIR / "layers-energy-mapping.json") as f:
            data = json.load(f)
        assert "layers" in data


class TestTechCatalog:
    """Verify technology catalog structure and content."""

    def test_load_returns_list(self):
        techs = load_tech_catalog()
        assert isinstance(techs, list)
        assert len(techs) >= 6  # We defined 6 archetypes

    def test_each_tech_has_required_fields(self):
        techs = load_tech_catalog()
        required = {"id", "name", "category", "description"}
        for tech in techs:
            missing = required - set(tech.keys())
            assert not missing, f"Tech {tech.get('id', '?')} missing fields: {missing}"

    def test_tech_ids_unique(self):
        techs = load_tech_catalog()
        ids = [t["id"] for t in techs]
        assert len(ids) == len(set(ids)), "Duplicate technology IDs found"

    def test_valid_categories(self):
        valid = {"solar_pv", "battery_storage", "grid_upgrade", "efficiency", "distributed_generation", "hybrid"}
        techs = load_tech_catalog()
        for tech in techs:
            assert tech["category"] in valid, f"Invalid category: {tech['category']}"


class TestConstraints:
    """Verify constraint definitions."""

    def test_load_returns_list(self):
        constraints = load_constraints()
        assert isinstance(constraints, list)
        assert len(constraints) > 0

    def test_each_constraint_has_required_fields(self):
        constraints = load_constraints()
        required = {"id", "name", "type", "severity"}
        for c in constraints:
            missing = required - set(c.keys())
            assert not missing, f"Constraint {c.get('id', '?')} missing fields: {missing}"

    def test_valid_severities(self):
        constraints = load_constraints()
        for c in constraints:
            assert c["severity"] in {"hard", "soft"}, f"Invalid severity: {c['severity']}"


class TestScoringWeights:
    """Verify scoring weight configuration."""

    def test_site_weights_sum_to_one(self):
        config = load_scoring_weights()
        weights = config["siteScoring"]["weights"]
        total = sum(w["weight"] for w in weights.values())
        assert abs(total - 1.0) < 0.001, f"Site weights sum to {total}, expected 1.0"

    def test_tech_weights_sum_to_one(self):
        config = load_scoring_weights()
        weights = config["technologyScoring"]["weights"]
        total = sum(w["weight"] for w in weights.values())
        assert abs(total - 1.0) < 0.001, f"Tech weights sum to {total}, expected 1.0"


class TestLayerMapping:
    """Verify layer-energy mapping."""

    def test_load_returns_dict(self):
        mapping = load_layer_mapping()
        assert isinstance(mapping, dict)
        assert len(mapping) > 0

    def test_each_layer_has_relevance(self):
        mapping = load_layer_mapping()
        valid_relevance = {"primary", "secondary", "constraint", "context"}
        for layer_id, config in mapping.items():
            assert config.get("relevance") in valid_relevance, (
                f"Layer {layer_id} has invalid relevance: {config.get('relevance')}"
            )

    def test_each_layer_has_component(self):
        mapping = load_layer_mapping()
        valid_components = {"site-selection", "technology-selection"}
        for layer_id, config in mapping.items():
            assert config.get("component") in valid_components, (
                f"Layer {layer_id} has invalid component: {config.get('component')}"
            )
