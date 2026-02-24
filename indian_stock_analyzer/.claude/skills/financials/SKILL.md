# Deep Financial Analysis Skill

## Overview
This skill enables extraction and analysis of detailed financial statements, quarterly results, and multi-year ratio trends from Screener.in — the most comprehensive free source for Indian company financials.

## Before Analysis — MANDATORY
You MUST read `screener-extraction.md` in this directory before accessing Screener.in. It contains:
- URL patterns and page structure
- Table extraction methods for quarterly/annual results
- Balance sheet, cash flow, and ratio extraction
- Output JSON schemas

## Valuation Methods
After data collection, read `financial-modeling.md` for:
- Discounted Cash Flow (DCF) methodology
- Relative valuation (PE, EV/EBITDA multiples)
- PEG ratio growth-adjusted valuation
- Graham Number and Margin of Safety calculations
- Dividend Discount Model (DDM) for dividend payers

## Data Sources
- **Primary**: `https://www.screener.in/company/{TICKER}/consolidated/`
- **Fallback**: `https://www.screener.in/company/{TICKER}/`
- Data available: 10 years of annual results, 12 quarters of results, balance sheet, cash flow, shareholding, ratios

## Error Handling
- If Screener returns 404: try alternate ticker formats (BSE code, full name)
- If consolidated data unavailable: fall back to standalone
- If tables are empty: note in output, continue with available data
- Rate limit: wait 3 seconds between Screener requests
