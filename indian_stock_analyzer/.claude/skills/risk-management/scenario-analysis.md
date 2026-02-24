# Scenario Analysis & Stress Testing

## 1. Three-Scenario Model

### Bull Case (25% probability)
Everything goes right:
- Revenue growth at top of guidance range
- Margin expansion from operating leverage
- Sector tailwinds (favorable regulation, demand surge)
- PE re-rating (market assigns higher multiple)
- FII buying accelerates

### Base Case (50% probability)
Business as expected:
- Revenue growth inline with consensus
- Margins stable or slight improvement
- No major positive/negative surprises
- Valuation stays at current multiples

### Bear Case (25% probability)
Multiple things go wrong:
- Revenue growth disappoints
- Margin compression (input costs, competition)
- Sector headwinds (regulation, demand slowdown)
- PE de-rating (market assigns lower multiple)
- FII selling pressure

### Price Target Estimation
```
Bull Case Price = Bull EPS * Bull PE Multiple
Base Case Price = Base EPS * Base PE Multiple
Bear Case Price = Bear EPS * Bear PE Multiple

Expected Value = (0.25 * Bull) + (0.50 * Base) + (0.25 * Bear)
```

## 2. Stress Test Scenarios

### Market Crash Scenario
```
Global crisis (like 2020, 2008):
- Nifty falls 30-40%
- Stock falls = Nifty fall * Beta * 1.2 (crisis beta expansion)
- Recovery time: 12-24 months historically

Questions:
- Can you hold through a 40-60% drawdown?
- Does the company have enough cash to survive 12 months of stress?
- Is the debt manageable even with 50% revenue drop?
```

### Sector-Specific Stress
```
IT Services: US recession, visa restrictions, AI displacement
Banking: NPA cycle, rate reversal, regulatory tightening
Auto: Demand slowdown, EV transition, emission norms
Pharma: Price control, USFDA observations, patent cliff
FMCG: Rural slowdown, commodity inflation, competitive intensity
Metals: Global demand collapse, China dumping, carbon regulation
Real Estate: Rate hike cycle, RERA delays, demand collapse
```

### Company-Specific Stress
```
Key Person Risk: What if CEO/founder exits?
Customer Concentration: What if top client churns?
Regulatory Risk: What if adverse policy change?
Technology Risk: What if product becomes obsolete?
Governance Risk: What if accounting irregularity surfaces?
```

## 3. Sensitivity Analysis

### PE Sensitivity Table
```
                    PE Multiple
EPS Growth    | 15x   | 20x   | 25x   | 30x   | 35x
------------- |-------|-------|-------|-------|------
-10%          | ___   | ___   | ___   | ___   | ___
  0%          | ___   | ___   | ___   | ___   | ___
+10%          | ___   | ___   | ___   | ___   | ___
+20%          | ___   | ___   | ___   | ___   | ___
+30%          | ___   | ___   | ___   | ___   | ___

Fill with: EPS * (1 + growth) * PE Multiple
Highlight current price equivalent cell
```

### Margin of Safety Analysis
```
At current price:
- PE must stay above X for breakeven
- EPS must grow at least Y% to justify current price
- If growth halves, stock is Z% overvalued
- If PE contracts to sector average, downside is W%
```

## 4. Indian Market Macro Risks

### Systematic Risks (affect all stocks)
1. **RBI Rate Cycle**: Rate hike = negative for growth, positive for banks (short-term)
2. **Rupee Depreciation**: Negative for importers, positive for exporters (IT, Pharma)
3. **FII Outflows**: When DXY strengthens, FIIs pull out of India
4. **Crude Oil Price**: India imports 80%+ of oil. High crude = negative for economy
5. **Election Cycle**: Pre-election spending positive, post-election uncertainty
6. **Global Risk-Off**: Geopolitical events, US recession risk
7. **Monsoon**: Still affects rural demand and agri-linked sectors

### Current Macro Assessment Framework
```json
{
  "rbi_stance": "Hawkish|Neutral|Dovish",
  "rate_direction": "Rising|Stable|Falling",
  "rupee_trend": "Strengthening|Stable|Weakening",
  "fii_flow_trend": "Net Buyer|Neutral|Net Seller",
  "crude_oil_level": "Low(<$70)|Moderate($70-90)|High(>$90)",
  "market_valuation": "Cheap|Fair|Expensive",
  "macro_risk_level": "Low|Moderate|High"
}
```

## 5. Output Schema

```json
{
  "company": "Company Name",
  "scenarios": {
    "bull_case": {
      "probability": 0.25,
      "target_price": 0.00,
      "upside_percent": 0.00,
      "assumptions": ["assumption 1", "assumption 2"]
    },
    "base_case": {
      "probability": 0.50,
      "target_price": 0.00,
      "upside_percent": 0.00,
      "assumptions": ["assumption 1", "assumption 2"]
    },
    "bear_case": {
      "probability": 0.25,
      "target_price": 0.00,
      "downside_percent": 0.00,
      "assumptions": ["assumption 1", "assumption 2"]
    },
    "expected_value": 0.00,
    "expected_return": 0.00
  },
  "stress_tests": {
    "market_crash_impact": 0.00,
    "sector_stress_impact": 0.00,
    "survival_assessment": "Strong|Adequate|Weak"
  },
  "macro_risks": {
    "most_relevant_risks": ["risk 1", "risk 2"],
    "macro_risk_level": "Low|Moderate|High"
  },
  "analyzed_at": "ISO-8601 timestamp"
}
```
