"""
Action scoring and prioritization.

Scores each action from the catalog against context signals using
weighted multi-criteria assessment. Produces a ranked action list
with recommendations (priority / include / conditional / defer).

Scoring criteria (default weights — adjustable per project):
  1. Context alignment (0.25) — how many supportive signals match
  2. Existing commitment alignment (0.20) — action aligns with city/state plans
  3. Impact potential (0.20) — emissions + co-benefits potential
  4. Financing readiness (0.15) — funder priorities match, archetypes available
  5. Implementation readiness (0.10) — prerequisites met, maturity tier
  6. Portfolio synergy (0.10) — action complements other high-scoring actions
"""

from typing import Any

# Default scoring criteria
DEFAULT_CRITERIA = [
    {"id": "context_alignment", "label": "Context Alignment", "weight": 0.25,
     "description": "How well action addresses identified problems and matches supportive signals"},
    {"id": "commitment_alignment", "label": "Existing Commitment Alignment", "weight": 0.20,
     "description": "Action aligns with city/state plans already in place"},
    {"id": "impact_potential", "label": "Impact Potential", "weight": 0.20,
     "description": "Emissions reduction + co-benefits (resilience, equity, cost savings)"},
    {"id": "financing_readiness", "label": "Financing Readiness", "weight": 0.15,
     "description": "Funder priorities match, financing archetypes available and suitable"},
    {"id": "implementation_readiness", "label": "Implementation Readiness", "weight": 0.10,
     "description": "Prerequisites achievable, technology proven, timeline feasible"},
    {"id": "portfolio_synergy", "label": "Portfolio Synergy", "weight": 0.10,
     "description": "Action complements other high-scoring actions in the portfolio"},
]


def score_context_alignment(action: dict, signals: dict) -> float:
    """Score 0-100 based on how many supportive context signals match."""
    supportive = action.get("contextSignals", {}).get("supportive", [])
    blocking = action.get("contextSignals", {}).get("blocking", [])

    if not supportive:
        return 50  # neutral if no signals defined

    # Count supportive signals that are present in context
    geo = signals.get("geographic", {})
    reg = signals.get("regulatory", {})
    fin = signals.get("financing", {})

    matched_supportive = 0
    for signal in supportive:
        # Simple keyword matching against context signals
        signal_lower = signal.lower()
        if "net metering" in signal_lower and reg.get("net_metering_active"):
            matched_supportive += 1
        elif "solar ghi" in signal_lower and geo.get("solar_ghi_kwh_m2_year", 0) > 1400:
            matched_supportive += 1
        elif "outage" in signal_lower and geo.get("grid_outage_frequency") == "high":
            matched_supportive += 1
        elif "flood" in signal_lower and geo.get("flood_risk") == "high":
            matched_supportive += 1
        elif "extreme weather" in signal_lower and geo.get("post_disaster_context"):
            matched_supportive += 1
        elif "energy poverty" in signal_lower and geo.get("energy_poverty_present"):
            matched_supportive += 1
        elif "tariff" in signal_lower:
            matched_supportive += 1  # assume high tariffs for Brazil
        elif "ppp" in signal_lower and reg.get("ppp_framework_available"):
            matched_supportive += 1
        elif "biometano" in signal_lower.replace("â", "a") or "biomethane" in signal_lower:
            matched_supportive += 1  # POA is in Pacto
        elif "climate" in signal_lower and reg.get("just_transition_plan_active"):
            matched_supportive += 1
        elif "post-disaster" in signal_lower and geo.get("post_disaster_context"):
            matched_supportive += 1

    # Check for blocking signals
    matched_blocking = 0
    for signal in blocking:
        signal_lower = signal.lower()
        if "utility unwilling" in signal_lower:
            # We don't know — leave as 0
            pass

    support_ratio = matched_supportive / len(supportive) if supportive else 0
    block_penalty = matched_blocking * 25

    return min(100, max(0, support_ratio * 100 - block_penalty))


def score_commitment_alignment(action: dict, commitments: list[str]) -> float:
    """Score 0-100 based on alignment with existing city/state commitments."""
    local_relevance = action.get("localRelevance", {}).get("portoAlegre", "")
    action_name = action.get("name", "").lower()

    score = 0
    for commitment in commitments:
        commitment_lower = commitment.lower()
        # Check if action keywords appear in commitments
        if any(keyword in commitment_lower for keyword in action_name.lower().split()):
            score += 30

        # Check local relevance text for commitment references
        if any(word in local_relevance.lower() for word in commitment_lower.split()[:3]):
            score += 10

    # Cap at 100 and boost if "in progress" or "active" in local relevance
    if "in progress" in local_relevance.lower() or "active" in local_relevance.lower():
        score += 20
    if "high" in local_relevance.lower()[:10]:
        score += 15
    if "critical" in local_relevance.lower()[:15]:
        score += 25

    return min(100, score)


def score_impact_potential(action: dict) -> float:
    """Score 0-100 based on emissions and co-benefits potential."""
    indicators = action.get("impactIndicators", {})
    score = 50  # baseline

    # Boost for multiple impact dimensions
    if indicators.get("emissionsReduction"):
        score += 15
    if indicators.get("costSavings"):
        score += 10
    if indicators.get("reliabilityImprovement"):
        score += 15
    if indicators.get("resilience"):
        score += 15
    if indicators.get("airQuality"):
        score += 10
    if indicators.get("beneficiaries"):
        score += 5

    return min(100, score)


def score_financing_readiness(action: dict, signals: dict) -> float:
    """Score 0-100 based on financing archetype availability and funder priority match."""
    fin = signals.get("financing", {})
    archetype_ids = action.get("financingArchetypeIds", [])
    funder_priorities = fin.get("funder_priority_categories", [])

    score = len(archetype_ids) * 15  # more financing options = better

    # Check if action category matches funder priorities
    category = action.get("category", "")
    for priority in funder_priorities:
        if priority in category or category in priority:
            score += 20
            break

    # Boost if proven maturity (easier to finance)
    if action.get("maturityTier") == "proven":
        score += 15
    elif action.get("maturityTier") == "scaling":
        score += 10

    return min(100, score)


def score_implementation_readiness(action: dict) -> float:
    """Score 0-100 based on maturity tier and prerequisite count."""
    maturity = action.get("maturityTier", "emerging")
    prerequisites = action.get("prerequisites", [])

    maturity_scores = {"proven": 80, "scaling": 60, "emerging": 40, "pilot": 25}
    score = maturity_scores.get(maturity, 40)

    # Fewer prerequisites = easier to implement
    prereq_penalty = max(0, (len(prerequisites) - 2) * 5)
    score -= prereq_penalty

    return min(100, max(0, score))


def score_actions(
    actions: list[dict],
    signals: dict,
    criteria: list[dict] | None = None,
) -> list[dict]:
    """
    Score all actions and return ranked list with recommendations.

    Args:
        actions: List of action dicts from energy-action-catalog.json
        signals: Output of context_signals.collect_all_signals()
        criteria: Optional override of scoring criteria weights

    Returns:
        List of evaluated action dicts, sorted by composite score descending
    """
    if criteria is None:
        criteria = DEFAULT_CRITERIA

    commitments = signals.get("existing_commitments", [])
    weight_map = {c["id"]: c["weight"] for c in criteria}

    evaluated = []
    for action in actions:
        scores = {
            "context_alignment": score_context_alignment(action, signals),
            "commitment_alignment": score_commitment_alignment(action, commitments),
            "impact_potential": score_impact_potential(action),
            "financing_readiness": score_financing_readiness(action, signals),
            "implementation_readiness": score_implementation_readiness(action),
            "portfolio_synergy": 50,  # placeholder — computed in second pass
        }

        composite = sum(scores[k] * weight_map.get(k, 0) for k in scores)

        # Determine recommendation tier
        if composite >= 70:
            recommendation = "priority"
        elif composite >= 55:
            recommendation = "include"
        elif composite >= 40:
            recommendation = "conditional"
        else:
            recommendation = "defer"

        evaluated.append({
            "actionId": action["id"],
            "name": action["name"],
            "category": action.get("category", ""),
            "compositeScore": round(composite, 1),
            "scoreBreakdown": {k: round(v, 1) for k, v in scores.items()},
            "recommendation": recommendation,
            "rationale": action.get("localRelevance", {}).get("portoAlegre", ""),
            "contextSignalsMatched": action.get("contextSignals", {}),
            "dependencies": [],
            "nextSteps": action.get("prerequisites", []),
        })

    # Sort by composite score descending
    evaluated.sort(key=lambda x: x["compositeScore"], reverse=True)

    return evaluated


def build_action_portfolio(evaluated: list[dict]) -> dict:
    """Build the recommended action portfolio from scored actions."""
    priority = [a["actionId"] for a in evaluated if a["recommendation"] == "priority"]
    complementary = [a["actionId"] for a in evaluated if a["recommendation"] == "include"]

    return {
        "priorityActions": priority,
        "complementaryActions": complementary,
        "portfolioRationale": (
            f"{len(priority)} priority actions identified based on context alignment, "
            f"existing commitments, and financing readiness. "
            f"{len(complementary)} complementary actions support the portfolio."
        ),
        "estimatedPortfolioImpact": {
            "totalEmissionsReduction": "To be computed from action-level estimates",
            "totalInvestmentRange": "To be computed from action-level CAPEX ranges",
            "totalBeneficiaries": "To be computed from action-level beneficiary estimates",
        },
    }
