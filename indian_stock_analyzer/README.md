# Indian Stock Analyzer

An AI-powered stock analysis system for Indian equities. Takes a company name, scrapes data from Tickertape and StockTwits, runs specialized analysis sub-agents, and produces BUY/SELL/HOLD recommendations with entry prices and profit targets.

Built with the [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk).

## Architecture

```
main.py (Orchestrator) — 4 steps, 3 sub-agents
  │
  ├── 1. Data Collector Agent (haiku)
  │     → Tickertape + StockTwits scraping
  │     → Screener.in financial analysis
  │     → News & events research
  │     → Output: *_tickertape.json, *_stocktwits.json,
  │               *_financials.json, *_news.json
  │
  ├── 2. Analyzer Agent (haiku)
  │     → Sentiment scoring (social 40%, market 30%, fundamental 30%)
  │     → Technical analysis (trends, support/resistance, entry strategy)
  │     → Peer comparison & relative valuation
  │     → Output: *_sentiment.json, *_technical.json, *_peers.json
  │
  ├── 3. Recommender Agent (sonnet)
  │     → Synthesize BUY/SELL/HOLD + conviction + targets
  │     → Risk assessment, position sizing, scenario analysis
  │     → Output: *_recommendation.json, *_risk.json
  │
  └── 4. Report Generation
        → Formatted text report via format_report.py
```

## Prerequisites

- Python 3.10+
- Claude Code CLI installed
- `ANTHROPIC_API_KEY` environment variable set

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Analyze a Stock

```bash
python main.py "Tata Consultancy Services"
python main.py "Mahindra and Mahindra Ltd"
python main.py "Infosys Ltd"
```

### Resume a Session

```bash
python main.py "Tata Consultancy Services" --resume <session_id>
```

The session ID is displayed after each analysis run.

## Output Files

All analysis outputs are saved to the `data/` directory:

| File | Agent | Description |
|------|-------|-------------|
| `{slug}_tickertape.json` | Data Collector | Fundamental data scraped from Tickertape |
| `{slug}_stocktwits.json` | Data Collector | Social sentiment data from StockTwits |
| `{slug}_financials.json` | Data Collector | Deep financial analysis & intrinsic valuations |
| `{slug}_news.json` | Data Collector | News & events with sentiment scoring |
| `{slug}_sentiment.json` | Analyzer | Weighted sentiment analysis scores |
| `{slug}_technical.json` | Analyzer | Technical analysis with entry strategy |
| `{slug}_peers.json` | Analyzer | Peer comparison & relative valuation |
| `{slug}_recommendation.json` | Recommender | Final BUY/SELL/HOLD recommendation |
| `{slug}_risk.json` | Recommender | Risk assessment & position sizing |

## Utility Scripts

```bash
# Validate a data file
python scripts/validate_stock_data.py data/tcs_tickertape.json

# Calculate technical metrics
python scripts/calculate_metrics.py data/tcs_tickertape.json

# Generate formatted report
python scripts/format_report.py tcs data
```

## Project Structure

```
├── main.py                    # Orchestrator
├── config/settings.json       # Configuration
├── agents/                    # Sub-agent prompt templates
│   ├── data-collector.md     # Scraping + financials + news
│   ├── analyzer.md           # Sentiment + technical + peers
│   └── recommender.md        # Recommendation + risk
├── hooks/                     # Pre/post tool-use hooks
│   ├── pre_scrape_validator.py
│   └── post_analysis_logger.py
├── scripts/                   # Utility scripts
│   ├── validate_stock_data.py
│   ├── calculate_metrics.py
│   └── format_report.py
├── .claude/skills/scraping/   # Claude Code skills
│   ├── SKILL.md
│   ├── data-extraction.md
│   └── analysis-frameworks.md
├── data/                      # Analysis output (gitignored)
├── sessions/                  # Session state (gitignored)
└── logs/                      # Audit logs (gitignored)
```

## Disclaimer

This tool is for **informational and educational purposes only**. It does NOT constitute financial advice. Always consult a qualified financial advisor before making investment decisions. The authors are not responsible for any financial losses incurred from using this tool. Past performance does not guarantee future results.
