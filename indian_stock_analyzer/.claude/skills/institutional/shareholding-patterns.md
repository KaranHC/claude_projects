# Shareholding Pattern Analysis

## 1. Data Extraction

### Sources
Shareholding data is disclosed quarterly by all listed companies:
- Screener.in: `#shareholding` section on company page
- Tickertape: Shareholding tab on stock page
- BSE: Annual Report → Shareholding Pattern

### Key Categories
```
1. Promoter & Promoter Group
   - Indian Promoters
   - Foreign Promoters
   - Shares pledged or encumbered

2. Foreign Institutional Investors (FII/FPI)
   - Foreign Portfolio Investors
   - Foreign Venture Capital

3. Domestic Institutional Investors (DII)
   - Mutual Funds
   - Banks & Financial Institutions
   - Insurance Companies (LIC, etc.)
   - Pension Funds (EPFO, NPS)

4. Public/Retail
   - Individual shareholders (small)
   - Individual shareholders (large, >Rs.2L)
   - NRI
   - HUF
   - Bodies Corporate
   - Trusts
```

## 2. Analysis Framework

### Promoter Analysis
```
Signal Matrix:
- Promoter holding >70%: Very high confidence (but low free float risk)
- Promoter holding 50-70%: Strong confidence
- Promoter holding 35-50%: Moderate (check institutional support)
- Promoter holding <35%: Low → needs very strong institutional backing

Trend Analysis:
- Increasing 3 consecutive quarters: Strong BUY signal
- Stable (±0.5%): Neutral
- Decreasing 3 consecutive quarters: CAUTION signal

Pledge Analysis:
- No pledge: Clean ✓
- Pledge <10% of holding: Acceptable
- Pledge 10-30%: Monitor closely
- Pledge >30%: RED FLAG — financial stress risk
- Pledge increasing: Deteriorating signal
```

### FII/FPI Analysis
```
FII Flows Signal:
- FII increasing + Price rising: Confirmed uptrend (strong BUY)
- FII increasing + Price falling: Accumulation phase (contrarian BUY)
- FII decreasing + Price rising: Distribution (CAUTION — rally may end)
- FII decreasing + Price falling: Confirmed downtrend (AVOID)

FII Holding Levels:
- >30%: Heavy FII ownership (vulnerable to global risk-off)
- 15-30%: Healthy FII interest
- 5-15%: Under-owned by FIIs (potential re-rating if discovered)
- <5%: Off FII radar (could be opportunity or trap)
```

### DII/Mutual Fund Analysis
```
MF Holding Significance:
- In top 25 MF holdings of 5+ schemes: Widely held, consensus pick
- Newly entering MF portfolios: Early accumulation signal
- MFs reducing → but FIIs increasing: Rotation, not concern
- Both MFs and FIIs reducing: Broad institutional exit — RED FLAG

Key MF Investors to Watch:
- SBI MF, HDFC MF, ICICI Pru MF (largest AUM)
- Parag Parikh Flexi Cap (quality bias)
- Quant MF (momentum bias)
- PPFAS, Motilal Oswal (concentrated portfolios)
```

## 3. Smart Money Score

### Calculation
```python
smart_money_score = 0  # Range: -100 to +100

# Promoter signals (weight: 30%)
if promoter_change > 0.5: smart_money_score += 15
elif promoter_change < -0.5: smart_money_score -= 15
if pledge_percent > 30: smart_money_score -= 15
elif pledge_percent == 0: smart_money_score += 10

# FII signals (weight: 30%)
if fii_change > 1.0: smart_money_score += 20
elif fii_change > 0: smart_money_score += 10
elif fii_change < -1.0: smart_money_score -= 20
elif fii_change < 0: smart_money_score -= 10

# DII signals (weight: 20%)
if dii_change > 1.0: smart_money_score += 15
elif dii_change > 0: smart_money_score += 7
elif dii_change < -1.0: smart_money_score -= 15

# Consistency bonus (weight: 20%)
if all_three_increasing: smart_money_score += 20
elif all_three_decreasing: smart_money_score -= 20
```

### Interpretation
- **+60 to +100**: Very strong institutional conviction — high confidence BUY
- **+20 to +60**: Positive institutional flow — supports BUY thesis
- **-20 to +20**: Mixed signals — no clear institutional direction
- **-60 to -20**: Negative institutional flow — supports SELL/AVOID
- **-100 to -60**: Strong institutional exit — high confidence SELL

## 4. Output Schema

```json
{
  "company": "Company Name",
  "ticker": "TICKER",
  "shareholding_current": {
    "promoter_percent": 0.00,
    "promoter_pledge_percent": 0.00,
    "fii_percent": 0.00,
    "dii_percent": 0.00,
    "mf_percent": 0.00,
    "retail_percent": 0.00
  },
  "shareholding_changes": {
    "promoter_change_1q": 0.00,
    "promoter_change_4q": 0.00,
    "fii_change_1q": 0.00,
    "fii_change_4q": 0.00,
    "dii_change_1q": 0.00,
    "dii_change_4q": 0.00
  },
  "smart_money_score": 0,
  "smart_money_signal": "Strong Buy|Buy|Neutral|Sell|Strong Sell",
  "key_observations": [
    "Observation 1",
    "Observation 2"
  ],
  "risk_flags": [],
  "analyzed_at": "ISO-8601 timestamp"
}
```
