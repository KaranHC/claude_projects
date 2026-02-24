# Screener.in Data Extraction Patterns

## 1. URL Resolution

### Finding the Correct Page
- Primary URL: `https://www.screener.in/company/{TICKER}/consolidated/`
- Standalone fallback: `https://www.screener.in/company/{TICKER}/`
- Use WebSearch: `site:screener.in {company_name}` to resolve the correct ticker slug

### Common Ticker Formats
- NSE ticker: `TCS`, `INFY`, `RELIANCE`, `M&M` (note: `&` in URL-encoded form)
- BSE code fallback: 6-digit code like `500325`

## 2. Page Structure

Screener.in pages contain structured data in HTML tables. Key sections:

### Company Header
- Company name, BSE/NSE codes
- Current price, market cap
- Book value, stock PE, dividend yield
- ROCE, ROE

### Quarterly Results Table
Located under `#quarters` section. Columns:
```
| Quarter | Sales | Expenses | Operating Profit | OPM% | Other Income | Interest | Depreciation | PBT | Tax | Net Profit | EPS |
```
Extract last 8-12 quarters for trend analysis.

### Profit & Loss (Annual)
Located under `#profit-loss` section. Same columns as quarterly but annual figures.
Extract last 5-10 years.

### Balance Sheet
Located under `#balance-sheet` section. Key rows:
- Share Capital, Reserves, Borrowings, Total Liabilities
- Fixed Assets, CWIP, Investments, Other Assets, Total Assets

### Cash Flow Statement
Located under `#cash-flow` section. Key rows:
- Cash from Operating Activity
- Cash from Investing Activity
- Cash from Financing Activity
- Net Cash Flow

### Key Ratios
Located under `#ratios` or in the overview section:
- ROCE %, ROE %, Debt to Equity
- Interest Coverage, Current Ratio
- Dividend Payout %

### Shareholding Pattern
Located under `#shareholding` section:
- Promoter holding % (with quarterly trend)
- FII holding %
- DII holding %
- Public holding %

## 3. Extraction Method

Use WebFetch to get the page HTML. The data is in standard HTML tables.
Look for `<section id="quarters">`, `<section id="profit-loss">`, etc.

Parse table rows to extract numerical data. Handle:
- Numbers with commas: `1,234` → `1234`
- Percentages: `45.2%` → `45.2`
- Negative values in parentheses: `(100)` → `-100`
- Cr (Crores) suffix: `1,500 Cr` → `1500`

## 4. Output Schema

### Quarterly Results JSON
```json
{
  "company": "Company Name",
  "ticker": "TICKER",
  "quarters": [
    {
      "quarter": "Dec 2024",
      "sales": 0.00,
      "expenses": 0.00,
      "operating_profit": 0.00,
      "opm_percent": 0.00,
      "net_profit": 0.00,
      "eps": 0.00
    }
  ],
  "revenue_growth_yoy": 0.00,
  "profit_growth_yoy": 0.00,
  "opm_trend": "Improving|Stable|Declining",
  "source": "screener.in",
  "scraped_at": "ISO-8601 timestamp"
}
```

### Financial Summary JSON
```json
{
  "company": "Company Name",
  "ticker": "TICKER",
  "annual_results": [],
  "balance_sheet": {
    "total_debt": 0.00,
    "total_equity": 0.00,
    "debt_to_equity": 0.00,
    "current_ratio": 0.00,
    "total_assets": 0.00
  },
  "cash_flow": {
    "operating_cash_flow": 0.00,
    "investing_cash_flow": 0.00,
    "financing_cash_flow": 0.00,
    "free_cash_flow": 0.00,
    "fcf_yield": 0.00
  },
  "ratios": {
    "roce": 0.00,
    "roe": 0.00,
    "interest_coverage": 0.00,
    "dividend_payout": 0.00
  },
  "growth_rates": {
    "revenue_cagr_3yr": 0.00,
    "revenue_cagr_5yr": 0.00,
    "profit_cagr_3yr": 0.00,
    "profit_cagr_5yr": 0.00
  },
  "source": "screener.in",
  "scraped_at": "ISO-8601 timestamp"
}
```

## 5. Validation
After extraction, validate with:
```bash
python scripts/validate_stock_data.py <output_json_file>
```
