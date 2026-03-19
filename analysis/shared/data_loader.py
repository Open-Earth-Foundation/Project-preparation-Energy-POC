"""Load and validate reference data from data/ directory."""

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent.parent.parent / "data"
SCHEMAS_DIR = Path(__file__).parent.parent.parent / "schemas"


def load_json(filename: str) -> dict:
    """Load a JSON file from the data/ directory.

    Args:
        filename: Filename relative to data/ (e.g., 'energy-tech-catalog.json').

    Returns:
        Parsed JSON dict.
    """
    filepath = DATA_DIR / filename
    with open(filepath) as f:
        return json.load(f)


def load_tech_catalog() -> list[dict]:
    """Load energy technology catalog."""
    data = load_json("energy-tech-catalog.json")
    return data["technologies"]


def load_constraints() -> list[dict]:
    """Load site constraint definitions."""
    data = load_json("site-constraint-types.json")
    return data["constraints"]


def load_scoring_weights() -> dict:
    """Load scoring weight configuration."""
    return load_json("scoring-weights.json")


def load_layer_mapping() -> dict[str, dict]:
    """Load layer-to-energy mapping."""
    data = load_json("layers-energy-mapping.json")
    return data["layers"]


def load_financing_archetypes() -> list[dict]:
    """Load financing archetype definitions."""
    data = load_json("financing-archetypes.json")
    return data["archetypes"]


def load_research(category: str | None = None) -> list[dict]:
    """Load research entries from data/research/.

    Args:
        category: Optional filter — 'benchmarks', 'policies', or 'case-studies'.

    Returns:
        List of research entry dicts.
    """
    research_dir = DATA_DIR / "research"
    entries = []

    dirs = [research_dir / category] if category else research_dir.iterdir()

    for subdir in dirs:
        if not subdir.is_dir():
            continue
        for filepath in subdir.glob("*.json"):
            with open(filepath) as f:
                entries.append(json.load(f))

    return entries


def validate_data_files() -> dict[str, bool]:
    """Validate that all expected data files exist and parse correctly.

    Returns:
        Dict mapping filename to validation status.
    """
    expected_files = [
        "energy-tech-catalog.json",
        "site-constraint-types.json",
        "scoring-weights.json",
        "layers-energy-mapping.json",
        "financing-archetypes.json",
    ]

    results = {}
    for filename in expected_files:
        try:
            load_json(filename)
            results[filename] = True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            results[filename] = False
            print(f"  FAIL: {filename} — {e}")

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate reference data files")
    parser.add_argument("--validate", action="store_true", help="Validate all data files")
    args = parser.parse_args()

    if args.validate:
        print("Validating data files...")
        results = validate_data_files()
        for name, ok in results.items():
            status = "OK" if ok else "FAIL"
            print(f"  {status}: {name}")

        total = len(results)
        passed = sum(1 for v in results.values() if v)
        print(f"\n{passed}/{total} files valid")
