# Bulk & Block Deals Analysis

## 1. Definitions

### Block Deals
- Minimum quantity: 5 lakh shares or Rs.10 crore value
- Executed in a separate trading window (8:45-9:00 AM)
- Both buyer and seller are known
- Single transaction between two parties

### Bulk Deals
- When any entity trades >0.5% of total shares in a day
- Can be multiple transactions through the day
- Reported end-of-day by exchanges
- Indicates significant position building/unwinding

### SAST Disclosures
- Required when entity crosses 5%, 10%, 15%, etc. thresholds
- Also required for any 2%+ change in holding
- Filed with stock exchanges and SEBI
- Most reliable source of large position changes

## 2. Data Sources

### WebSearch Queries
```
"{ticker}" bulk deal block deal NSE BSE 2024 2025
"{company_name}" bulk deal last 3 months
"{company_name}" SAST disclosure SEBI
"{ticker}" insider trading
```

### Exchange Data
- NSE: `https://www.nseindia.com/companies-listing/corporate-filings-bulk-deals`
- BSE: `https://www.bseindia.com/markets/equity/EQReports/BulkDeals.aspx`

## 3. Signal Interpretation

### Bulk/Block Buy Signals
```
Strongly Positive:
- Promoter/promoter group buying
- Marquee FII (BlackRock, Vanguard, GIC) buying
- Ace investor (Rakesh Jhunjhunwala legacy, Dolly Khanna, Vijay Kedia) buying
- PE/VC fund taking position (Warburg, Bain, KKR)

Moderately Positive:
- Top mutual fund buying
- Insurance company (LIC, HDFC Life) buying
- Domestic PE fund buying

Neutral to Slightly Positive:
- Unknown entity buying (could be operator-driven)
- Corporate body buying (check relationship)
```

### Bulk/Block Sell Signals
```
Strongly Negative:
- Promoter selling (especially if >1% of total holding)
- Multiple FIIs selling simultaneously
- PE/VC fund exiting (post lock-in)

Moderately Negative:
- Single large FII reducing position
- MF reducing across multiple schemes

Context Dependent:
- Pre-IPO investor exit (expected, may be absorbed)
- Promoter selling for diversification (if small %)
- Rebalancing by index funds
```

## 4. Insider Trading Signals

### What Insiders Know
Insiders (directors, KMPs, connected persons) have the best view of:
- Upcoming quarterly results
- Major contract wins/losses
- Regulatory approvals
- M&A plans

### SEBI Insider Trading Regulations
- Insiders must disclose trades within 2 trading days
- Trading window closes 7 days before results
- Contra-trade restriction: 6 months
- Violations are tracked and penalized

### Insider Buy/Sell Score
```
+3: Multiple insiders buying in open market
+2: CEO/CFO buying significant quantity
+1: Single director/KMP buying
 0: No insider activity
-1: Single director selling
-2: CEO/CFO selling significant quantity
-3: Multiple insiders selling simultaneously
```

## 5. Output Schema

```json
{
  "company": "Company Name",
  "ticker": "TICKER",
  "bulk_block_deals": [
    {
      "date": "YYYY-MM-DD",
      "type": "Bulk|Block",
      "entity": "Entity Name",
      "action": "Buy|Sell",
      "quantity": 0,
      "price": 0.00,
      "value_cr": 0.00,
      "entity_type": "Promoter|FII|DII|MF|HNI|Corporate",
      "signal": "Positive|Negative|Neutral"
    }
  ],
  "insider_trades": [
    {
      "date": "YYYY-MM-DD",
      "person": "Name",
      "designation": "MD|CFO|Director",
      "action": "Buy|Sell",
      "quantity": 0,
      "price": 0.00
    }
  ],
  "deal_flow_score": 0.00,
  "deal_flow_signal": "Strong Accumulation|Accumulation|Neutral|Distribution|Strong Distribution",
  "notable_investors": ["investor 1", "investor 2"],
  "analyzed_at": "ISO-8601 timestamp"
}
```
