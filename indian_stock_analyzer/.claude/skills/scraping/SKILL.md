# Stock Data Scraping Skill

## Overview
This skill enables scraping and extraction of Indian stock market data from Tickertape and StockTwits for comprehensive equity analysis.

## Before Scraping — MANDATORY
You MUST read `data-extraction.md` in this directory before performing any web scraping. It contains:
- Exact URL patterns and API endpoints
- HTML/JSON extraction methods
- Output JSON schemas
- Error handling patterns

## Analysis Methods
After data collection, read `analysis-frameworks.md` for:
- Technical indicator calculations (RSI, MACD, Moving Averages)
- Fundamental analysis benchmarks (Indian market PE, PB ratios)
- Sentiment scoring methodology
- Recommendation criteria and thresholds

## Rate Limiting Rules
- Wait at least 3 seconds between requests to the same domain
- Maximum 2 retries per failed request
- On 403/429 responses: back off and retry with increased delay
- Never make concurrent requests to the same domain

## Error Handling
- If Tickertape returns no data: log error, continue with StockTwits only
- If StockTwits returns no data: log error, continue with Tickertape only
- If both fail: save error report with partial data and stop
- Always validate scraped data with `scripts/validate_stock_data.py` before saving

## Workflow
1. Read `data-extraction.md` (MANDATORY)
2. Use WebSearch to find the correct Tickertape URL slug for the company
3. Use WebFetch to scrape Tickertape page
4. Extract data from `__NEXT_DATA__` JSON in HTML
5. Use WebFetch to call StockTwits API
6. Validate all extracted data
7. Save validated JSON files to the data directory
