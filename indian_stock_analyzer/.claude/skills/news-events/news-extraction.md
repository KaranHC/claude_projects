# News Extraction & Analysis

## 1. News Sources

### Primary: WebSearch Aggregation
Use multiple searches to capture comprehensive news:
```
"{company_name}" stock news India last 30 days
"{company_name}" quarterly results 2024 2025
"{company_name}" management commentary outlook
"{ticker}" NSE analyst rating upgrade downgrade
"{company_name}" SEBI regulatory filing
```

### Secondary: MoneyControl
- URL: `https://www.moneycontrol.com/news/tags/{company_slug}.html`
- Contains timestamped news articles with headlines and summaries
- Good for earnings reports, analyst notes, corporate actions

### Tertiary: Economic Times Markets
- URL pattern: `https://economictimes.indiatimes.com/topic/{company_name}`
- Macro context and sector-level analysis

## 2. News Classification

### Category Tags
Classify each news item into one or more categories:

| Category | Impact Level | Examples |
|----------|-------------|---------|
| `EARNINGS` | HIGH | Quarterly results, profit warnings, guidance |
| `MANAGEMENT` | HIGH | CEO/CFO change, board reshuffles |
| `REGULATORY` | HIGH | SEBI orders, RBI directives, policy changes |
| `M&A` | HIGH | Acquisitions, divestments, mergers |
| `LEGAL` | HIGH | Lawsuits, investigations, penalties |
| `ANALYST` | MEDIUM | Rating changes, target price revisions |
| `SECTOR` | MEDIUM | Industry trends, competitor moves |
| `DIVIDEND` | MEDIUM | Dividend announcements, special dividends |
| `EXPANSION` | MEDIUM | New plants, market entry, capex |
| `MACRO` | LOW | Market trends, economic indicators |
| `ROUTINE` | LOW | AGM notices, routine filings |

### Sentiment Scoring Per News Item
- **+2**: Very positive (beat estimates, upgrade, major contract)
- **+1**: Positive (in-line results, expansion, positive outlook)
- **0**: Neutral (routine filing, no-impact news)
- **-1**: Negative (miss estimates, downgrade, margin pressure)
- **-2**: Very negative (fraud, regulatory action, profit warning)

## 3. News Impact Assessment

### Aggregate News Score
```
News Score = Sum(sentiment_i * impact_weight_i * recency_weight_i) / N

Impact weights: HIGH=3, MEDIUM=2, LOW=1
Recency weights: Last 7 days=1.5, 8-14 days=1.0, 15-30 days=0.5
```

### Red Flag Detection
Flag any news containing:
- SEBI show-cause, investigation, penalty
- Auditor qualification, disclaimer, resignation
- Promoter share pledge increase, selling
- Credit rating downgrade
- Whistleblower complaint
- Forensic audit
- NCLT/insolvency proceedings

## 4. Upcoming Catalysts

### Events to Track
```json
{
  "upcoming_catalysts": [
    {
      "event": "Q3 FY25 Results",
      "expected_date": "2025-01-15",
      "impact": "HIGH",
      "expectation": "Revenue growth of 8-10% expected"
    },
    {
      "event": "Dividend Declaration",
      "expected_date": "2025-03-15",
      "impact": "MEDIUM",
      "expectation": "Interim dividend expected based on pattern"
    }
  ]
}
```

## 5. Output Schema

```json
{
  "company": "Company Name",
  "ticker": "TICKER",
  "news_period": "last_30_days",
  "total_news_items": 0,
  "news_items": [
    {
      "headline": "string",
      "source": "string",
      "date": "YYYY-MM-DD",
      "category": "EARNINGS|MANAGEMENT|...",
      "sentiment": -2 to +2,
      "impact_level": "HIGH|MEDIUM|LOW",
      "summary": "1-2 sentence summary"
    }
  ],
  "aggregate_news_score": 0.00,
  "news_sentiment_label": "Very Positive|Positive|Neutral|Negative|Very Negative",
  "red_flags": ["flag 1", "flag 2"],
  "upcoming_catalysts": [],
  "key_themes": ["theme 1", "theme 2"],
  "analyzed_at": "ISO-8601 timestamp"
}
```
