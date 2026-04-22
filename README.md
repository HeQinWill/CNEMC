<div align="center">

# 🌫️ CNEMC Air Quality Data Scraper

*Automated collection of China's national air quality data (六参数) — hourly updates*

[![Last Commit](https://img.shields.io/github/last-commit/HeQinWill/CNEMC?logo=github)](https://github.com/HeQinWill/CNEMC/commits/main)
[![Data Source](https://img.shields.io/badge/Data-CNEMC-00BFFF?logo=gov.uk)](https://air.cnemc.cn:18007)
[![License](https://img.shields.io/badge/License-MIT-blue?logo=open-source-initiative)](https://opensource.org/licenses/MIT)

</div>

## 🎯 What is this?

A **data collection pipeline** for China's national air quality monitoring network (中国环境监测总站). Fetches hourly AQI data for 6 key pollutants across all monitoring stations — automatically, via cron.

## 📊 The Six Parameters (六参数)

| Parameter | Description | Unit |
|-----------|-------------|------|
| `PM2.5` | Fine particulate matter | μg/m³ |
| `PM10` | Coarse particulate matter | μg/m³ |
| `SO₂` | Sulfur dioxide | μg/m³ |
| `NO₂` | Nitrogen dioxide | μg/m³ |
| `CO` | Carbon monoxide | mg/m³ |
| `O₃` | Ozone (hourly + 8h rolling) | μg/m³ |

> **Note:** `O₃_24h` values changed after 2023-11-09. Always verify which metric is being used in your analysis.

## 📡 Data Sources

| Endpoint | Method | Description |
|----------|--------|-------------|
| [`GetAllAQIPublishLive`](https://air.cnemc.cn:18007) | POST | Current hour's readings |
| [`GetAQIHistoryByConditionHis`](https://air.cnemc.cn:18007) | POST | Historical readings (last 24h) |
| [`China.json`](https://air.cnemc.cn:18007/Content/Scripts/Map/China.json) | GET | GeoJSON map boundary file |

## 🚀 Quick Start

### 1. Fetch current data

```bash
curl -k 'https://air.cnemc.cn:18007/HourChangesPublish/GetAllAQIPublishLive' \
  -X POST \
  -H 'Content-Length: 0' \
  -o cnemc_$(date +%Y%m%d%H%M).json
```

### 2. Fetch historical data

```bash
curl 'https://air.cnemc.cn:18007/HourChangesPublish/GetAQIHistoryByConditionHis' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  --data 'date=2025-11-08+10%3A00%3A00' \
  -o cnemc_his.json
```

### 3. Set up auto-crawl (cron)

```bash
# Run every 30 minutes
crontab -e

# Add this line:
13,43 * * * * /usr/bin/bash /path/to/cnemc.sh
```

## 📁 Output Format

Data is saved as timestamped CSV files:

```
2026-03-08T11.csv
2026-03-08T12.csv
...
```

### Column Reference

| Column | Meaning |
|--------|---------|
| `site_code` | Station identifier (e.g., `1742A`) |
| `site_name` | Station name (e.g., `阳泉市平坦`) |
| `pm25` | PM2.5 — 1h average |
| `pm25_24` | PM2.5 — 24h rolling average |
| `pm10` / `pm10_24` | PM10 (1h / 24h) |
| `so2` / `so2_24` | SO₂ (1h / 24h) |
| `no2` / `no2_24` | NO₂ (1h / 24h) |
| `co` / `co_24` | CO (1h / 24h) |
| `o3` | O₃ — 1h average |
| `o3_8h` | O₃ — daily max 8h rolling |
| `aqi` | Overall AQI |

## ⚠️ Data Quality Notes

- **~30 min delay** — Data published ~30 min after collection
- **8h rolling mean** — Requires 8 hours of data; early hours may be incomplete
- **Missing records** — Some timestamps have gaps; see [`Known Issues`](README.md#数据问题记录) in the source README
- **O₃ column swap** — Before 2023-11-09, `o3_24h` and `o3` columns were swapped in the raw output

## 📦 Related Data Sources

| Source | URL |
|--------|-----|
| CNEMC Air Quality | https://air.cnemc.cn:18007 |
| Quotsoft Mirror | https://quotsoft.net/air/ |

## 🛠 Tech Stack

| Component | Tool |
|-----------|------|
| Data source | CNEMC API |
| Crawler | curl / wget |
| Scheduler | cron |
| Storage | CSV files |

---

README optimized with [Gingiris README Generator](https://gingiris.github.io/github-readme-generator/)
