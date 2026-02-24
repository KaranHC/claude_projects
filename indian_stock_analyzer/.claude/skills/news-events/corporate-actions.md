# Corporate Actions & Events Analysis

## 1. Types of Corporate Actions

### Positive Signals
| Action | Impact | Typical Price Effect |
|--------|--------|---------------------|
| **Dividend (Special)** | Shows cash confidence | Mildly positive |
| **Buyback** | Signals undervaluation by management | Positive (5-15% upside) |
| **Bonus Issue** | Confidence in growth, improves liquidity | Positive short-term |
| **Stock Split** | Improves retail accessibility | Neutral to mild positive |
| **Preferential Allotment** | Strategic investor interest | Depends on investor quality |
| **Promoter Buying** | Insider confidence | Strongly positive signal |

### Negative Signals
| Action | Impact | Typical Price Effect |
|--------|--------|---------------------|
| **Promoter Selling** | Insider reducing exposure | Negative signal |
| **Promoter Pledge Increase** | Financial stress signal | Negative |
| **QIP/FPO (at discount)** | Dilution at low price | Negative |
| **Rights Issue** | May signal capital need | Mixed (depends on purpose) |
| **Debt Restructuring** | Financial stress | Strongly negative |
| **Auditor Resignation** | Governance red flag | Strongly negative |

### Neutral/Context-Dependent
| Action | Impact | Depends On |
|--------|--------|------------|
| **Merger/Demerger** | Restructuring | Synergies, valuations |
| **Capex Announcement** | Growth investment | ROI expectations, funding |
| **JV/Partnership** | Strategic move | Partner quality, terms |
| **Name Change** | Rebranding | Reason behind change |

## 2. Earnings Calendar

### Indian Earnings Season
- Q1 (Apr-Jun): Results in July-August
- Q2 (Jul-Sep): Results in October-November
- Q3 (Oct-Dec): Results in January-February
- Q4 (Jan-Mar): Results in April-May (with annual)

### What to Track
- **Result date**: When are results expected?
- **Consensus estimates**: What are Street expectations?
- **Previous quarter trend**: Beat/miss/inline pattern
- **Management guidance**: Any forward-looking statements

### Earnings Quality Assessment
```
Earnings Quality Score (0-100):
+20: Revenue growth > profit growth (sustainable)
+20: Cash from operations > net profit (cash backing)
+15: Consistent margins (OPM variance < 3% QoQ)
+15: Low exceptional items (< 5% of PBT)
+15: Working capital improving (lower days cycle)
+15: Tax rate normal (no one-time benefits)
```

## 3. Shareholding Changes

### Quarterly Shareholding Pattern Analysis
Track quarter-over-quarter changes in:
```
Promoter holding: Increasing → confidence, Decreasing → concern
FII holding: Increasing → global interest, Decreasing → risk-off
DII/MF holding: Increasing → domestic institutional support
Retail holding: Increasing → late-stage rally risk, Decreasing → smart money exit
```

### Significant Thresholds
- Promoter crosses below 50%: Loss of majority → governance risk
- FII crosses 25%: Strong international validation
- MF holding doubles: Entering major fund portfolios
- Pledge > 30% of promoter holding: Financial stress alert

## 4. Impact Assessment Framework

### Corporate Action Impact Score
```
Impact Score = Base Impact * Magnitude Factor * Timing Factor

Base Impact:
- Buyback/Special Dividend: +2
- Promoter buying: +2
- Bonus/Split: +1
- Regular dividend: +0.5
- QIP: -1
- Promoter selling: -2
- Pledge increase: -2
- Auditor issue: -3

Magnitude Factor (0.5 to 2.0):
- Based on size relative to market cap or holding

Timing Factor:
- Within last 30 days: 1.0
- 30-90 days: 0.5
- >90 days: 0.2
```

## 5. Output Schema

```json
{
  "company": "Company Name",
  "ticker": "TICKER",
  "recent_corporate_actions": [
    {
      "action": "string",
      "date": "YYYY-MM-DD",
      "details": "string",
      "impact": "Positive|Negative|Neutral",
      "impact_score": 0.00
    }
  ],
  "shareholding_changes": {
    "promoter_change_qoq": 0.00,
    "fii_change_qoq": 0.00,
    "dii_change_qoq": 0.00,
    "signal": "Accumulation|Distribution|Stable"
  },
  "next_earnings": {
    "expected_date": "YYYY-MM-DD",
    "quarter": "Q3 FY25",
    "consensus_revenue_growth": 0.00,
    "consensus_profit_growth": 0.00
  },
  "earnings_quality_score": 0,
  "corporate_action_net_score": 0.00,
  "analyzed_at": "ISO-8601 timestamp"
}
```
