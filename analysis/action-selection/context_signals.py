"""
Context signal extraction for action selection.

Reads baseline context documents and structured data to produce
a set of signals that inform action scoring. Signals are facts
derived from context — not scores themselves.

Example signals:
  - "grid_outage_frequency": "high" (from RS energy report)
  - "net_metering_active": True (from regulatory context)
  - "funder_priority_resilience": True (from financing context)
"""

import json
from pathlib import Path
from typing import Any

# Root of the repo
REPO_ROOT = Path(__file__).resolve().parents[2]
CONTEXT_DIR = REPO_ROOT / "context"
DATA_DIR = REPO_ROOT / "data"


def load_action_catalog() -> dict:
    """Load the energy action catalog."""
    with open(DATA_DIR / "energy-action-catalog.json") as f:
        return json.load(f)


def load_merged_catalog() -> dict:
    """
    Load the local energy action catalog merged with normalized CCGlobal actions.

    Returns the same structure as energy-action-catalog.json but with
    CCGlobal actions appended. Each CCGlobal action has source='ccglobal'.
    """
    from .ccglobal_extract import extract_all

    catalog = load_action_catalog()
    ccglobal_actions = extract_all()

    # Avoid duplicates — skip CCGlobal actions whose id already exists
    existing_ids = {a["id"] for a in catalog["actions"]}
    new_actions = [a for a in ccglobal_actions if a["id"] not in existing_ids]

    merged = dict(catalog)
    merged["actions"] = catalog["actions"] + new_actions
    merged["_ccglobal"] = {
        "addedCount": len(new_actions),
        "skippedDuplicates": len(ccglobal_actions) - len(new_actions),
    }
    return merged


def extract_geographic_signals(city_locode: str) -> dict[str, Any]:
    """
    Extract signals from geographic context documents.

    For MVP, returns a manually curated set of signals for Porto Alegre.
    Future: parse context markdown files or use agent-extracted structured data.
    """
    signals = {}

    if city_locode == "BR POA":
        signals = {
            "solar_ghi_kwh_m2_year": 1600,  # moderate-high for Brazil
            "grid_outage_frequency": "high",  # Jan 2024 storm, May 2024 floods
            "flood_risk": "high",  # historic flooding May 2024
            "renewable_share_state": 0.875,  # 87.5% renewable in RS
            "coal_dependency": True,  # Candiota III + Pampa Sul
            "post_disaster_context": True,  # May 2024 floods
            "population": 1490000,
            "energy_poverty_present": True,
        }

    return signals


def extract_regulatory_signals(city_locode: str) -> dict[str, Any]:
    """
    Extract signals from regulatory context.

    For MVP, returns known regulatory facts for Brazil/RS/POA.
    Future: read from context/regulatory/ structured files.
    """
    signals = {}

    if city_locode.startswith("BR"):
        signals = {
            "net_metering_active": True,  # Brazil MMGD program
            "net_metering_under_review": True,  # policy may change
            "ppp_framework_available": True,
            "just_transition_plan_active": True,  # RS TEJ plan
            "environmental_licensing_required": True,
        }

    return signals


def extract_financing_signals(city_locode: str) -> dict[str, Any]:
    """
    Extract signals from financing context.

    For MVP, returns known funder priorities.
    Future: read from context/financing/ structured files.
    """
    signals = {}

    if city_locode == "BR POA":
        signals = {
            "dfi_interest_resilience": True,  # post-flood recovery
            "climate_fund_eligibility": True,  # GCF, GEF eligible
            "green_bond_feasible": True,  # Brazil has framework
            "municipal_budget_constrained": True,  # post-flood fiscal pressure
            "funder_priority_categories": [
                "resilience", "just_transition", "renewable_energy", "transport_electrification"
            ],
        }

    return signals


def extract_existing_commitments(city_locode: str) -> list[str]:
    """
    Extract existing plans and commitments from context.

    These are things the city/state has already committed to —
    actions aligned with these get a boost.
    """
    commitments = []

    if city_locode == "BR POA":
        commitments = [
            "PLAC: 100 electric buses",
            "PLAC: renewable procurement for 60 public facilities",
            "PLAC: LED lighting and building retrofits",
            "PLAC: drainage and flood protection (R$6B)",
            "Pacto do Biometano participation",
            "RS Just Energy Transition Plan (TEJ)",
            "RS Book of Opportunities: 4.3 GW renewable pipeline",
        ]

    return commitments


def collect_all_signals(city_locode: str) -> dict:
    """Collect all context signals for a city into a single dict."""
    return {
        "geographic": extract_geographic_signals(city_locode),
        "regulatory": extract_regulatory_signals(city_locode),
        "financing": extract_financing_signals(city_locode),
        "existing_commitments": extract_existing_commitments(city_locode),
    }
