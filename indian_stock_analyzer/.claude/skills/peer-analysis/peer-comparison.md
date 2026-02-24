# Peer Comparison Framework

## 1. Peer Identification

### Step 1: Sector Classification
Determine the company's sector and sub-industry:
- Use Tickertape's sector classification from the scraped data
- Cross-reference with Screener.in peer section
- WebSearch: `"{company_name}" peers competitors India stock`

### Step 2: Peer Selection Criteria
Select 4-6 peers matching:
- **Same sub-industry** (e.g., "IT Services" not just "Technology")
- **Similar market cap tier**:
  - Large Cap: >Rs.20,000 Cr
  - Mid Cap: Rs.5,000-20,000 Cr
  - Small Cap: <Rs.5,000 Cr
- **Listed on NSE/BSE** (for data availability)
- **Operational** (exclude companies under restructuring/NCLT)

### Common Indian Sector Peer Groups
```
IT Services: TCS, Infosys, Wipro, HCL Tech, Tech Mahindra, LTIMindtree
Banking (Private): HDFC Bank, ICICI Bank, Kotak, Axis Bank, IndusInd
Banking (PSU): SBI, BoB, PNB, Canara Bank, Union Bank
Auto (Passenger): Maruti, Tata Motors, M&M, Hyundai Motor India
Auto (2W): Hero Moto, Bajaj Auto, TVS Motor, Eicher Motors
FMCG: HUL, ITC, Nestle, Dabur, Marico, Godrej Consumer
Pharma: Sun Pharma, Dr Reddy's, Cipla, Lupin, Aurobindo, Divi's
Metals: Tata Steel, JSW Steel, Hindalco, Vedanta, SAIL
Oil & Gas: Reliance, ONGC, IOC, BPCL, HPCL
Telecom: Bharti Airtel, Jio (Reliance), Vodafone Idea
Cement: UltraTech, Ambuja, ACC, Shree Cement, Dalmia Bharat
Real Estate: DLF, Godrej Properties, Oberoi Realty, Prestige, Brigade
Power: NTPC, Power Grid, Tata Power, Adani Power, JSW Energy
```

## 2. Metrics to Compare

### Valuation Metrics
| Metric | What It Tells You |
|--------|-------------------|
| PE Ratio (TTM) | Earnings multiple — lower may be cheaper |
| PB Ratio | Asset value multiple — important for banks |
| EV/EBITDA | Enterprise value multiple — debt-adjusted |
| PEG Ratio | Growth-adjusted PE — accounts for growth rate |
| Dividend Yield | Income return — higher = more income |

### Profitability Metrics
| Metric | What It Tells You |
|--------|-------------------|
| ROE % | Shareholder return efficiency |
| ROCE % | Capital efficiency (includes debt) |
| OPM % | Operating margin — pricing power |
| NPM % | Net margin — bottom-line efficiency |
| Asset Turnover | Revenue per unit of assets |

### Growth Metrics
| Metric | What It Tells You |
|--------|-------------------|
| Revenue Growth (3Y CAGR) | Top-line momentum |
| Profit Growth (3Y CAGR) | Bottom-line momentum |
| EPS Growth (3Y CAGR) | Per-share earnings growth |

### Financial Health
| Metric | What It Tells You |
|--------|-------------------|
| Debt/Equity | Leverage risk |
| Interest Coverage | Ability to service debt |
| Current Ratio | Short-term liquidity |
| FCF Yield | Cash generation vs price |
| Promoter Holding % | Skin in the game |

## 3. Comparison Output Schema

```json
{
  "target_company": "Company Name",
  "target_ticker": "TICKER",
  "sector": "Sector",
  "sub_industry": "Sub-Industry",
  "peers": [
    {
      "name": "Peer Name",
      "ticker": "PEER_TICKER",
      "market_cap_cr": 0,
      "pe_ratio": 0.00,
      "pb_ratio": 0.00,
      "roe": 0.00,
      "roce": 0.00,
      "opm": 0.00,
      "debt_to_equity": 0.00,
      "revenue_growth_3yr": 0.00,
      "profit_growth_3yr": 0.00,
      "promoter_holding": 0.00
    }
  ],
  "sector_averages": {
    "pe_ratio": 0.00,
    "pb_ratio": 0.00,
    "roe": 0.00,
    "opm": 0.00
  },
  "relative_position": {
    "pe_vs_sector": "Premium|Discount|Inline",
    "pe_percentile": 0,
    "roe_vs_sector": "Above|Below|Inline",
    "roe_percentile": 0,
    "growth_vs_sector": "Above|Below|Inline",
    "overall_rank": 0,
    "out_of": 0
  },
  "peer_verdict": "string",
  "analyzed_at": "ISO-8601 timestamp"
}
```

## 4. Ranking Methodology

### Composite Peer Score (0-100)
Weight each dimension:
- Valuation attractiveness: 30% (lower PE/PB vs peers = better)
- Profitability: 25% (higher ROE/ROCE/OPM = better)
- Growth: 25% (higher revenue/profit growth = better)
- Financial health: 20% (lower debt, higher coverage = better)

For each metric, rank the target among peers (percentile).
Composite = weighted average of percentile ranks.

### Interpretation
- Score 75-100: Best-in-class among peers
- Score 50-75: Above average
- Score 25-50: Below average
- Score 0-25: Laggard — needs compelling reason to invest
