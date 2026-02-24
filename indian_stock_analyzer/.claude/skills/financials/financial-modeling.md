# Financial Modeling & Valuation Methods

## 1. Discounted Cash Flow (DCF)

### When to Use
- Companies with positive and predictable free cash flow
- NOT suitable for: early-stage companies, banks/NBFCs, cyclical at bottom

### Methodology
```
Intrinsic Value = Sum of (FCF_t / (1 + WACC)^t) + Terminal Value / (1 + WACC)^n

Where:
- FCF_t = Free Cash Flow in year t
- WACC = Weighted Average Cost of Capital
- Terminal Value = FCF_n * (1 + g) / (WACC - g)
- g = Terminal growth rate (typically 3-5% for Indian companies)
- n = Projection period (typically 5-10 years)
```

### WACC for Indian Companies
- Risk-free rate: Current 10-year India government bond yield (~7%)
- Equity risk premium: 6-8% for India
- Beta: Company-specific (use 1.0 if unavailable)
- Cost of equity = Risk-free + Beta * ERP
- Typical range: 12-16% for Indian companies

### Simplified DCF (for available data)
When only limited data is available:
```
Fair Value = (Current FCF * Growth Multiple) / Shares Outstanding

Growth Multiple Guide:
- High growth (>20% CAGR): 20-30x FCF
- Moderate growth (10-20%): 12-20x FCF
- Low growth (<10%): 8-12x FCF
- No growth/declining: 5-8x FCF
```

## 2. Relative Valuation

### PE-Based Fair Value
```
Fair Value = EPS * Fair PE Multiple

Fair PE Multiple = Sector Average PE * (1 + Growth Premium/Discount)

Growth Premium:
- Company growth > Sector growth → premium (up to 1.5x sector PE)
- Company growth < Sector growth → discount (down to 0.7x sector PE)
```

### EV/EBITDA Valuation
```
Fair EV = EBITDA * Fair EV/EBITDA Multiple
Fair Equity Value = Fair EV - Net Debt
Fair Price = Fair Equity Value / Shares Outstanding

Indian Market EV/EBITDA Ranges:
- IT Services: 15-25x
- FMCG: 25-40x
- Banking: Not applicable (use P/B)
- Auto: 8-15x
- Pharma: 12-20x
- Metals/Mining: 5-10x
```

### PEG Ratio (Growth-Adjusted PE)
```
PEG = PE Ratio / Earnings Growth Rate (%)

Interpretation:
- PEG < 0.5: Significantly undervalued (verify growth is sustainable)
- PEG 0.5-1.0: Undervalued to fairly valued
- PEG 1.0-1.5: Fairly valued
- PEG 1.5-2.0: Moderately overvalued
- PEG > 2.0: Overvalued (unless exceptional moat)
```

## 3. Graham Number (Value Investing)

### Formula
```
Graham Number = sqrt(22.5 * EPS * Book Value Per Share)

If current price < Graham Number: potentially undervalued
Margin of Safety = (Graham Number - Current Price) / Graham Number * 100
```

### Requirements
- Positive EPS (trailing 12 months)
- Positive book value
- Works best for established, profitable companies

## 4. Dividend Discount Model (DDM)

### When to Use
- Companies with consistent dividend history (>5 years)
- Stable or growing dividend payouts
- Common for: Utilities, mature FMCG, PSU companies

### Gordon Growth Model
```
Fair Value = Dividend Per Share * (1 + g) / (r - g)

Where:
- g = Sustainable dividend growth rate
- r = Required rate of return (cost of equity, typically 12-15%)
- g estimate = ROE * Retention Ratio, or historical dividend CAGR
```

## 5. Sum-of-Parts (SOTP) Valuation

### When to Use
- Conglomerates (Tata, Reliance, ITC, L&T)
- Companies with distinct business segments

### Method
- Value each business segment separately using appropriate multiples
- Add value of investments/subsidiaries at market value
- Subtract holding company discount (10-20%)

## 6. Fair Value Synthesis

### Combining Multiple Methods
```json
{
  "dcf_value": 0.00,
  "pe_fair_value": 0.00,
  "graham_number": 0.00,
  "ev_ebitda_value": 0.00,
  "ddm_value": 0.00,
  "weighted_fair_value": 0.00,
  "current_price": 0.00,
  "upside_downside_percent": 0.00,
  "margin_of_safety": 0.00,
  "valuation_verdict": "Undervalued|Fairly Valued|Overvalued"
}
```

### Weight Assignment
- For profitable, FCF-positive companies: DCF 40%, PE 30%, EV/EBITDA 20%, Graham 10%
- For high-growth companies: PE/PEG 50%, EV/EBITDA 30%, DCF 20%
- For dividend payers: DDM 30%, PE 30%, DCF 20%, Graham 20%
- For loss-making: EV/Revenue 50%, Price/Book 30%, Peer comparison 20%
