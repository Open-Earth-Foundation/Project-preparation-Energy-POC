"""Tests for technology matching logic."""

import pytest

from analysis.technology_selection.tech_matching import check_site_requirements, match_technologies
from analysis.shared.types import SiteCharacteristics, FloodRisk, BuiltUpDensity


class TestCheckSiteRequirements:
    def test_solar_ground_good_site(self):
        tech = {
            "id": "solar-pv-ground",
            "siteRequirements": {
                "minSolarGHI": 1400,
                "maxFloodRisk": "low",
                "excludedLandCover": ["forest", "wetland", "water"],
                "minAreaM2": 10000,
            },
        }
        site = SiteCharacteristics(
            zone_id="z1",
            name="Good Site",
            area_m2=50000,
            solar_ghi=1600,
            flood_risk=FloodRisk.NONE,
            land_cover_type="grassland",
        )
        is_ok, issues = check_site_requirements(tech, site)
        assert is_ok
        assert len(issues) == 0

    def test_solar_ground_insufficient_ghi(self):
        tech = {
            "id": "solar-pv-ground",
            "siteRequirements": {"minSolarGHI": 1400},
        }
        site = SiteCharacteristics(
            zone_id="z2",
            name="Low Solar",
            area_m2=50000,
            solar_ghi=1100,
        )
        is_ok, issues = check_site_requirements(tech, site)
        assert not is_ok
        assert any("solar resource" in i.lower() for i in issues)

    def test_solar_ground_high_flood_risk(self):
        tech = {
            "id": "solar-pv-ground",
            "siteRequirements": {"maxFloodRisk": "low"},
        }
        site = SiteCharacteristics(
            zone_id="z3",
            name="Flood Zone",
            area_m2=50000,
            flood_risk=FloodRisk.HIGH,
        )
        is_ok, issues = check_site_requirements(tech, site)
        assert not is_ok

    def test_solar_ground_excluded_land_cover(self):
        tech = {
            "id": "solar-pv-ground",
            "siteRequirements": {"excludedLandCover": ["forest", "wetland"]},
        }
        site = SiteCharacteristics(
            zone_id="z4",
            name="Forest Site",
            area_m2=50000,
            land_cover_type="forest",
        )
        is_ok, issues = check_site_requirements(tech, site)
        assert not is_ok


class TestMatchTechnologies:
    def test_good_site_returns_matches(self):
        site = SiteCharacteristics(
            zone_id="z1",
            name="Good Site",
            area_m2=50000,
            solar_ghi=1600,
            flood_risk=FloodRisk.NONE,
            land_cover_type="grassland",
        )
        matches = match_technologies(site)
        assert len(matches) > 0
        # Ground-mount solar should be in the list for a good open site
        tech_ids = [m.technology_id for m in matches]
        assert "solar-pv-ground" in tech_ids

    def test_urban_site_excludes_ground_mount(self):
        site = SiteCharacteristics(
            zone_id="z2",
            name="Urban Site",
            area_m2=500,  # Too small for ground-mount
            solar_ghi=1500,
            built_up_density=BuiltUpDensity.DENSE_URBAN,
            land_cover_type="built_up",
        )
        matches = match_technologies(site)
        tech_ids = [m.technology_id for m in matches]
        # Ground mount should be excluded due to small area
        assert "solar-pv-ground" not in tech_ids
