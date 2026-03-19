"""Generate technology shortlist from analysis results.

Reads technology matches and populates the tech-shortlist template.

Usage:
    python -m outputs.generators.tech_shortlist
"""

from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "tech-shortlist.md"


def generate_tech_shortlist(
    city_name: str,
    zone_name: str,
    zone_score: float,
    site_characteristics: dict,
    technology_matches: list,
) -> str:
    """Generate a technology shortlist document.

    Args:
        city_name: City display name.
        zone_name: Selected zone name.
        zone_score: Zone score from site selection.
        site_characteristics: Site properties dict.
        technology_matches: List of TechnologyMatch objects.

    Returns:
        Populated markdown string.
    """
    with open(TEMPLATE_PATH) as f:
        template = f.read()

    # TODO: Populate template variables from analysis results
    return template


if __name__ == "__main__":
    print("Tech shortlist generator")
    print("Requires analysis results from the technology selection pipeline")
