# Indian Stock Analyzer: Product Walkthrough

> A 3-agent pipeline built on the Claude Agent SDK that delivers institutional-grade Indian equity analysis from a single command.

---

## 1. Introduction & Overview

The Indian Stock Analyzer is a CLI application that takes an Indian company name and produces a comprehensive BUY / SELL / HOLD recommendation with risk-adjusted position sizing. It orchestrates three specialized AI sub-agents in sequence:

```
Data Collection  -->  Analysis  -->  Recommendation
  (haiku)           (haiku)          (sonnet)
```

Each sub-agent is equipped with purpose-built skills, hooks, and Python scripts. The orchestrator (Claude Sonnet) dispatches them via the Claude Agent SDK's `Task` tool, then assembles the final report.

**What you get at the end:** 9 structured JSON files covering fundamentals, sentiment, technicals, peer comparison, recommendation, and risk, plus a formatted text report.

---

## 2. Input to Output: Step-by-Step Flow

Running the analyzer is a single command:

```bash
python main.py "Mahindra and Mahindra Ltd"
```

Here is exactly what happens inside `main.py`:

| Step | Code Location | What Happens |
|------|---------------|-------------|
| 1. Parse CLI args | `main.py:398-416` | Company name extracted from `sys.argv[1]`; optional `--resume <session_id>` parsed |
| 2. Slugify | `main.py:44` | `slugify("Mahindra and Mahindra Ltd")` produces `mahindra-and-mahindra-ltd` |
| 3. Load config | `main.py:49` | `load_config()` reads `config/settings.json` (domains, weights, agent settings) |
| 4. Load agent prompts | `main.py:56` | `load_agent_prompt()` reads 3 markdown files from `agents/` and replaces `{company}`, `{company_slug}`, `{data_dir}` placeholders |
| 5. Build system prompt | `main.py:99` | `build_system_prompt()` constructs the orchestrator prompt defining the 4-step workflow |
| 6. Configure SDK | `main.py:217` | `ClaudeAgentOptions` set with model=sonnet, max_turns=25, 8 allowed tools, hooks |
| 7. Stream execution | `main.py:242` | `query()` async generator yields `AssistantMessage`, `UserMessage`, `ResultMessage` as the orchestrator runs |
| 8. Orchestrator dispatches | Runtime | 3 Task sub-agents dispatched sequentially; Step 4 calls `format_report.py` via Bash |
| 9. Save session | `main.py:354` | `save_session()` writes session ID to `sessions/` for `--resume` support |
| 10. Print summary | `main.py:360-395` | Tools used, sub-agents run, files written, and output file checklist printed |

---

## 3. Component Deep-Dive

### a) Skills (7 categories, 21 files)

Skills live in `.claude/skills/` and provide domain-specific instructions that sub-agents load at runtime.

| Category | Files (3 per category) | Used By | Purpose |
|----------|----------------------|---------|---------|
| `scraping` | `SKILL.md`, `data-extraction.md`, `analysis-frameworks.md` | Data Collector | Tickertape/StockTwits extraction patterns, HTML parsing strategies |
| `financials` | `SKILL.md`, `screener-extraction.md`, `financial-modeling.md` | Data Collector | Screener.in data extraction, valuation models (Graham, DCF, PEG) |
| `peer-analysis` | `SKILL.md`, `peer-comparison.md`, `relative-valuation.md` | Analyzer | Peer identification, percentile ranking, relative fair value |
| `institutional` | `SKILL.md`, `shareholding-patterns.md`, `bulk-block-deals.md` | Analyzer | FII/DII flows, promoter holdings, bulk/block deal analysis |
| `risk-management` | `SKILL.md`, `risk-models.md`, `scenario-analysis.md` | Recommender | VaR, volatility, position sizing, bull/base/bear scenarios |
| `chart-patterns` | `SKILL.md`, `pattern-catalog.md`, `candlestick-patterns.md` | Analyzer | Technical pattern recognition, candlestick interpretation |
| `news-events` | `SKILL.md`, `news-extraction.md`, `corporate-actions.md` | Data Collector | News classification, sentiment scoring, corporate action tracking |

### b) Sub-Agents (3 files in `agents/`)

Each agent is a markdown prompt template with placeholder variables.

**`data-collector.md`** (model: haiku)
- **Phase 1 -- Scraping:** Find Tickertape URL via WebSearch, scrape with WebFetch, attempt StockTwits API
- **Phase 2 -- Financials:** Scrape Screener.in for quarterly results, annual P&L, balance sheet, cash flow; calculate intrinsic valuations (PE-based, Graham Number, PEG, DCF)
- **Phase 3 -- News:** Multi-query WebSearch, classify each item by category/sentiment/impact, identify red flags and catalysts
- **Outputs:** `_tickertape.json`, `_stocktwits.json`, `_financials.json`, `_news.json`
- **Tools:** Skill, WebSearch, WebFetch, Bash, Read, Write, Glob

**`analyzer.md`** (model: haiku)
- **Phase 1 -- Sentiment:** Weighted scoring from social (40%), market (30%), fundamental (30%) signals with confidence calculation
- **Phase 2 -- Technical:** Price position, RSI estimation, support/resistance levels, entry strategy with stop-loss and 3 profit targets
- **Phase 3 -- Peer Comparison:** Identify 4-6 sector peers, gather metrics, calculate percentile rankings and composite score, relative valuation
- **Outputs:** `_sentiment.json`, `_technical.json`, `_peers.json`
- **Tools:** Read, Write, Bash, WebSearch, WebFetch

**`recommender.md`** (model: sonnet)
- **Phase 1 -- Recommendation:** Score 6 dimensions (technical 25%, fundamental 25%, sentiment 15%, financial 15%, peer 10%, news 10%), compute composite, determine BUY/SELL/HOLD with conviction level
- **Phase 2 -- Risk:** Volatility and beta estimation, Value at Risk, max drawdown, position sizing for Rs.10L portfolio, risk-reward ratios, bull/base/bear scenario analysis
- **Outputs:** `_recommendation.json`, `_risk.json`
- **Tools:** Read, Write, Bash

### c) Hooks (2 Python files in `hooks/`)

Hooks intercept tool calls before and after execution, running inside `main.py`'s event loop.

**`pre_scrape_validator.py`** -- PreToolUse hook
- **WebFetch:** Validates URL domain against the allowed list in `settings.json`. Blocks any domain not in `[tickertape.in, api.stocktwits.com, screener.in, moneycontrol.com, trendlyne.com]`
- **Bash:** Blocks commands containing `curl`, `wget`, `nc`, or `ncat`
- Returns `{"decision": "deny", "reason": "..."}` on violation

**`post_analysis_logger.py`** -- PostToolUse hook
- **Write:** When a `data/*.json` file is written, logs filename + UTC timestamp to an in-memory list
- Injects `additionalContext` back to the agent: *"Successfully saved {filename}. Total analysis files written this session: N."*
- `get_write_log()` and `clear_write_log()` used by `main.py` for the session summary

### d) Scripts (6 Python files in `scripts/`)

| Script | Purpose | Called By |
|--------|---------|-----------|
| `validate_stock_data.py` | Validates JSON structure and value ranges by file type | Data Collector (Step 5) |
| `calculate_metrics.py` | Computes 52-week position, support/resistance, PE relative to sector, momentum | Analyzer (Step 5) |
| `financial_analysis.py` | Graham Number, PE-based fair value, PEG assessment, simplified DCF | Data Collector (Step 9) |
| `peer_comparison.py` | Percentile ranking, sector averages, composite peer score, relative valuation | Analyzer (Step 13) |
| `risk_calculator.py` | Volatility, beta, VaR (daily/monthly), max drawdown, position sizing | Recommender (risk phase) |
| `format_report.py` | Loads all `data/{slug}_*.json`, produces formatted text report | Orchestrator (Step 4, direct Bash) |

### e) Configuration (2 JSON files)

**`config/settings.json`**
```json
{
  "allowed_domains": ["www.tickertape.in", "api.stocktwits.com", "www.screener.in",
                       "www.moneycontrol.com", "trendlyne.com"],
  "rate_limit": {"delay_seconds": 3, "max_retries": 2},
  "agent": {"model": "sonnet", "max_turns": 25, "permission_mode": "acceptEdits"},
  "analysis_weights": {
    "technical": 0.25, "sentiment": 0.15, "fundamental": 0.25,
    "financial": 0.15, "peer": 0.10, "news": 0.10
  },
  "skills": ["scraping","financials","peer-analysis","news-events",
             "institutional","risk-management","chart-patterns"]
}
```

**`.claude/settings.local.json`** -- Permissions whitelist
```json
{
  "permissions": {
    "allow": [
      "WebSearch",
      "WebFetch(domain:www.tickertape.in)",
      "WebFetch(domain:api.stocktwits.com)",
      "WebFetch(domain:www.screener.in)",
      "WebFetch(domain:www.moneycontrol.com)",
      "WebFetch(domain:trendlyne.com)",
      "Bash(python scripts/*)"
    ]
  }
}
```

---

## 4. Worked Example: Mahindra & Mahindra Ltd

The following data comes from an actual run on **2026-02-10**.

### Input

```bash
python main.py "Mahindra and Mahindra Ltd"
```

Slug: `mahindra-and-mahindra-ltd` | Data directory: `data/`

---

### Step 1: Data Collection (haiku)

**Tickertape scrape** -- extracted via WebFetch from `www.tickertape.in`:

| Field | Value |
|-------|-------|
| Price | Rs.3,675.80 |
| PE Ratio | 33.52 |
| PB Ratio | 4.65 |
| Market Cap | Rs.4,33,323 Cr |
| 52-Week Range | Rs.2,425 -- Rs.3,839.90 |
| EPS | Rs.127.49 |
| Sector | Consumer Discretionary / Four Wheelers |
| Promoter Holding | 18.14% |
| FII + DII | 66.83% |

**StockTwits** -- API returned 403 Forbidden for tickers `MAHM`, `MAHM.NS`. The pre-scrape hook logged: *"Domain 'api.stocktwits.com' allowed"* but the API itself denied access. Result saved with `"error": "api_access_denied"`.

**Screener.in financials:**

| Metric | Value |
|--------|-------|
| D/E Ratio | 1.68 |
| ROE | 18.0% |
| ROCE | 14.0% |
| Revenue CAGR (3yr) | 21.0% |
| Profit CAGR (3yr) | 27.0% |
| OPM (latest) | 19-20% |
| Financial Health Score | 66/100 |
| Blended Fair Value | Rs.2,450 |

**News** -- 12 items collected, aggregate score **1.42** ("Very Positive"). Top headlines:
1. Rs.15,000 Cr Nagpur manufacturing facility investment (sentiment: +2, HIGH impact)
2. January 2026 tractor sales up 46% YoY (sentiment: +2, HIGH impact)
3. EV sales surge 386% YoY, market share jumps to 20% (sentiment: +2, HIGH impact)

One red flag identified: IndiGo trademark dispute over "6E" naming (severity: LOW, mitigated).

**Output files:** `_tickertape.json`, `_stocktwits.json`, `_financials.json`, `_news.json`

---

### Step 2: Analysis (haiku)

**Sentiment analysis:**

| Component | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Social (StockTwits) | 0.00 | 0% (redistributed) | 0.00 |
| Market signals | 0.58 | 50% | 0.29 |
| Fundamental signals | 0.28 | 50% | 0.14 |
| **Overall** | **0.43 Bullish** | | Confidence: **52%** |

**Technical analysis:**

| Indicator | Value |
|-----------|-------|
| Current Trend | Uptrend (Strong) |
| 52-Week Position | 88.44% |
| RSI (14d) | 53.77 (Neutral) |
| Support 1 / 2 | Rs.3,600 / Rs.3,535 |
| Resistance 1 / 2 | Rs.3,700 / Rs.3,818 |
| Technical Signal | Buy |
| Risk-Reward Ratio | 2.57:1 |

**Peer comparison** -- 5 peers analyzed (Maruti Suzuki, Tata Motors, Hyundai Motor India, Eicher Motors, Ashok Leyland):

| Metric | M&M | Sector Avg | Rank |
|--------|-----|-----------|------|
| PE Ratio | 33.52 | 40.44 | 4th (17% discount) |
| ROE | 18.0% | 27.3% | 5th |
| OPM | 19.0% | 16.63% | 2nd |
| Composite Score | 42 | -- | 3rd of 6 |
| Peer Fair Value | Rs.4,051 | -- | 9.25% upside |
| Verdict | Average | | |

**Output files:** `_sentiment.json`, `_technical.json`, `_peers.json`

---

### Step 3: Recommendation & Risk (sonnet)

**Recommendation:**

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Technical | +0.85 | 25% | +0.2125 |
| Sentiment | +0.43 | 15% | +0.0645 |
| Fundamental | -0.10 | 25% | -0.0250 |
| Financial | -0.66 | 15% | -0.0990 |
| Peer | -0.16 | 10% | -0.0160 |
| News | +1.00 | 10% | +0.1000 |
| **Composite** | | | **+0.33** |

| Field | Value |
|-------|-------|
| Recommendation | **HOLD** |
| Conviction | **MEDIUM** |
| Entry Price | Rs.3,600 |
| Stop Loss | Rs.3,420 (-5%) |
| Target 1 | Rs.3,820 (+6.1%, 1-3 months) |
| Target 2 | Rs.4,050 (+12.5%, 3-6 months) |
| Target 3 | Rs.4,300 (+19.4%, 6-12 months) |

**Risk assessment:**

| Metric | Value |
|--------|-------|
| Annual Volatility | 45.17% (High) |
| Estimated Beta | 1.2 |
| Daily VaR (95%) | Rs.4,681 per Rs.1L position |
| Max Drawdown Est. | 50% |
| Position Size (medium conviction) | 55 shares / Rs.1,98,000 for Rs.10L portfolio |
| Weighted R:R | 3.46:1 |
| Risk Rating | Moderate-High |

| Scenario | Price | Probability | Return |
|----------|-------|-------------|--------|
| Bull | Rs.4,779 | 25% | +30.0% |
| Base | Rs.4,140 | 50% | +12.6% |
| Bear | Rs.3,125 | 25% | -15.0% |
| **Expected** | **Rs.4,046** | | **+10.1%** |

**Output files:** `_recommendation.json`, `_risk.json`

---

### Step 4: Report Generation

```bash
python scripts/format_report.py mahindra-and-mahindra-ltd data/
```

Loads all 9 JSON files and produces a formatted analysis report saved to `data/mahindra-and-mahindra-ltd_ANALYSIS_REPORT.json`.

---

### Session Summary

```
ANALYSIS SUMMARY
============================================================
  Company:            Mahindra and Mahindra Ltd
  Slug:               mahindra-and-mahindra-ltd
  Sub-agents run:     3
    1. Data Collection
    2. Analysis
    3. Recommendation & Risk
  Files written:      9 data JSONs + 1 report
  Data directory:     data/
============================================================
```

---

## 5. Architecture Diagram

```
                          python main.py "Company Name"
                                     |
                                     v
                         +-----------------------+
                         |       main.py         |
                         |  IndianStockAnalyzer   |
                         +-----------+-----------+
                                     |
                     load_config()   |   load_agent_prompt() x3
                     slugify()       |   build_system_prompt()
                                     |
                                     v
                         +-----------------------+
                         |  Claude Agent SDK     |
                         |  query() async stream |
                         +-----------+-----------+
                                     |
                                     v
                    +--------------------------------+
                    |    Orchestrator (Sonnet)        |
                    |    model=sonnet, max_turns=25   |
                    +---+----------+----------+------+
                        |          |          |
              Task tool |  Task    |  Task    |  Bash
                        v          v          v     v
              +---------+  +-------+  +------+  +----------+
              |  Data   |  | Analy |  |Recom |  | format_  |
              |Collector|  |  zer  |  |mender|  | report.py|
              | (haiku) |  |(haiku)|  |(sonn)|  +----------+
              +----+----+  +---+---+  +---+--+
                   |           |          |
     +-------------+     +----+----+     +------+
     | Tools:       |     | Tools:  |     |Tools:|
     | WebSearch    |     | Read    |     | Read |
     | WebFetch ----+--+  | Write   |     | Write|
     | Bash         |  |  | Bash    |     | Bash |
     | Write        |  |  | WebSrch |     +---+--+
     | Read         |  |  | WebFtch |         |
     | Skill        |  |  +----+----+         |
     +------+-------+  |       |              |
            |           |       |              |
            v           v       v              v
   +--------+--------+  +------+------+  +----+------+
   | _tickertape.json |  |_sentiment   |  |_recomm    |
   | _stocktwits.json |  |_technical   |  |_risk.json |
   | _financials.json |  |_peers.json  |  +-----------+
   | _news.json       |  +-------------+
   +------------------+

   Hooks (applied in main.py event loop):
   +-----------------------------------------+
   | PreToolUse:  pre_scrape_validator.py     |
   |   WebFetch -> domain whitelist check     |
   |   Bash    -> block curl/wget/nc/ncat     |
   | PostToolUse: post_analysis_logger.py     |
   |   Write   -> log data/*.json writes      |
   +-----------------------------------------+

   Skills loaded at runtime (.claude/skills/):
   +-------------------------------------------+
   | scraping | financials | peer-analysis      |
   | news-events | institutional | risk-mgmt   |
   | chart-patterns                             |
   | (7 categories x 3 files = 21 skill files) |
   +-------------------------------------------+
```

---

## 6. Key Configuration Reference

### Analysis Weights

| Dimension | Weight | Source Data |
|-----------|--------|------------|
| Technical | 25% | `_technical.json` |
| Fundamental | 25% | `_tickertape.json`, `_financials.json` |
| Sentiment | 15% | `_sentiment.json` |
| Financial | 15% | `_financials.json` |
| Peer | 10% | `_peers.json` |
| News | 10% | `_news.json` |

### Allowed Domains

| Domain | Purpose |
|--------|---------|
| `www.tickertape.in` | Price, fundamentals, holdings |
| `api.stocktwits.com` | Social sentiment |
| `www.screener.in` | Financial statements, ratios |
| `www.moneycontrol.com` | News, analyst ratings |
| `trendlyne.com` | Shareholding, technicals |

### Agent Settings

| Setting | Value |
|---------|-------|
| Orchestrator model | Sonnet |
| Data Collector model | Haiku |
| Analyzer model | Haiku |
| Recommender model | Sonnet |
| Max turns | 25 |
| Permission mode | `acceptEdits` |

### Directory Structure

```
indian_stock_analyzer/
+-- main.py                     # Entry point and orchestrator
+-- config/
|   +-- settings.json           # Domains, weights, agent config
+-- .claude/
|   +-- settings.local.json     # Tool permission whitelist
|   +-- skills/                 # 7 skill categories, 21 .md files
|       +-- scraping/
|       +-- financials/
|       +-- peer-analysis/
|       +-- news-events/
|       +-- institutional/
|       +-- risk-management/
|       +-- chart-patterns/
+-- agents/
|   +-- data-collector.md       # Phase 1 prompt template
|   +-- analyzer.md             # Phase 2 prompt template
|   +-- recommender.md          # Phase 3 prompt template
+-- hooks/
|   +-- pre_scrape_validator.py # Domain & command validation
|   +-- post_analysis_logger.py # Write logging & context injection
+-- scripts/
|   +-- validate_stock_data.py  # JSON schema validation
|   +-- calculate_metrics.py    # Technical metric computation
|   +-- financial_analysis.py   # Intrinsic valuation models
|   +-- peer_comparison.py      # Relative ranking & valuation
|   +-- risk_calculator.py      # VaR, position sizing
|   +-- format_report.py        # Final report assembly
+-- data/                       # Output JSONs (per company slug)
+-- sessions/                   # Session files for --resume
+-- logs/                       # Runtime logs ({slug}_{timestamp}.log per run)
```

### File Inventory

| Category | Count | Files |
|----------|-------|-------|
| Agent prompts | 3 | `data-collector.md`, `analyzer.md`, `recommender.md` |
| Skill files | 21 | 7 categories x 3 files each (`SKILL.md` + 2 topic files) |
| Hook scripts | 2 | `pre_scrape_validator.py`, `post_analysis_logger.py` |
| Python scripts | 6 | `validate_stock_data.py`, `calculate_metrics.py`, `financial_analysis.py`, `peer_comparison.py`, `risk_calculator.py`, `format_report.py` |
| Config files | 2 | `config/settings.json`, `.claude/settings.local.json` |
| **Total project files** | **34** | |

---

*Generated from an actual Mahindra & Mahindra Ltd analysis run on 2026-02-10.*
