# Institutional Activity & Smart Money Tracking Skill

## Overview
This skill tracks institutional investor activity — FII/FPI, DII, mutual funds, and insider trades. In Indian markets, institutional flows are among the strongest predictors of medium-term price direction. Retail investors who align with institutional flows statistically outperform.

## Before Analysis — MANDATORY
Read `shareholding-patterns.md` for:
- How to extract and interpret quarterly shareholding data
- FII/DII flow analysis methodology
- Mutual fund portfolio overlap analysis

Read `bulk-block-deals.md` for:
- Large transaction tracking methodology
- Insider trading signal interpretation
- SAST (Substantial Acquisition) disclosure analysis

## Data Sources
- **Tickertape shareholding**: From scraped company page
- **Screener.in shareholding tab**: `#shareholding` section
- **Trendlyne**: `https://trendlyne.com/equity/{ticker}/shareholding/`
- **BSE bulk/block deals**: Via WebSearch
- **SEBI SAST filings**: Via WebSearch

## Key Insight
When FIIs, DIIs, and promoters are all increasing holdings simultaneously, the stock has a historically high probability of outperformance over the next 6-12 months. Conversely, synchronized selling is a strong exit signal.
