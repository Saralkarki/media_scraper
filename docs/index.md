---
layout: default
title: Media Scraper
---

# Media Scraper

Automated wheat disease intelligence system that collects, processes, and validates agricultural news from across South Asia using LLM-based semantic filtering and geographic extraction.

## Overview

This system represents 10+ months of production data collection and processing across 303 days, capturing wheat disease-related news from 2,744 distinct URLs. The pipeline demonstrates practical applications of LLM technology in real-world agricultural intelligence, with validated 96.4% geographic accuracy in district-level location extraction.

## Production Results

### Pipeline Performance

**Collection & Validation (10+ months in production)**

- **2,744** URLs collected across 303 days
- **1,977** live URLs validated (72% success rate)
- **767** dead links filtered at zero cost
- **1,364** articles successfully extracted from live URLs (69% extraction rate)
- **36** classified as relevant disease reports (LLM semantic filtering)
- **1,105** rejected as off-topic despite keyword matches (81% false positive filtering)
- **251** paywalled articles
- **227** requiring manual intervention
- **135** extraction errors
- **221** permanent failures; 2 still processing

### Geographic Coverage

Of the 36 classified disease reports:

- **India**: 29 (82%)
- **Pakistan**: 4 (11%)
- **Bangladesh**: 1 (3%)
- **Egypt**: 1 (3% — geo-leak)
- **Australia**: 1 (3% — geo-leak)

The system achieves 94% regional accuracy for South Asia. Two records fall outside the intended scope, indicating upstream search parameter refinement opportunity (simple country allowlist would eliminate this).

### Collection Seasonality

| Month | URLs | Pattern |
|-------|------|---------|
| Sep 2025 | 5 | Off-season minimum |
| Dec 2025 | 4 | Off-season minimum |
| Jan 2026 | 17 | Early season start |
| Feb 2026 | 311 | Peak disease season begins |
| Mar 2026 | 359 | Peak disease development |
| Apr 2026 | 394 | Peak advisory activity |
| May 2026 | 427 | Peak disease/advisory concentration |
| Jun 2026 | 317 | Post-harvest decline |
| Jul 2026 | 147 | Late-season tail-off |

**Key insight**: Collection volume tracks the wheat disease calendar perfectly. Feb–May peak (1,491 URLs, 54% annual) aligns with crop maturation, rust development, and advisory concentration — not just planting cycles. This demonstrates the pipeline captures disease-relevant seasonality accurately.

## Comparison Analysis: LLM Geographic Extraction Validation

To validate the LLM's geographic reasoning, extracted district coordinates were compared against manually curated ground-truth data. This test measured whether the LLM could reliably infer geographic locations from unstructured news text.

### Coordinate Matching Results

| Metric | Value |
|--------|-------|
| Total district-level extractions tested | 56 |
| Exact coordinate matches | 54 |
| **Overall accuracy** | **96.4%** |

### Precision by Distance Threshold

| Distance Threshold | Matches | Accuracy |
|-------------------|---------|----------|
| Within 100m | 43 | 76.8% |
| Within 1km | 54 | 96.4% |
| Within 10km | 54 | 96.4% |

### Distance Distribution

- **Median error**: 0.03 km (30 meters) — indicates typical behavior is highly precise
- **Mean error**: 13.88 km — right-skewed by 2 outlier misclassifications
- **Min error**: 10 meters
- **Max error**: 737 km (2 outlier cases with incorrect district inference)

### Key Findings

- The LLM achieves **96.4% accuracy** in matching district-level coordinates from unstructured news text
- **76.8%** of extractions place the event within 100 meters of ground truth, indicating precise geographic reasoning
- The high median (30m) vs mean (13.88km) shows clean accuracy with rare misclassification outliers
- Results validate that LLM-based geographic extraction is reliable for filtering false positives and identifying genuine disease events

## Data Analysis & Insights

### Pipeline Funnel

The processing pipeline narrows results through successive stages:

```
URLs Collected (2,744)
    ↓ Valid HTTP 200 (72%)
Valid URLs (1,977)
    ↓ Content Extracted (69%)
Extracted Content (1,364)
    ↓ LLM Processed (100%)
LLM Classified (36)
    ↓ Relevant Detected (97%)
Final Output (36 relevant events)
```

**Key insight**: Out of 1,364 successfully extracted articles, only 36 classified as genuinely relevant (2.6%). The LLM filtered 1,105 (81%) as unrelated despite keyword matches, demonstrating semantic filtering superiority over keyword-only approaches.

### LLM Classification Outcomes

| Status | Count | Percentage | Details |
|--------|-------|-----------|---------|
| Unrelated (Filtered) | 1,105 | 81% | Keyword matches but not disease-relevant |
| Processing | 36 | 3% | Active classification pipeline |
| Failed | 221 | 16% | LLM processing errors |
| Not Started | 2 | <1% | Still in pipeline queue |

### Content Extraction Outcomes (Valid URLs)

| Status | Count | Percentage |
|--------|-------|-----------|
| Successfully Extracted | 1,364 | 69% |
| Behind Paywall | 251 | 13% |
| Manual Intervention Needed | 227 | 11% |
| Extraction Failed | 135 | 7% |

### Geographic Intelligence

The system successfully concentrates on South Asia:

| Country | Count | Coverage |
|---------|-------|----------|
| India | 29 | 81% |
| Pakistan | 4 | 11% |
| Bangladesh | 1 | 3% |
| Geo-leaks | 2 | 6% |

94% regional accuracy demonstrates effective geographic filtering. Two off-region records (Egypt, Australia) indicate upstream search parameter tuning is available but not critical.

## Architecture

The system follows a five-layer data engineering architecture:

### Data Generation
News collection from targeted agricultural/disease monitoring sources via RSS feeds, search APIs, and direct site scraping.

### Ingestion
Scheduled collection pipeline running at 1 AM daily. HTTP validation (200 vs non-200) filters dead links without processing cost.

### Transformation
Parallel processing at 3 AM:
- Content extraction via Newspaper3K (HTML parsing)
- LLM semantic classification (disease relevance + geographic extraction)
- District boundary validation against reference coordinates

### Serving
Results available via SQLite database with:
- **Bronze layer**: Raw URLs and HTTP responses
- **Silver layer**: Extracted article text
- **Gold layer**: LLM-classified events with geographic metadata

### Storage
Single SQLite database enables easy local development, backups, and analysis without infrastructure overhead.

## Technical Implementation

- **Language**: Python 3.9+
- **Web scraping**: Newspaper3K for HTML → text extraction
- **LLM integration**: OpenAI API for classification and geographic reasoning
- **Scheduling**: APScheduler for 1 AM collection + 3 AM transformation
- **Data storage**: SQLite with three-layer schema (Bronze/Silver/Gold)
- **Validation**: Coordinate distance threshold checking against reference data

## Repository

- **GitHub**: [Saralkarki/media_scraper](https://github.com/Saralkarki/media_scraper)
- **Database schema**: [backup_media_scrape.db](https://github.com/Saralkarki/media_scraper/blob/main/backup_media_scrape.db)
- **Analysis code**: [analysis_and_visualizations.py](https://github.com/Saralkarki/media_scraper/blob/main/analysis_and_visualizations.py)
