"""
Media Scraper - Data Analysis and Visualizations
Analyzes wheat disease news collection pipeline using SQLite database
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10

DB_PATH = "/Users/saral/Documents/media_scrape/backup_media_scrape.db"
OUTPUT_DIR = "/Volumes/SP PX10/DS projects/media_scraper/images/analysis"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_data(query):
    """Execute SQL query and return DataFrame"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ============================================================================
# 1. Pipeline Funnel Analysis
# ============================================================================
print("📊 Generating Pipeline Funnel Analysis...")

df_urls = get_data("""
    SELECT 
        COUNT(*) as total_urls,
        SUM(CASE WHEN response_code = 200 THEN 1 ELSE 0 END) as valid_urls,
        SUM(CASE WHEN parsed_newspaper3k = 1 THEN 1 ELSE 0 END) as extracted_content,
        SUM(CASE WHEN llm_parsed = 1 THEN 1 ELSE 0 END) as llm_classified,
        SUM(CASE WHEN llm_parsed = 2 THEN 1 ELSE 0 END) as llm_relevant
    FROM url_list
""")

funnel_data = {
    'Stage': ['URLs Collected', 'Valid URLs (200)', 'Content Extracted', 'LLM Classified', 'Relevant News'],
    'Count': [
        df_urls['total_urls'].values[0],
        df_urls['valid_urls'].values[0],
        df_urls['extracted_content'].values[0],
        df_urls['llm_classified'].values[0],
        df_urls['llm_relevant'].values[0]
    ]
}

fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
bars = ax.bar(funnel_data['Stage'], funnel_data['Count'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}',
            ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_ylabel('Count', fontsize=12, fontweight='bold')
ax.set_title('Pipeline Funnel: From Collection to Classification', fontsize=14, fontweight='bold', pad=20)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/01_pipeline_funnel.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: 01_pipeline_funnel.png")
plt.close()

# ============================================================================
# 2. LLM Classification Distribution
# ============================================================================
print("📊 Generating LLM Classification Distribution...")

df_llm = get_data("""
    SELECT 
        CASE 
            WHEN llm_parsed = -1 THEN 'Failed'
            WHEN llm_parsed = 1 THEN 'Processing'
            WHEN llm_parsed = 2 THEN 'Relevant'
            WHEN llm_parsed IS NULL THEN 'Not Started'
            ELSE 'Unrelated'
        END as status,
        COUNT(*) as count
    FROM url_list
    WHERE parsed_newspaper3k = 1
    GROUP BY llm_parsed
    ORDER BY count DESC
""")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart
colors_pie = ['#e74c3c', '#3498db', '#2ecc71', '#95a5a6', '#f39c12']
wedges, texts, autotexts = ax1.pie(df_llm['count'], labels=df_llm['status'], autopct='%1.1f%%',
                                     colors=colors_pie, startangle=90, textprops={'fontsize': 11})
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax1.set_title('LLM Classification of Extracted Content', fontsize=12, fontweight='bold')

# Bar chart
ax2.barh(df_llm['status'], df_llm['count'], color=colors_pie, alpha=0.8, edgecolor='black', linewidth=1.5)
ax2.set_xlabel('Count', fontsize=11, fontweight='bold')
for i, v in enumerate(df_llm['count']):
    ax2.text(v + 20, i, f'{int(v):,}', va='center', fontweight='bold')
ax2.set_title('Classification Distribution', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/02_llm_classification.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: 02_llm_classification.png")
plt.close()

# ============================================================================
# 3. Content Extraction Outcomes
# ============================================================================
print("📊 Generating Content Extraction Analysis...")

df_extraction = get_data("""
    SELECT 
        lkp.label as extraction_status,
        COUNT(*) as count
    FROM url_list ul
    LEFT JOIN lkp_parsed_newspaper3k lkp ON ul.parsed_newspaper3k = lkp.code
    WHERE ul.response_code = 200
    GROUP BY ul.parsed_newspaper3k, lkp.label
    ORDER BY count DESC
""")

fig, ax = plt.subplots(figsize=(12, 6))
colors_extract = ['#2ecc71', '#e74c3c', '#f39c12', '#3498db']
bars = ax.bar(df_extraction['extraction_status'], df_extraction['count'], 
              color=colors_extract[:len(df_extraction)], alpha=0.8, edgecolor='black', linewidth=1.5)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}',
            ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_ylabel('Count', fontsize=12, fontweight='bold')
ax.set_title('Content Extraction Outcomes (Valid URLs)', fontsize=14, fontweight='bold', pad=20)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/03_extraction_outcomes.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: 03_extraction_outcomes.png")
plt.close()

# ============================================================================
# 4. Daily Collection Trend
# ============================================================================
print("📊 Generating Daily Collection Trend...")

df_daily = get_data("""
    SELECT 
        DATE(fetched_at) as date,
        COUNT(*) as urls_collected,
        SUM(CASE WHEN response_code = 200 THEN 1 ELSE 0 END) as valid_urls
    FROM url_list
    GROUP BY DATE(fetched_at)
    ORDER BY date
""")

df_daily['date'] = pd.to_datetime(df_daily['date'])

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df_daily['date'], df_daily['urls_collected'], marker='o', linewidth=2, 
        label='Total URLs Collected', color='#3498db', markersize=4, alpha=0.7)
ax.plot(df_daily['date'], df_daily['valid_urls'], marker='s', linewidth=2,
        label='Valid URLs (HTTP 200)', color='#2ecc71', markersize=4, alpha=0.7)

ax.fill_between(df_daily['date'], df_daily['urls_collected'], alpha=0.2, color='#3498db')
ax.fill_between(df_daily['date'], df_daily['valid_urls'], alpha=0.2, color='#2ecc71')

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Count', fontsize=12, fontweight='bold')
ax.set_title('Daily URL Collection Trend', fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/04_daily_collection_trend.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: 04_daily_collection_trend.png")
plt.close()

# ============================================================================
# 5. Geographic Distribution of Detected Events
# ============================================================================
print("📊 Generating Geographic Distribution...")

df_geo = get_data("""
    SELECT 
        country,
        COUNT(*) as count
    FROM wheat_disease
    WHERE news_type IS NOT NULL
    GROUP BY country
    ORDER BY count DESC
""")

fig, ax = plt.subplots(figsize=(12, 6))
colors_geo = plt.cm.Spectral(range(len(df_geo)))
bars = ax.barh(df_geo['country'], df_geo['count'], color=colors_geo, alpha=0.8, edgecolor='black', linewidth=1.5)

for i, bar in enumerate(bars):
    width = bar.get_width()
    percentage = (width / df_geo['count'].sum()) * 100
    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2.,
            f'{int(width)} ({percentage:.1f}%)',
            ha='left', va='center', fontweight='bold', fontsize=11)

ax.set_xlabel('Number of Events', fontsize=12, fontweight='bold')
ax.set_title('Geographic Distribution of Wheat Disease Events', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/05_geographic_distribution.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: 05_geographic_distribution.png")
plt.close()

# ============================================================================
# 6. News Type Classification
# ============================================================================
print("📊 Generating News Type Classification...")

df_news_type = get_data("""
    SELECT 
        news_type,
        COUNT(*) as count
    FROM wheat_disease
    WHERE news_type IS NOT NULL
    GROUP BY news_type
    ORDER BY count DESC
""")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart
colors_news = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
wedges, texts, autotexts = ax1.pie(df_news_type['count'], labels=df_news_type['news_type'], 
                                     autopct='%1.1f%%', colors=colors_news[:len(df_news_type)],
                                     startangle=90, textprops={'fontsize': 11})
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax1.set_title('News Type Distribution', fontsize=12, fontweight='bold')

# Bar chart
ax2.bar(df_news_type['news_type'], df_news_type['count'], 
        color=colors_news[:len(df_news_type)], alpha=0.8, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Count', fontsize=11, fontweight='bold')
ax2.set_title('News Type Counts', fontsize=12, fontweight='bold')
for i, (news_type, count) in enumerate(zip(df_news_type['news_type'], df_news_type['count'])):
    ax2.text(i, count + 0.5, f'{int(count)}', ha='center', fontweight='bold')
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/06_news_type_classification.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: 06_news_type_classification.png")
plt.close()

# ============================================================================
# 7. Disease Detection Over Time
# ============================================================================
print("📊 Generating Disease Detection Timeline...")

df_timeline = get_data("""
    SELECT 
        DATE(date) as date,
        COUNT(*) as events
    FROM wheat_disease
    WHERE news_type IS NOT NULL AND date > '2024-12-01'
    GROUP BY DATE(date)
    ORDER BY date
""")

df_timeline['date'] = pd.to_datetime(df_timeline['date'])

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df_timeline['date'], df_timeline['events'], marker='o', linewidth=2.5,
        color='#e74c3c', markersize=6, label='Disease Events Detected')
ax.fill_between(df_timeline['date'], df_timeline['events'], alpha=0.3, color='#e74c3c')

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Events', fontsize=12, fontweight='bold')
ax.set_title('Wheat Disease Event Detection Timeline', fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/07_disease_timeline.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: 07_disease_timeline.png")
plt.close()

# ============================================================================
# 8. Response Code Distribution
# ============================================================================
print("📊 Generating Response Code Analysis...")

df_response = get_data("""
    SELECT 
        lkp.label as response,
        COUNT(*) as count
    FROM url_list ul
    LEFT JOIN lkp_response_code lkp ON ul.response_code = lkp.code
    GROUP BY ul.response_code, lkp.label
    ORDER BY count DESC
    LIMIT 10
""")

fig, ax = plt.subplots(figsize=(12, 6))
colors_response = ['#2ecc71', '#e74c3c', '#f39c12', '#95a5a6']
bars = ax.bar(range(len(df_response)), df_response['count'], 
              color=colors_response[:len(df_response)], alpha=0.8, edgecolor='black', linewidth=1.5)

ax.set_xticks(range(len(df_response)))
ax.set_xticklabels(df_response['response'], rotation=15, ha='right')
ax.set_ylabel('Count', fontsize=12, fontweight='bold')
ax.set_title('HTTP Response Code Distribution', fontsize=14, fontweight='bold', pad=20)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}',
            ha='center', va='bottom', fontweight='bold', fontsize=10)

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/08_response_codes.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: 08_response_codes.png")
plt.close()

print("\n" + "="*60)
print("✅ All visualizations generated successfully!")
print(f"📁 Output directory: {OUTPUT_DIR}")
print("="*60)
