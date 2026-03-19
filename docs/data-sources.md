# Data Sources

Catalog of external data sources used by the Energy PoC.

## Geospatial (via Geo-Layer-Viewer)

| Source | Layers | Resolution | Coverage | Access |
|--------|--------|-----------|----------|--------|
| Global Solar Atlas (World Bank/Solargis) | GHI, DNI, PVOUT per neighbourhood | Neighbourhood-level | Porto Alegre | Geo-Layer-Viewer API |
| ESA Dynamic World | Land cover classification (10 classes) | 10m | Global | OEF S3 tile catalog |
| GHSL (EC JRC) | Built-up density, population, urbanization | 100m-1km | Global | OEF S3 tile catalog |
| Copernicus DEM | Elevation / slope | 30m | Global | AWS Open Data |
| JRC Global Surface Water | Water occurrence, seasonality | 30m | Global | Azure Blob Storage |
| VIIRS Night Lights | Night-time radiance (grid proxy) | 500m | Global | OEF S3 tile catalog |
| MODIS NDVI | Vegetation index | 250m | Global | Planetary Computer |
| Hansen GFC | Forest loss 2000-2024 | 30m | Global | Google Cloud Storage |
| CHIRPS Climate Indices | Extreme precipitation (R90p, R95p, R99p) | 5km | Global | OEF S3 tile catalog |
| ERA5 Temperature Indices | Extreme temperature (TNx, TXx, TX90p) | ~30km | Global | OEF S3 tile catalog |
| Flood Risk Index | Flood risk projections | ~1km | Global | OEF S3 tile catalog |
| Heatwave Magnitude | Heatwave magnitude projections | ~30km | Global | OEF S3 tile catalog |
| Planet/SkySat | 2024 flood extent (Porto Alegre) | High-res | Porto Alegre | OEF S3 |
| IBGE Census 2010 | Socioeconomic indicators | Census tract | Brazil | OEF S3 (GeoJSON) |
| IBGE Settlements 2022 | Informal settlement locations | Point | Brazil | OEF S3 (GeoJSON) |
| EPTC GTFS | Transit stops and routes | Stop/route | Porto Alegre | OEF S3 (GeoJSON) |
| OSM | City boundary, rivers, POIs | Variable | Porto Alegre | Nominatim / Overpass |

## Emissions (via CityCatalyst Global API)

| Source | Data | Coverage |
|--------|------|----------|
| SEEG v2023 | Brazilian city-level emissions by GPC sector | Brazil |
| Climate TRACE v2025 | Facility-level emissions | Global |

## City Documents (in repo)

| File | Description |
|------|-------------|
| `city_data/Sumario Executivo PLAC V7 - EN.pdf` | Porto Alegre Climate Action Plan - Executive Summary (English) |
| `city_data/P1_PLAC_PlanoTrabalho 9.pdf` | Porto Alegre Climate Action Plan - Work Plan |
