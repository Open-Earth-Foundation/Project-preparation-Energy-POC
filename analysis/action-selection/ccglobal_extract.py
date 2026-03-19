"""
Extract and normalize CityCatalyst Global API energy actions
into the local energy-action-catalog format.

Source: data/research/ccglobal-energy-actions.json
Target format: same schema as data/energy-action-catalog.json actions

Usage:
    python -m analysis.action-selection.ccglobal_extract [--output FILE]
"""

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
CCGLOBAL_PATH = REPO_ROOT / "data" / "research" / "ccglobal-energy-actions.json"

# Map CCGlobal subsectors to local sector codes + labels
SUBSECTOR_MAP = {
    "residential_buildings": ("I.1", "Residential"),
    "commercial_and_institutional_buildings_and_facilities": ("I.2", "Commercial/Institutional"),
    "manufacturing_industries_and_construction": ("I.3", "Manufacturing/Construction"),
    "energy_industries": ("I.4", "Energy Industries"),
    "energy_generation_supplied_to_the_grid": ("I.4.4", "Grid-supplied Generation"),
    "agriculture_forestry_and_fishing_activities": ("I.5", "Agriculture/Forestry"),
    "non-specified_sources": ("I.6", "Non-specified"),
}

# Map CCGlobal action_subcategory to local category
CATEGORY_MAP = {
    "Energy & Building Retrofits": "efficiency",
    "Infrastructure Development": "infrastructure",
    "Regulation & Standards": "policy",
    "Public Programs / Incentives": "policy",
    "Strategic Plans": "policy",
}

# Map cost to maturity heuristic (rough — cost alone doesn't determine maturity,
# but combined with timeline it's a reasonable proxy for pre-feasibility)
TIMELINE_MATURITY_MAP = {
    "<5 years": "proven",
    "5-10 years": "scaling",
    ">10 years": "emerging",
}

# Map GHG reduction range strings to numeric midpoints for scoring
GHG_RANGE_MIDPOINTS = {
    "0-19": 10,
    "20-39": 30,
    "40-59": 50,
    "60-79": 70,
    "80-100": 90,
}


def load_ccglobal_actions() -> dict:
    """Load raw CCGlobal energy actions from research data."""
    with open(CCGLOBAL_PATH) as f:
        return json.load(f)


def _infer_context_signals(action: dict) -> dict[str, list[str]]:
    """Infer supportive/blocking signals from CCGlobal action fields."""
    supportive = []
    subsector = action.get("subsector", "")
    desc = action.get("description", "").lower()

    # Solar-related
    if "solar" in desc:
        supportive.append("Solar GHI > 1400 kWh/m2/year")
    if "pv" in desc or "photovoltaic" in desc:
        supportive.append("Net metering policy active (Brazil MMGD)")

    # Grid / resilience
    if "grid" in desc or "substation" in desc or "distribution" in desc:
        supportive.append("High outage frequency (SAIDI > 20 hours/year)")
    if "microgrid" in desc or "storage" in desc or "resilience" in desc:
        supportive.append("Recent extreme weather events causing grid failures")

    # Building efficiency
    if "retrofit" in desc or "efficiency" in desc or "insulation" in desc:
        supportive.append("High electricity tariffs (>0.12 USD/kWh)")
    if "building" in desc and "standard" in desc:
        supportive.append("Municipal climate action plan commitment")

    # Biogas / biomethane
    if "biogas" in desc or "biomethane" in desc or "biodigester" in desc:
        supportive.append("Existing Pacto de Biometano participation")

    # Industrial
    if subsector == "manufacturing_industries_and_construction":
        supportive.append("High electricity tariffs (>0.12 USD/kWh)")

    # LED / lighting
    if "led" in desc or "lighting" in desc:
        supportive.append("PPP framework available for ESCO model")

    # Energy poverty
    if "rural" in desc or "peri-urban" in desc or "low-income" in desc:
        supportive.append("High energy poverty rate")

    # Post-disaster
    if "flood" in desc or "storm" in desc:
        supportive.append("Post-disaster reconstruction context")

    return {
        "supportive": supportive if supportive else ["General energy sector alignment"],
        "blocking": [],
    }


def _infer_impact_indicators(action: dict) -> dict[str, Any]:
    """Build impact indicators from CCGlobal GHG reduction potential."""
    ghg = action.get("ghg_reduction_potential", {})
    indicators = {}

    for sector, range_str in ghg.items():
        midpoint = GHG_RANGE_MIDPOINTS.get(range_str, 0)
        indicators["emissionsReduction"] = {
            "range": f"{range_str}% reduction potential",
            "basis": f"CCGlobal estimate for {sector}",
        }

    desc = action.get("description", "").lower()
    if any(kw in desc for kw in ["cost", "savings", "tariff", "bill"]):
        indicators["costSavings"] = {"range": "Estimated", "basis": "Description implies cost savings"}
    if any(kw in desc for kw in ["resilience", "reliable", "outage", "backup"]):
        indicators["reliabilityImprovement"] = {"range": "Estimated", "basis": "Description implies reliability gains"}

    return indicators


def normalize_action(action: dict) -> dict:
    """
    Convert a single CCGlobal action into the local catalog format.

    CCGlobal fields → local catalog fields:
      action_id → id
      action_name → name
      subsector → sector, sectorLabel
      action_subcategory → category
      description → description
      cost_investment_needed → (used for financing heuristics)
      timeline_for_implementation → implementationTimeline, maturityTier
      ghg_reduction_potential → impactIndicators
    """
    subsector = action.get("subsector", "non-specified_sources")
    sector_code, sector_label = SUBSECTOR_MAP.get(subsector, ("I.6", "Non-specified"))
    subcategory = action.get("action_subcategory", "")
    category = CATEGORY_MAP.get(subcategory, "other")
    timeline = action.get("timeline_for_implementation", "5-10 years")
    maturity = TIMELINE_MATURITY_MAP.get(timeline, "scaling")
    cost = action.get("cost_investment_needed", "medium")

    # Financing archetypes based on cost level
    financing = []
    if cost == "low":
        financing = ["municipal-budget"]
    elif cost == "medium":
        financing = ["municipal-budget", "climate-fund-grant"]
    else:
        financing = ["dfi-concessional", "climate-fund-grant", "green-bond"]

    return {
        "id": action["action_id"],
        "name": action["action_name"],
        "category": category,
        "sector": sector_code,
        "sectorLabel": sector_label,
        "description": action.get("description", ""),
        "source": "ccglobal",
        "sourceCategory": action.get("action_category", ""),
        "sourceSubcategory": subcategory,
        "typicalScale": None,
        "technologyIds": [],
        "financingArchetypeIds": financing,
        "prerequisites": [],
        "impactIndicators": _infer_impact_indicators(action),
        "contextSignals": _infer_context_signals(action),
        "localRelevance": {
            "portoAlegre": "",  # to be enriched by agent or manual review
        },
        "maturityTier": maturity,
        "implementationTimeline": timeline,
        "costLevel": cost,
        "ghgReductionPotential": action.get("ghg_reduction_potential", {}),
    }


def extract_all() -> list[dict]:
    """Load CCGlobal research data and return normalized action list."""
    raw = load_ccglobal_actions()
    actions = []
    for source_key in ("c40", "icare", "ipcc"):
        for action in raw.get("actions", {}).get(source_key, []):
            actions.append(normalize_action(action))
    return actions


def extract_with_metadata() -> dict:
    """Return full extraction result with metadata."""
    raw = load_ccglobal_actions()
    actions = extract_all()
    return {
        "source": raw.get("_metadata", {}),
        "totalExtracted": len(actions),
        "actions": actions,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Extract and normalize CCGlobal energy actions")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    args = parser.parse_args()

    result = extract_with_metadata()

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Extracted {result['totalExtracted']} actions to {args.output}")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
