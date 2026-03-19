# GPC Stationary Energy Sector Reference

## Overview

The Global Protocol for Community-Scale Greenhouse Gas Inventories (GPC) defines Sector I as Stationary Energy. This sector covers emissions from fuel combustion and electricity consumption in buildings, facilities, and industries within the city boundary.

## GPC Sub-Sectors (Sector I)

| Ref | Sub-Sector | Scope 1 | Scope 2 | Scope 3 |
|-----|-----------|---------|---------|---------|
| I.1 | Residential | I.1.1 | I.1.2 | I.1.3 |
| I.2 | Commercial/Institutional | I.2.1 | I.2.2 | I.2.3 |
| I.3 | Manufacturing/Construction | I.3.1 | I.3.2 | I.3.3 |
| I.4 | Energy Industries | I.4.1 | I.4.2 | I.4.3 |
| I.5 | Agriculture/Forestry/Fishing | I.5.1 | I.5.2 | I.5.3 |
| I.6 | Non-specified | I.6.1 | I.6.2 | I.6.3 |
| I.7 | Fugitive (coal/oil/gas) | I.7.1 | — | — |
| I.8 | Fugitive (other) | I.8.1 | — | — |

## Relevance to Energy PoC

- **Scope 2 emissions** (I.x.2) are the primary target for solar PV and distributed generation — reducing grid electricity consumption
- **Scope 1 emissions** (I.x.1) are targeted by efficiency measures that reduce fuel combustion
- **Sub-sector breakdown** helps prioritize: if commercial/institutional (I.2) has highest emissions, target public buildings first

## Data Access

Use the CityCatalyst Global API to fetch emissions by GPC reference number:
```
GET /api/v0/climatetrace/city/BR POA/2022/SEEGv2023?gpc_ref=I.1.1
```
