"""Tests for agent patch creation and application."""

import pytest

from agent.patches import create_patch, apply_patch
from analysis.shared.types import Patch


class TestCreatePatch:
    def test_creates_valid_patch(self):
        patch = create_patch(
            target_component="site-selection",
            target_field="candidateZones.0.score",
            proposed_value=85.5,
            rationale="Updated based on refined solar data",
            confidence=0.8,
            current_value=72.0,
            sources=["Global Solar Atlas 2024"],
        )
        assert patch.target_component == "site-selection"
        assert patch.proposed_value == 85.5
        assert patch.status == "proposed"
        assert patch.confidence == 0.8

    def test_patch_has_uuid(self):
        patch = create_patch(
            target_component="technology-selection",
            target_field="shortlist.0.name",
            proposed_value="Solar PV",
            rationale="test",
            confidence=0.5,
        )
        assert len(patch.id) > 0


class TestApplyPatch:
    def test_apply_accepted_patch(self):
        context = {
            "site-selection": {
                "summary": {"topZoneId": "old-zone"}
            }
        }
        patch = Patch(
            id="test-1",
            target_component="site-selection",
            target_field="summary.topZoneId",
            current_value="old-zone",
            proposed_value="new-zone",
            rationale="Better zone found",
            confidence=0.9,
            status="accepted",
        )
        updated = apply_patch(context, patch)
        assert updated["site-selection"]["summary"]["topZoneId"] == "new-zone"

    def test_reject_non_accepted_patch(self):
        context = {"site-selection": {}}
        patch = Patch(
            id="test-2",
            target_component="site-selection",
            target_field="summary.topZoneId",
            current_value=None,
            proposed_value="zone-1",
            rationale="test",
            confidence=0.5,
            status="proposed",
        )
        with pytest.raises(ValueError, match="must be 'accepted'"):
            apply_patch(context, patch)
