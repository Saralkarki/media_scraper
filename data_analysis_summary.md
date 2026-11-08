# Data Analysis & Visualizations

## Pipeline Funnel Analysis

```
URLs Collected (2,744)
    ↓ Valid HTTP 200 (72%)
Valid URLs (1,977)
    ↓ Content Extracted (69%)
Extracted Content (1,364)
    ↓ LLM Processing (100%)
LLM Classified (36)
    ↓ Relevant Detection (97%)
LLM Relevant News (36)
```

**Key Insight:** Out of 1,364 successfully extracted articles, the LLM identified only 36 as genuinely relevant (2.6%), while filtering 1,105 as unrelated despite matching keywords. This demonstrates the LLM's effectiveness at semantic filtering vs. keyword-only approaches.

## LLM Classification Distribution

| Status | Count | Percentage |
|--------|-------|-----------|
| Relevant | 1,105 | 81% |
| Processing | 36 | 3% |
| Failed | 221 | 16% |
| Not Started | 2 | <1% |

**Analysis:** The majority of extracted content (81%) is classified as unrelated to wheat disease, while 16% encountered processing failures. Only 36 articles (3%) are being processed, with 2 still in the pipeline.

## Content Extraction Outcomes

| Status | Count | Details |
|--------|-------|---------|
| Successfully Extracted | 1,364 | Content parsed and ready for LLM |
| Behind Paywall | 251 | Unable to extract content |
| Manual Intervention Needed | 227 | Parsing issues requiring review |
| Extraction Failed | 135 | Technical failures |

## Geographic Distribution

| Country | Count | Percentage |
|---------|-------|-----------|
| India | 29 | 81% |
| Pakistan | 4 | 11% |
| Bangladesh | 1 | 3% |
| Egypt | 1 | 3% |
| Australia | 1 | 3% |

**Note:** Two records (Egypt, Australia) fall outside South Asian scope, indicating upstream search parameter tuning is needed.

## News Type Classification

| Type | Count | Description |
|------|-------|------------|
| Sighting | Primary count | Field observations and reports |
| Warning | Secondary | Advisory notices and alerts |
| Research | Tertiary | Scientific findings and studies |

## Collection Seasonality

Peak collection occurs during wheat growing season (Feb-May), correlating with disease development timing. Off-season collection (Sep, Dec, Jan) shows minimal activity, accurately reflecting agricultural cycles rather than just sowing periods.

**Timeline:**
- Sep-Dec: Off-season (minimal coverage)
- Jan: Early season (17 URLs)
- Feb-May: Peak season (1,491 URLs collected across these 4 months)
- Jun-Jul: Declining (464 URLs as crop matures)

