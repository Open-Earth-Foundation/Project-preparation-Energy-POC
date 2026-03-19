"""Client wrapper for the Geo-Layer-Viewer Express API.

Provides typed access to geospatial layer data for energy analysis.
See data/layers-energy-mapping.json for layer ID reference.
"""

import json
import os
from pathlib import Path
from typing import Any

import requests

BASE_URL = os.getenv("GEO_LAYER_VIEWER_URL", "http://localhost:5000")
LAYER_MAPPING_PATH = Path(__file__).parent.parent.parent / "data" / "layers-energy-mapping.json"


def _load_layer_mapping() -> dict:
    """Load layer-energy mapping from data/layers-energy-mapping.json."""
    with open(LAYER_MAPPING_PATH) as f:
        return json.load(f)["layers"]


def get_city_boundary(city_name: str = "Porto Alegre") -> dict:
    """Fetch city boundary GeoJSON from Geo-Layer-Viewer.

    Args:
        city_name: City name for OSM Nominatim lookup.

    Returns:
        GeoJSON polygon of city boundary.
    """
    resp = requests.get(f"{BASE_URL}/api/geospatial/boundary", params={"city": city_name})
    resp.raise_for_status()
    return resp.json()


def get_layer_data(layer_id: str, bounds: dict | None = None) -> dict:
    """Fetch GeoJSON data for a specific layer.

    Args:
        layer_id: Geo-Layer-Viewer layer ID (use layers-energy-mapping.json for reference).
        bounds: Optional bounding box to filter data.

    Returns:
        GeoJSON FeatureCollection or tile metadata.
    """
    params = {}
    if bounds:
        params.update(bounds)
    resp = requests.get(f"{BASE_URL}/api/geospatial/{layer_id}", params=params)
    resp.raise_for_status()
    return resp.json()


def get_solar_data() -> dict:
    """Fetch solar neighbourhood data (PVOUT, GHI, DNI per neighbourhood)."""
    resp = requests.get(f"{BASE_URL}/api/geospatial/solar-neighbourhoods")
    resp.raise_for_status()
    return resp.json()


def get_ibge_indicators() -> dict:
    """Fetch IBGE census indicators (socioeconomic data per tract)."""
    resp = requests.get(f"{BASE_URL}/api/geospatial/ibge-indicators")
    resp.raise_for_status()
    return resp.json()


def get_ibge_settlements() -> dict:
    """Fetch IBGE informal settlement locations."""
    resp = requests.get(f"{BASE_URL}/api/geospatial/ibge-settlements")
    resp.raise_for_status()
    return resp.json()


def get_sites(layer_type: str) -> dict:
    """Fetch OSM site data (parks, schools, hospitals, etc.).

    Args:
        layer_type: One of parks, schools, hospitals, wetlands, sports, social, vacant.
    """
    resp = requests.get(f"{BASE_URL}/api/geospatial/sites/{layer_type}")
    resp.raise_for_status()
    return resp.json()


def get_transit_stops() -> dict:
    """Fetch GTFS transit stop locations."""
    resp = requests.get(f"{BASE_URL}/api/geospatial/transit-stops")
    resp.raise_for_status()
    return resp.json()


def get_energy_relevant_layers() -> dict[str, dict]:
    """Return all layer IDs relevant to energy analysis, grouped by relevance.

    Returns:
        Dict with keys 'primary', 'secondary', 'constraint', 'context',
        each containing a list of layer config dicts.
    """
    mapping = _load_layer_mapping()
    grouped: dict[str, list] = {"primary": [], "secondary": [], "constraint": [], "context": []}
    for layer_id, config in mapping.items():
        relevance = config.get("relevance", "context")
        grouped.setdefault(relevance, []).append({"layerId": layer_id, **config})
    return grouped


def health_check() -> bool:
    """Check if Geo-Layer-Viewer API is reachable."""
    try:
        resp = requests.get(f"{BASE_URL}/api/geospatial/boundary", params={"city": "Porto Alegre"}, timeout=5)
        return resp.status_code == 200
    except requests.RequestException:
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test Geo-Layer-Viewer connection")
    parser.add_argument("--test", action="store_true", help="Run health check")
    args = parser.parse_args()

    if args.test:
        ok = health_check()
        print(f"Geo-Layer-Viewer at {BASE_URL}: {'OK' if ok else 'UNREACHABLE'}")

        mapping = _load_layer_mapping()
        print(f"Layer mapping loaded: {len(mapping)} layers")
