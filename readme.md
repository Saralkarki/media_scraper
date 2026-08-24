# Media Scraper

An automated system for collecting and analyzing news articles about wheat rust disease and related agricultural concerns from across South Asia.

## System Architecture

```
News Sources       Content Extraction       LLM Processing       Storage & Access
     ↓                    ↓                      ↓                    ↓
┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐
│ Google News  │  │ URL Validation   │  │  Groq API        │  │  SQLite DB   │
│ NewsAPI      │→ │ newspaper3k      │→ │  Structured      │→ │  REST API    │
│ Other feeds  │  │ HTTP validation  │  │  Extraction      │  │  Dashboard   │
└──────────────┘  └──────────────────┘  └──────────────────┘  └──────────────┘
```

## Overview

This application automatically collects, processes, and analyzes news articles about wheat rust disease using AI-powered feature extraction, providing real-time insights for agricultural intelligence across South Asia.

## Tech Stack

**Backend & Processing**: Flask · Python · SQLAlchemy · newspaper3k  
**AI & LLM**: Groq API for structured data extraction  
**Frontend**: JavaScript · Highcharts · DataTables  
**Infrastructure**: SQLite · APScheduler · Docker · REST API

## Key Capabilities

![System Architecture](images/Staging_data.png)
*Data Collection & Staging: Multi-source news aggregation and initial processing pipeline*

### Core Pipeline
- **Data Collection**: Multi-source aggregation from Google News, NewsAPI with APScheduler automation
- **Content Extraction**: URL validation and article text parsing via newspaper3k
- **AI-Powered Processing**: Groq API for structured data extraction with confidence scoring
- **Structured Output**: Geographic location, disease classification, wheat variety identification

![LLM Parsed Data Table](images/final_table_LLM_parsed.png)
*Extracted Data: Structured information extracted by LLM including location, disease type, variety, and confidence scores*

## Features

- **Automated Collection** – Continuous background scraping via APScheduler
- **LLM-Powered Analysis** – Groq API for intelligent data extraction and classification
- **REST API** – Programmatic access with filtering and authentication
- **Interactive Dashboards** – Real-time visualizations with Highcharts and DataTables
- **Scalable Design** – Docker-based deployment with SQLite backend
- **Data Quality** – Duplicate detection, validation, and confidence scoring

### Dashboard Visualizations

![Interactive Visualizations](images/visualization.png)
*Analytics Dashboard: Real-time charts and statistics with Highcharts for trend analysis*

![Geographic Mapping](images/mapped-visualization.png)
*Regional Intelligence: Geographic distribution of wheat rust disease outbreaks across South Asia*

## Quick Links

- 🌐 **Live Application**: https://mediascraper.saralcodes.xyz/
- 📖 **Full Documentation**: See technical documentation on the live site
