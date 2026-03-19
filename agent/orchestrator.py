"""Agent orchestrator for energy project preparation.

Reads project context and geo data, calls LLM with prompt templates,
and returns structured patches for human review.

Usage:
    python -m agent.orchestrator --prompt site-analysis --city "Porto Alegre"
"""

import json
import os
from pathlib import Path
from typing import Any

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(prompt_name: str, variables: dict[str, str] | None = None) -> str:
    """Load and populate a prompt template.

    Args:
        prompt_name: Name of the prompt file (without .md extension).
        variables: Template variables to substitute (e.g., {{city_name}}).

    Returns:
        Populated prompt string.
    """
    filepath = PROMPTS_DIR / f"{prompt_name}.md"
    with open(filepath) as f:
        template = f.read()

    if variables:
        for key, value in variables.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))

    return template


def prepare_context(city_locode: str = "BR POA") -> dict[str, Any]:
    """Gather project context for agent consumption.

    Loads reference data, research, and any existing analysis results.

    Args:
        city_locode: UN/LOCODE for the target city.

    Returns:
        Context dict with all relevant data for agent prompts.
    """
    from analysis.shared.data_loader import (
        load_tech_catalog,
        load_constraints,
        load_scoring_weights,
        load_layer_mapping,
        load_research,
    )

    return {
        "city_locode": city_locode,
        "tech_catalog": load_tech_catalog(),
        "constraints": load_constraints(),
        "scoring_weights": load_scoring_weights(),
        "layer_mapping": load_layer_mapping(),
        "research": load_research(),
    }


def call_llm(prompt: str, context: dict, model: str | None = None) -> str:
    """Call the LLM with a prompt and context.

    Args:
        prompt: The populated prompt template.
        context: Project context to include in the request.
        model: LLM model to use. Defaults to env LLM_MODEL.

    Returns:
        LLM response text.
    """
    model = model or os.getenv("LLM_MODEL", "claude-sonnet-4-6")

    # TODO: Implement actual LLM call via Anthropic API
    # For now, return a placeholder
    raise NotImplementedError(
        "LLM integration not yet implemented. "
        "Set ANTHROPIC_API_KEY and implement call_llm() with the Anthropic SDK."
    )


def run_agent(
    prompt_name: str,
    city_name: str = "Porto Alegre",
    city_locode: str = "BR POA",
    extra_variables: dict[str, str] | None = None,
) -> dict:
    """Run an agent with a specific prompt template.

    Args:
        prompt_name: Prompt template name (e.g., 'site-analysis').
        city_name: City display name.
        city_locode: UN/LOCODE.
        extra_variables: Additional template variables.

    Returns:
        Dict with agent response and proposed patches.
    """
    variables = {"city_name": city_name, **(extra_variables or {})}
    prompt = load_prompt(prompt_name, variables)
    context = prepare_context(city_locode)

    response = call_llm(prompt, context)

    return {
        "prompt_name": prompt_name,
        "city": city_name,
        "response": response,
        "patches": [],  # TODO: Parse structured patches from response
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run energy project preparation agent")
    parser.add_argument("--prompt", required=True, help="Prompt template name")
    parser.add_argument("--city", default="Porto Alegre", help="City name")
    args = parser.parse_args()

    print(f"Running agent with prompt: {args.prompt}")
    print(f"City: {args.city}")
    print("Note: LLM integration not yet implemented. Set ANTHROPIC_API_KEY to enable.")
