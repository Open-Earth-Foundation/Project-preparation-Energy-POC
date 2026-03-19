"""Match energy technologies to site characteristics.

Filters the technology catalog by site requirements and scores
each applicable technology.

Usage:
    python -m analysis.technology_selection.tech_matching --site <zone_id>

Inputs:
    - Site characteristics from site selection
    - Technology catalog from data/energy-tech-catalog.json

Outputs:
    - Ranked list of applicable technologies with feasibility scores
"""

from analysis.shared.data_loader import load_tech_catalog
from analysis.shared.types import (
    FloodRisk,
    BuiltUpDensity,
    SiteCharacteristics,
    TechnologyCategory,
    TechnologyMatch,
    Range,
)


FLOOD_RISK_ORDER = {FloodRisk.NONE: 0, FloodRisk.LOW: 1, FloodRisk.MEDIUM: 2, FloodRisk.HIGH: 3}
DENSITY_ORDER = {BuiltUpDensity.RURAL: 0, BuiltUpDensity.SUBURBAN: 1, BuiltUpDensity.URBAN: 2, BuiltUpDensity.DENSE_URBAN: 3}


def check_site_requirements(tech: dict, site: SiteCharacteristics) -> tuple[bool, list[str]]:
    """Check if a technology's site requirements are met.

    Args:
        tech: Technology entry from energy-tech-catalog.json.
        site: Site characteristics.

    Returns:
        Tuple of (is_applicable, list_of_issues).
    """
    reqs = tech.get("siteRequirements", {})
    issues = []

    # Solar resource check
    min_ghi = reqs.get("minSolarGHI")
    if min_ghi and site.solar_ghi and site.solar_ghi < min_ghi:
        issues.append(f"Insufficient solar resource: GHI {site.solar_ghi} < {min_ghi} kWh/m2/year")

    # Flood risk check
    max_flood = reqs.get("maxFloodRisk")
    if max_flood:
        max_level = FLOOD_RISK_ORDER.get(FloodRisk(max_flood), 0)
        site_level = FLOOD_RISK_ORDER.get(site.flood_risk, 0)
        if site_level > max_level:
            issues.append(f"Flood risk too high: {site.flood_risk.value} > {max_flood}")

    # Land cover check
    excluded = reqs.get("excludedLandCover", [])
    if site.land_cover_type and site.land_cover_type in excluded:
        issues.append(f"Excluded land cover: {site.land_cover_type}")

    # Area check
    min_area = reqs.get("minAreaM2")
    if min_area and site.area_m2 > 0 and site.area_m2 < min_area:
        issues.append(f"Insufficient area: {site.area_m2}m2 < {min_area}m2")

    # Hard fail if any issue exists for hard requirements
    is_applicable = len(issues) == 0
    return is_applicable, issues


def estimate_sizing(tech: dict, site: SiteCharacteristics) -> dict:
    """Estimate pre-feasibility sizing ranges for a technology at a site.

    Args:
        tech: Technology entry from catalog.
        site: Site characteristics.

    Returns:
        Dict with capacity_range, estimated_output, area_required.
    """
    sizing = {}

    area_per_mw = tech.get("areaPerMW")
    if area_per_mw and site.area_m2 > 0:
        # Capacity based on available area
        max_cap = site.area_m2 / area_per_mw["min"]  # MW, optimistic
        min_cap = site.area_m2 / area_per_mw["max"]  # MW, conservative
        sizing["capacity_range"] = {"min": round(min_cap, 2), "max": round(max_cap, 2), "unit": "MW"}

    cap_factor = tech.get("capacityFactor")
    if cap_factor and "capacity_range" in sizing:
        hours_per_year = 8760
        min_output = sizing["capacity_range"]["min"] * 1000 * cap_factor["min"] * hours_per_year
        max_output = sizing["capacity_range"]["max"] * 1000 * cap_factor["max"] * hours_per_year
        sizing["estimated_output"] = {"min": round(min_output), "max": round(max_output), "unit": "MWh/year"}

    return sizing


def match_technologies(site: SiteCharacteristics) -> list[TechnologyMatch]:
    """Match all applicable technologies to a site.

    Args:
        site: Site characteristics.

    Returns:
        Sorted list of TechnologyMatch objects (highest feasibility first).
    """
    catalog = load_tech_catalog()
    matches = []

    for tech in catalog:
        is_applicable, issues = check_site_requirements(tech, site)

        if not is_applicable:
            continue

        sizing = estimate_sizing(tech, site)

        capex = tech.get("capexRange")
        lcoe = tech.get("lcoeRange")

        match = TechnologyMatch(
            technology_id=tech["id"],
            name=tech["name"],
            category=TechnologyCategory(tech["category"]),
            feasibility_score=75.0,  # TODO: implement detailed scoring
            capacity_range=Range(**sizing["capacity_range"]) if "capacity_range" in sizing else None,
            estimated_output=Range(**sizing["estimated_output"]) if "estimated_output" in sizing else None,
            capex_range=Range(**capex) if capex else None,
            lcoe_range=Range(**lcoe) if lcoe else None,
            rationale=tech.get("applicability", ""),
            risks=[],
        )
        matches.append(match)

    matches.sort(key=lambda m: m.feasibility_score, reverse=True)
    return matches


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Match technologies to site characteristics")
    parser.add_argument("--site", help="Zone/site ID")
    args = parser.parse_args()

    print("Technology matching")
    print("Run with site characteristics from site selection pipeline")
