"""Identify candidate zones from geospatial layers.

Divides the study area into analysis zones (neighbourhoods or grid cells)
and extracts layer values for each zone.

Usage:
    python -m analysis.site_selection.candidate_zones --city "Porto Alegre"

Inputs:
    - City boundary from Geo-Layer-Viewer
    - Layer data for energy-relevant layers (see data/layers-energy-mapping.json)

Outputs:
    - List of candidate zones with extracted layer values
"""

from analysis.shared.geo_client import get_city_boundary, get_solar_data, get_ibge_indicators
from analysis.shared.data_loader import load_layer_mapping
from analysis.shared.types import SiteCharacteristics


def get_candidate_zones(city_name: str = "Porto Alegre") -> list[dict]:
    """Identify candidate zones within a city boundary.

    Uses neighbourhood boundaries from solar data as the base unit,
    enriched with additional layer values.

    Args:
        city_name: City name for boundary lookup.

    Returns:
        List of zone dicts with id, name, geometry, and layer values.
    """
    # Fetch base data
    boundary = get_city_boundary(city_name)
    solar_data = get_solar_data()
    ibge_data = get_ibge_indicators()

    # Use solar neighbourhoods as zone units (they have boundaries + solar values)
    zones = []
    for feature in solar_data.get("features", []):
        props = feature.get("properties", {})
        zone = {
            "id": props.get("id", f"zone-{len(zones)}"),
            "name": props.get("name", f"Zone {len(zones)}"),
            "geometry": feature.get("geometry"),
            "layer_values": {
                "solar_ghi": props.get("ghi"),
                "solar_dni": props.get("dni"),
                "solar_pvout": props.get("pvout"),
            },
        }
        zones.append(zone)

    return zones


def extract_site_characteristics(zone: dict) -> SiteCharacteristics:
    """Convert a raw zone dict to a typed SiteCharacteristics object.

    Args:
        zone: Zone dict from get_candidate_zones().

    Returns:
        SiteCharacteristics with available values populated.
    """
    lv = zone.get("layer_values", {})
    return SiteCharacteristics(
        zone_id=zone["id"],
        name=zone["name"],
        area_m2=0,  # TODO: calculate from geometry
        solar_ghi=lv.get("solar_ghi"),
        solar_dni=lv.get("solar_dni"),
        solar_pvout=lv.get("solar_pvout"),
        geometry=zone.get("geometry"),
    )


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Identify candidate zones for energy projects")
    parser.add_argument("--city", default="Porto Alegre", help="City name")
    args = parser.parse_args()

    zones = get_candidate_zones(args.city)
    print(f"Found {len(zones)} candidate zones in {args.city}")
    print(json.dumps(zones[:3], indent=2, default=str))
