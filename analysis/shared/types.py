"""Shared types for energy project preparation analysis."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ConstraintSeverity(Enum):
    HARD = "hard"
    SOFT = "soft"


class TechnologyCategory(Enum):
    SOLAR_PV = "solar_pv"
    BATTERY_STORAGE = "battery_storage"
    GRID_UPGRADE = "grid_upgrade"
    EFFICIENCY = "efficiency"
    DISTRIBUTED_GENERATION = "distributed_generation"
    HYBRID = "hybrid"


class FloodRisk(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class BuiltUpDensity(Enum):
    RURAL = "rural"
    SUBURBAN = "suburban"
    URBAN = "urban"
    DENSE_URBAN = "dense_urban"


@dataclass
class Range:
    min: float
    max: float
    unit: str = ""


@dataclass
class GeoPoint:
    lat: float
    lng: float


@dataclass
class GeoBounds:
    min_lat: float
    min_lng: float
    max_lat: float
    max_lng: float


@dataclass
class LayerValue:
    layer_id: str
    value: Any
    unit: str = ""


@dataclass
class SiteCharacteristics:
    zone_id: str
    name: str
    area_m2: float
    solar_ghi: float | None = None
    solar_dni: float | None = None
    solar_pvout: float | None = None
    flood_risk: FloodRisk = FloodRisk.NONE
    built_up_density: BuiltUpDensity = BuiltUpDensity.RURAL
    population_density: float | None = None
    land_cover_type: str = ""
    grid_proximity_proxy: float | None = None
    geometry: dict | None = None


@dataclass
class ConstraintResult:
    constraint_id: str
    passed: bool
    severity: ConstraintSeverity
    penalty: float = 0
    description: str = ""


@dataclass
class ScoredZone:
    zone_id: str
    name: str
    score: float
    score_breakdown: dict[str, float] = field(default_factory=dict)
    constraint_flags: list[str] = field(default_factory=list)
    characteristics: SiteCharacteristics | None = None


@dataclass
class TechnologyMatch:
    technology_id: str
    name: str
    category: TechnologyCategory
    feasibility_score: float
    capacity_range: Range | None = None
    estimated_output: Range | None = None
    capex_range: Range | None = None
    lcoe_range: Range | None = None
    rationale: str = ""
    risks: list[str] = field(default_factory=list)


@dataclass
class Patch:
    id: str
    target_component: str
    target_field: str
    current_value: Any
    proposed_value: Any
    rationale: str
    confidence: float
    sources: list[str] = field(default_factory=list)
    status: str = "proposed"
