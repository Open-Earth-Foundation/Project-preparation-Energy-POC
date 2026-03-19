"""
Run action selection for a city.

Usage:
    python -m analysis.action-selection.run_action_selection --city "BR POA"

Reads context signals and action catalog, scores all actions,
and outputs the ranked action portfolio to stdout as JSON.
"""

import argparse
import json
import sys
from datetime import datetime, timezone

from .context_signals import collect_all_signals, load_action_catalog
from .action_scoring import score_actions, build_action_portfolio, DEFAULT_CRITERIA


def run(city_locode: str) -> dict:
    """Run action selection and return the full output conforming to action-selection schema."""
    # Load inputs
    catalog = load_action_catalog()
    actions = catalog["actions"]
    signals = collect_all_signals(city_locode)

    # Score and rank
    evaluated = score_actions(actions, signals)
    portfolio = build_action_portfolio(evaluated)

    # Build context summary from signals
    context_summary = {
        "keyProblems": [],
        "existingCommitments": signals.get("existing_commitments", []),
        "funderPriorities": signals.get("financing", {}).get("funder_priority_categories", []),
        "regulatoryEnablers": [],
    }

    geo = signals.get("geographic", {})
    if geo.get("grid_outage_frequency") == "high":
        context_summary["keyProblems"].append("High grid outage frequency — storm/flood vulnerability")
    if geo.get("coal_dependency"):
        context_summary["keyProblems"].append("Coal dependency for dispatchable power (Candiota III, Pampa Sul)")
    if geo.get("post_disaster_context"):
        context_summary["keyProblems"].append("Post-disaster recovery context (May 2024 floods)")
    if geo.get("energy_poverty_present"):
        context_summary["keyProblems"].append("Energy poverty in vulnerable neighborhoods")

    reg = signals.get("regulatory", {})
    if reg.get("net_metering_active"):
        context_summary["regulatoryEnablers"].append("Net metering (MMGD) active")
    if reg.get("ppp_framework_available"):
        context_summary["regulatoryEnablers"].append("PPP framework available")
    if reg.get("just_transition_plan_active"):
        context_summary["regulatoryEnablers"].append("Just Energy Transition Plan (TEJ) active at state level")

    # Assemble output
    output = {
        "cityLocode": city_locode,
        "contextSummary": context_summary,
        "scoringCriteria": DEFAULT_CRITERIA,
        "evaluatedActions": evaluated,
        "actionPortfolio": portfolio,
        "summary": {
            "totalActionsEvaluated": len(evaluated),
            "priorityCount": len(portfolio["priorityActions"]),
            "analysisDate": datetime.now(timezone.utc).isoformat(),
            "notes": f"Action selection for {city_locode} using energy-action-catalog v{catalog['version']}",
        },
    }

    return output


def main():
    parser = argparse.ArgumentParser(description="Run action selection for a city")
    parser.add_argument("--city", required=True, help="UN/LOCODE (e.g., 'BR POA')")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    args = parser.parse_args()

    result = run(args.city)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Output written to {args.output}")
    else:
        json.dump(result, sys.stdout, indent=2)
        print()  # trailing newline


if __name__ == "__main__":
    main()
