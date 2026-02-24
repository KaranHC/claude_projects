# Relative Valuation Methods

## 1. Peer-Relative PE Valuation

### Method
```
Target's Fair PE = Sector Median PE * Quality Adjustment Factor

Quality Adjustment Factor (0.7x to 1.5x) based on:
+0.1 for each: Superior ROE, Higher growth, Lower debt, Better margins, Higher promoter holding
-0.1 for each: Inferior ROE, Lower growth, Higher debt, Worse margins, Lower promoter holding

Fair Price = Target's Fair PE * Target's EPS
```

### Example
If sector median PE is 25x, and target has:
- ROE above sector (+0.1)
- Growth above sector (+0.1)
- Debt below sector (+0.1)
- Margins inline (0)
- Promoter above sector (+0.1)
Quality Factor = 1.0 + 0.4 = 1.4x
Fair PE = 25 * 1.4 = 35x

## 2. Peer-Relative PB Valuation (for Banks/NBFCs)

### Method
```
Fair P/B = Sector Median P/B * (Target ROE / Sector Median ROE)

Adjustment:
- If ROE is 1.5x sector → deserves 1.5x P/B premium
- Floor: 0.5x sector P/B (even worst banks have floor)
- Ceiling: 3.0x sector P/B (diminishing returns)
```

### Indian Banking P/B Benchmarks
- High-quality private banks (HDFC, Kotak): 3-5x P/B
- Good private banks (ICICI, Axis): 2-3x P/B
- Average private banks: 1-2x P/B
- Good PSU banks (SBI): 1-2x P/B
- Weak PSU banks: 0.5-1x P/B

## 3. EV/EBITDA Relative Valuation

### When to Prefer Over PE
- Companies with different capital structures (debt levels)
- Companies with different depreciation policies
- Companies with different tax rates
- Cross-border comparisons

### Method
```
Fair EV/EBITDA = Sector Median * (1 + Growth Premium - Risk Discount)

Growth Premium = (Target EBITDA Growth - Sector Median Growth) * 0.5
Risk Discount = Additional risk factors * 0.1 each

Fair EV = Fair EV/EBITDA * Target EBITDA
Fair Equity = Fair EV - Net Debt + Cash
Fair Price = Fair Equity / Shares Outstanding
```

## 4. Premium/Discount Justification Framework

### Factors Justifying Premium Valuation
1. **Market leadership**: #1 or #2 in sector by revenue
2. **Consistent execution**: 5+ years of meeting/beating guidance
3. **Competitive moat**: Brand, network effect, switching cost, patents
4. **Superior capital allocation**: High ROIC, smart M&A, buybacks
5. **Secular tailwind**: Structural demand growth in segment
6. **ESG leadership**: Strong governance, sustainability practices

### Factors Warranting Discount
1. **Governance concerns**: Related party transactions, pledged shares
2. **Cyclical peak**: At top of earnings cycle
3. **Concentration risk**: Single client/product dependency
4. **Execution risk**: History of missing targets
5. **Regulatory overhang**: Pending policy/regulatory changes
6. **Promoter issues**: Low/declining holding, pledged shares, legal issues

### Maximum Justified Premium/Discount
- Premium over sector: Typically capped at +50% (1.5x sector PE)
- Discount to sector: Floor at -50% (0.5x sector PE) for viable companies
- Beyond these bounds: extraordinary circumstances only

## 5. Output: Relative Valuation Summary

```json
{
  "pe_relative_fair_value": 0.00,
  "pb_relative_fair_value": 0.00,
  "ev_ebitda_fair_value": 0.00,
  "blended_fair_value": 0.00,
  "current_price": 0.00,
  "premium_discount_to_fair": 0.00,
  "premium_justification": ["factor 1", "factor 2"],
  "discount_factors": ["factor 1"],
  "relative_verdict": "Attractive|Fair|Expensive"
}
```
