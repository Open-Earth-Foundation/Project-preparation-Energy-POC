# Action Selection module
# Evaluates and prioritizes energy actions based on context signals,
# scoring criteria, and action catalog archetypes.
#
# Flow: context/ + data/energy-action-catalog.json → scored action shortlist
# Output feeds into: site-selection (where to implement) and technology-selection (how)
#
# Extended with CityCatalyst Global API actions via ccglobal_extract.py:
#   data/research/ccglobal-energy-actions.json → normalized → merged catalog → scoring
