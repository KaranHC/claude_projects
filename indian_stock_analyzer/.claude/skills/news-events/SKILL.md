# News & Corporate Events Skill

## Overview
This skill enables extraction and analysis of recent news, corporate actions, and market-moving events for Indian listed companies. News flow and upcoming catalysts are critical for timing investment decisions.

## Before Analysis — MANDATORY
Read `news-extraction.md` for:
- News source URLs and extraction patterns
- Sentiment classification from headlines
- Relevance scoring methodology

Read `corporate-actions.md` for:
- Types of corporate actions and their impact
- How to extract upcoming events (earnings, dividends, AGMs)
- Impact assessment framework

## Data Sources
- **MoneyControl**: `https://www.moneycontrol.com/news/tags/{company}.html`
- **Economic Times**: `https://economictimes.indiatimes.com/topic/{company}`
- **BSE Filings**: `https://www.bseindia.com/corporates/ann.html`
- **WebSearch**: For recent news aggregation

## Key Principles
1. Focus on last 30 days of news for relevance
2. Weight institutional sources higher than social media
3. Distinguish between noise and signal (earnings, management changes, regulatory = signal)
4. Track upcoming catalysts (earnings dates, AGM, result announcements)
5. Note any red flags (SEBI notices, auditor concerns, legal proceedings)
