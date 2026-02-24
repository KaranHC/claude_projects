# Risk Models & Position Sizing

## 1. Volatility Assessment

### Historical Volatility Estimation
When full price history is unavailable, estimate from available data:

```
From 52-week range:
Estimated Annual Volatility = (52W High - 52W Low) / ((52W High + 52W Low) / 2) * 100

Volatility Categories:
- <20%: Low volatility (large-cap blue chips)
- 20-35%: Moderate volatility (typical mid-large cap)
- 35-50%: High volatility (mid-small cap, cyclicals)
- >50%: Very high volatility (small cap, turnarounds)
```

### Indian Market Benchmarks
- Nifty 50 annual volatility: ~15-18%
- Nifty Midcap 150: ~20-25%
- Nifty Smallcap 250: ~25-35%
- Individual stocks: typically 1.5-3x their index volatility

## 2. Beta Estimation

### From Available Data
```
Simplified Beta = Stock's 52W Range % / Nifty 50's 52W Range %

Interpretation:
- Beta < 0.8: Defensive (FMCG, Pharma, Utilities)
- Beta 0.8-1.2: Market-aligned
- Beta 1.2-1.5: Aggressive (Banks, Auto, Metals)
- Beta > 1.5: Highly aggressive (Small caps, Realty, Infra)
```

### Sector Beta Benchmarks (Indian Market)
```
IT Services: 0.7-1.0
FMCG: 0.5-0.8
Pharma: 0.6-0.9
Banking (Private): 1.0-1.3
Banking (PSU): 1.2-1.6
Auto: 1.0-1.4
Metals: 1.3-1.8
Real Estate: 1.4-2.0
Oil & Gas: 0.8-1.2
Telecom: 0.8-1.1
Cement: 0.9-1.3
Power: 0.8-1.2
```

## 3. Value at Risk (VaR) Estimation

### Parametric VaR
```
Daily VaR (95%) = Position Value * Daily Volatility * 1.645
Daily VaR (99%) = Position Value * Daily Volatility * 2.326

Where Daily Volatility = Annual Volatility / sqrt(252)
```

### Example
Stock price: Rs.1000, Position: 100 shares, Annual Vol: 30%
- Daily Vol = 30% / 15.87 = 1.89%
- Daily VaR (95%) = Rs.100,000 * 0.0189 * 1.645 = Rs.3,109
- Meaning: 95% confident daily loss won't exceed Rs.3,109

### Monthly VaR
```
Monthly VaR = Daily VaR * sqrt(21)  // 21 trading days
```

## 4. Maximum Drawdown Estimation

### From 52-Week Data
```
Observed Drawdown = (52W High - Current Price) / 52W High * 100
// If price is below 52W high

Historical Max Drawdown Estimates by Volatility:
- Low vol stocks: 15-25% max drawdown
- Moderate vol: 25-40% max drawdown
- High vol: 40-60% max drawdown
- Very high vol: 50-80% max drawdown
```

### Recovery Time Estimation
```
Expected Recovery Time (months) = Max Drawdown % / 2
// Rule of thumb: takes about 2 months per 1% of drawdown to recover

Example: 30% drawdown → ~15 months expected recovery
```

## 5. Position Sizing

### Fixed Percentage Risk Model
```
Position Size = (Portfolio Value * Risk Per Trade) / (Entry Price - Stop Loss)

Recommended Risk Per Trade:
- High conviction: 2.0% of portfolio
- Medium conviction: 1.0% of portfolio
- Low conviction: 0.5% of portfolio
```

### Example
Portfolio: Rs.10,00,000, Stock: Rs.500, Stop Loss: Rs.450
- Risk per share = Rs.500 - Rs.450 = Rs.50
- High conviction: (10,00,000 * 0.02) / 50 = 400 shares = Rs.2,00,000
- Medium conviction: (10,00,000 * 0.01) / 50 = 200 shares = Rs.1,00,000
- Low conviction: (10,00,000 * 0.005) / 50 = 100 shares = Rs.50,000

### Kelly Criterion (Optimal Position Size)
```
Kelly % = (Win Rate * Avg Win / Avg Loss - (1 - Win Rate)) / (Avg Win / Avg Loss)

Simplified for stock recommendations:
- Favorable setup (>60% win rate, 1:3 R:R): Kelly ≈ 25-30% → use half-Kelly = 12-15%
- Moderate setup (50% win rate, 1:2 R:R): Kelly ≈ 15% → half-Kelly = 7-8%
- Speculative (40% win rate, 1:4 R:R): Kelly ≈ 10% → half-Kelly = 5%

Always use half-Kelly or less for safety.
```

## 6. Risk-Reward Assessment

### Minimum Acceptable Ratios
```
Risk = Entry Price - Stop Loss
Reward = Target Price - Entry Price
R:R Ratio = Reward / Risk

Minimum R:R by conviction:
- HIGH conviction: Minimum 1:2 (risk 1 to make 2)
- MEDIUM conviction: Minimum 1:2.5
- LOW conviction: Minimum 1:3

If R:R < 1:2 for any setup → PASS (don't recommend)
```

### Multi-Target R:R
```
Weighted R:R = (P1*R1 + P2*R2 + P3*R3) / Risk

Where P1,P2,P3 = probability of reaching each target
R1,R2,R3 = reward at each target

Typical probability assignment:
- Target 1 (conservative): 70% probability
- Target 2 (moderate): 45% probability
- Target 3 (aggressive): 25% probability
```

## 7. Output Schema

```json
{
  "company": "Company Name",
  "ticker": "TICKER",
  "volatility": {
    "estimated_annual": 0.00,
    "volatility_category": "Low|Moderate|High|Very High",
    "estimated_beta": 0.00
  },
  "value_at_risk": {
    "daily_var_95": 0.00,
    "daily_var_99": 0.00,
    "monthly_var_95": 0.00
  },
  "drawdown": {
    "current_from_high": 0.00,
    "estimated_max_drawdown": 0.00,
    "estimated_recovery_months": 0
  },
  "position_sizing": {
    "high_conviction_shares": 0,
    "high_conviction_value": 0.00,
    "medium_conviction_shares": 0,
    "medium_conviction_value": 0.00,
    "low_conviction_shares": 0,
    "low_conviction_value": 0.00,
    "assumed_portfolio_value": 1000000
  },
  "risk_reward": {
    "risk_per_share": 0.00,
    "reward_target_1": 0.00,
    "reward_target_2": 0.00,
    "reward_target_3": 0.00,
    "rr_ratio_t1": "1:X",
    "rr_ratio_t2": "1:X",
    "weighted_rr": "1:X"
  },
  "risk_rating": "Low|Moderate|High|Very High",
  "analyzed_at": "ISO-8601 timestamp"
}
```
