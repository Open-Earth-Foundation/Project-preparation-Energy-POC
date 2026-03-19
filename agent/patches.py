"""Patch format and application logic for agent suggestions.

Patches follow the schema defined in schemas/patch.json.
All patches require human review before application.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Any

from analysis.shared.types import Patch


def create_patch(
    target_component: str,
    target_field: str,
    proposed_value: Any,
    rationale: str,
    confidence: float,
    current_value: Any = None,
    sources: list[str] | None = None,
) -> Patch:
    """Create a new patch proposal.

    Args:
        target_component: 'site-selection' or 'technology-selection'.
        target_field: Dot-path into the component (e.g., 'candidateZones.0.score').
        proposed_value: The value to set.
        rationale: Why this change is proposed.
        confidence: 0-1 confidence level.
        current_value: Current value (for display in review).
        sources: URLs or references supporting the patch.

    Returns:
        Patch object ready for review.
    """
    return Patch(
        id=str(uuid.uuid4()),
        target_component=target_component,
        target_field=target_field,
        current_value=current_value,
        proposed_value=proposed_value,
        rationale=rationale,
        confidence=confidence,
        sources=sources or [],
        status="proposed",
    )


def apply_patch(context: dict, patch: Patch) -> dict:
    """Apply an accepted patch to the project context.

    Only applies patches with status='accepted'. Navigates the dot-path
    to set the value in the context dict.

    Args:
        context: Project context dict.
        patch: Patch to apply (must have status='accepted').

    Returns:
        Updated context dict.

    Raises:
        ValueError: If patch status is not 'accepted'.
    """
    if patch.status != "accepted":
        raise ValueError(f"Cannot apply patch with status '{patch.status}' — must be 'accepted'")

    # Navigate dot-path
    parts = patch.target_field.split(".")
    target = context.get(patch.target_component, {})

    for part in parts[:-1]:
        if part.isdigit():
            target = target[int(part)]
        else:
            target = target.setdefault(part, {})

    # Set value
    final_key = parts[-1]
    if final_key.isdigit():
        target[int(final_key)] = patch.proposed_value
    else:
        target[final_key] = patch.proposed_value

    return context


def serialize_patches(patches: list[Patch]) -> str:
    """Serialize patches to JSON for storage or transmission."""
    from dataclasses import asdict
    return json.dumps([asdict(p) for p in patches], indent=2, default=str)


def deserialize_patches(json_str: str) -> list[dict]:
    """Deserialize patches from JSON."""
    return json.loads(json_str)
