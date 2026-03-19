"""Pre-feasibility sizing estimates for energy technologies.

Produces indicative capacity, output, area, and cost ranges.
NOT engineering design — uses archetype parameters and rules of thumb.

Usage:
    python -m analysis.technology_selection.sizing_estimates

Inputs:
    - Technology match from tech_matching.py
    - Site characteristics

Outputs:
    - Sizing ranges per technology-site combination
"""

from analysis.shared.types import SiteCharacteristics, TechnologyMatch, Range


def estimate_solar_pv_ground(site: SiteCharacteristics) -> dict:
    """Estimate ground-mount solar PV sizing for a site.

    Rules of thumb:
    - Area: 10,000-20,000 m2/MW
    - Capacity factor: 15-25% (depends on GHI)
    - CAPEX: $700-1,200/kW
    """
    if site.area_m2 <= 0:
        return {"error": "No area data available"}

    # Capacity range
    cap_min_mw = site.area_m2 / 20_000  # Conservative m2/MW
    cap_max_mw = site.area_m2 / 10_000  # Efficient m2/MW

    # Adjust capacity factor for solar resource
    if site.solar_ghi and site.solar_ghi > 1600:
        cf_min, cf_max = 0.18, 0.25
    elif site.solar_ghi and site.solar_ghi > 1400:
        cf_min, cf_max = 0.16, 0.22
    else:
        cf_min, cf_max = 0.15, 0.20

    # Annual output
    hours = 8760
    output_min = cap_min_mw * 1000 * cf_min * hours  # MWh/year
    output_max = cap_max_mw * 1000 * cf_max * hours

    # CAPEX
    capex_min = cap_min_mw * 1000 * 700  # USD
    capex_max = cap_max_mw * 1000 * 1200

    return {
        "technology": "solar-pv-ground",
        "capacity": {"min": round(cap_min_mw, 2), "max": round(cap_max_mw, 2), "unit": "MWp"},
        "annual_output": {"min": round(output_min), "max": round(output_max), "unit": "MWh/year"},
        "capex": {"min": round(capex_min), "max": round(capex_max), "unit": "USD"},
        "capacity_factor": {"min": cf_min, "max": cf_max},
        "area_used": {"min": site.area_m2 * 0.5, "max": site.area_m2 * 0.8, "unit": "m2"},
        "assumptions": [
            f"Available area: {site.area_m2:,.0f} m2",
            f"Solar GHI: {site.solar_ghi or 'unknown'} kWh/m2/year",
            "Area efficiency: 10,000-20,000 m2/MW",
            "CAPEX: $700-1,200/kW (2024 Brazil estimates)",
        ],
    }


def estimate_solar_pv_rooftop(site: SiteCharacteristics, roof_area_m2: float = 0) -> dict:
    """Estimate rooftop solar PV sizing.

    Args:
        site: Site characteristics.
        roof_area_m2: Estimated available roof area. If 0, uses a fraction of built-up area.
    """
    if roof_area_m2 <= 0:
        # Rule of thumb: 10-20% of built-up area may be suitable for rooftop PV
        roof_area_m2 = site.area_m2 * 0.15

    cap_min_kw = roof_area_m2 / 10  # Conservative 10 m2/kW
    cap_max_kw = roof_area_m2 / 6   # Efficient 6 m2/kW

    return {
        "technology": "solar-pv-rooftop",
        "capacity": {"min": round(cap_min_kw), "max": round(cap_max_kw), "unit": "kWp"},
        "capex": {
            "min": round(cap_min_kw * 900),
            "max": round(cap_max_kw * 1800),
            "unit": "USD",
        },
        "assumptions": [
            f"Estimated roof area: {roof_area_m2:,.0f} m2",
            "Area efficiency: 6-10 m2/kWp",
            "CAPEX: $900-1,800/kW",
        ],
    }
