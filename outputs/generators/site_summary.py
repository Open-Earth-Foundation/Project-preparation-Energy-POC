"""Generate site assessment summary from analysis results.

Reads scored zones and populates the site-summary template.

Usage:
    python -m outputs.generators.site_summary
"""

from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "site-summary.md"


def generate_site_summary(
    city_name: str,
    city_locode: str,
    scored_zones: list,
    total_zones_analyzed: int,
    constraints_applied: list[dict],
    layers_used: list[dict],
) -> str:
    """Generate a site assessment summary document.

    Args:
        city_name: City display name.
        city_locode: UN/LOCODE.
        scored_zones: List of ScoredZone objects (top N).
        total_zones_analyzed: Total zones before filtering.
        constraints_applied: Constraint definitions used.
        layers_used: Layer configs used in analysis.

    Returns:
        Populated markdown string.
    """
    with open(TEMPLATE_PATH) as f:
        template = f.read()

    # TODO: Populate template variables from analysis results
    # For now, return the template with placeholder markers
    return template


if __name__ == "__main__":
    print("Site summary generator")
    print("Requires analysis results from the site selection pipeline")
