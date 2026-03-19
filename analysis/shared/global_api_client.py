"""Client wrapper for the CityCatalyst Global API.

Provides access to city emissions data and metadata.
API docs: https://ccglobal.openearth.dev
"""

import os

import requests

BASE_URL = os.getenv("GLOBAL_API_URL", "https://ccglobal.openearth.dev")


def get_city_emissions(
    locode: str,
    year: str,
    datasource_id: str = "ClimateTRACEv2025",
    gpc_ref: str = "I.1.1",
) -> dict:
    """Fetch emissions data for a city.

    Args:
        locode: UN/LOCODE (e.g., 'BR POA').
        year: Data year (e.g., '2022').
        datasource_id: Data source ID (e.g., 'ClimateTRACEv2025', 'SEEGv2023').
        gpc_ref: GPC reference number (e.g., 'I.1.1' for stationary energy).

    Returns:
        Emissions data dict.
    """
    resp = requests.get(
        f"{BASE_URL}/api/v0/climatetrace/city/{locode}/{year}/{datasource_id}",
        params={"gpc_ref": gpc_ref},
    )
    resp.raise_for_status()
    return resp.json()


def get_energy_sector_emissions(locode: str, year: str = "2022") -> dict:
    """Fetch stationary energy sector emissions for a city.

    GPC Sector I covers stationary energy (residential, commercial, institutional,
    manufacturing, energy industries, fugitive).

    Args:
        locode: UN/LOCODE (e.g., 'BR POA').
        year: Data year.

    Returns:
        Dict with emissions by GPC sub-sector.
    """
    gpc_refs = {
        "I.1.1": "Residential - Scope 1",
        "I.1.2": "Residential - Scope 2",
        "I.2.1": "Commercial/Institutional - Scope 1",
        "I.2.2": "Commercial/Institutional - Scope 2",
        "I.3.1": "Manufacturing - Scope 1",
        "I.3.2": "Manufacturing - Scope 2",
        "I.4.1": "Energy Industries - Scope 1",
        "I.5.1": "Agriculture/Forestry/Fishing - Scope 1",
        "I.6.1": "Non-specified - Scope 1",
    }

    results = {}
    for ref, name in gpc_refs.items():
        try:
            data = get_city_emissions(locode, year, gpc_ref=ref)
            results[ref] = {"name": name, "data": data}
        except requests.HTTPError:
            results[ref] = {"name": name, "data": None}

    return results


def health_check() -> bool:
    """Check if Global API is reachable."""
    try:
        resp = requests.get(f"{BASE_URL}/api/v0/datasource", timeout=5)
        return resp.status_code == 200
    except requests.RequestException:
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test CityCatalyst Global API connection")
    parser.add_argument("--test", action="store_true", help="Run health check")
    parser.add_argument("--locode", default="BR POA", help="City UN/LOCODE")
    args = parser.parse_args()

    if args.test:
        ok = health_check()
        print(f"Global API at {BASE_URL}: {'OK' if ok else 'UNREACHABLE'}")
