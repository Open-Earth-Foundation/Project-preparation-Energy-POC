"""Generate concept brief combining site and technology analysis.

Reads both site selection and technology selection results to produce
a concise pre-feasibility concept brief.

Usage:
    python -m outputs.generators.concept_brief --project <id>
"""

from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "concept-brief.md"


def generate_concept_brief(
    project_name: str,
    city_name: str,
    country: str,
    site_results: dict,
    tech_results: dict,
    research_findings: list[dict] | None = None,
) -> str:
    """Generate a concept brief document.

    Args:
        project_name: Project display name.
        city_name: City name.
        country: Country name.
        site_results: Site selection outputs (top zone, score, characteristics).
        tech_results: Technology selection outputs (shortlist, sizing, costs).
        research_findings: Optional research entries to cite.

    Returns:
        Populated markdown string.
    """
    with open(TEMPLATE_PATH) as f:
        template = f.read()

    # TODO: Populate template variables from combined results
    return template


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate concept brief")
    parser.add_argument("--project", help="Project ID")
    args = parser.parse_args()

    print("Concept brief generator")
    print("Requires results from both site selection and technology selection pipelines")
