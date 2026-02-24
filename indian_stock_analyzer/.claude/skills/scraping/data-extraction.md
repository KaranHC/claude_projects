# Data Extraction Patterns

## 1. Tickertape Extraction

### URL Resolution
- Base URL: `https://www.tickertape.in/stocks/{slug}`
- Use WebSearch with query: `site:tickertape.in {company_name} stock` to find the correct slug
- Example: "Tata Consultancy Services" → `tata-consultancy-services-TCS`

### HTML Data Extraction
Tickertape embeds stock data in a `__NEXT_DATA__` script tag within the HTML:

```
<script id="__NEXT_DATA__" type="application/json">{ ... }</script>
```

After fetching the page with WebFetch, look for this JSON blob. The relevant data is nested under:
- `props.pageProps.securityInfo` or `props.pageProps.security`

### Fields to Extract
```json
{
  "name": "Company Name",
  "ticker": "NSE_TICKER",
  "exchange": "NSE",
  "current_price": 0.00,
  "market_cap": 0,
  "pe_ratio": 0.00,
  "pb_ratio": 0.00,
  "dividend_yield": 0.00,
  "week_52_high": 0.00,
  "week_52_low": 0.00,
  "sector": "Technology",
  "industry": "IT Services",
  "day_change_percent": 0.00,
  "volume": 0,
  "avg_volume": 0,
  "eps": 0.00,
  "book_value": 0.00,
  "face_value": 0.00,
  "roe": 0.00,
  "roce": 0.00,
  "debt_to_equity": 0.00,
  "promoter_holding": 0.00,
  "source": "tickertape",
  "scraped_at": "ISO-8601 timestamp"
}
```

### Fallback Strategy
If `__NEXT_DATA__` is not available, extract visible text data from the page:
- Price from the main price display element
- Key ratios from the overview/fundamentals section
- Mark extracted fields with `"extraction_method": "text_fallback"`

## 2. StockTwits Extraction

### API Endpoint
```
https://api.stocktwits.com/api/2/streams/symbol/{TICKER}.json
```

Note: Indian stocks on StockTwits may use formats like `TCS.NS` or `TCS-IN`.
If direct ticker fails, try WebSearch: `site:stocktwits.com {company_name}`

### Response Structure
The API returns JSON with:
- `symbol` — Stock info (id, ticker, title)
- `messages` — Array of recent posts with sentiment
- Each message has: `body`, `created_at`, `entities.sentiment.basic` (Bullish/Bearish/null)

### Fields to Extract
```json
{
  "ticker": "TCS",
  "platform": "stocktwits",
  "total_messages": 0,
  "bullish_count": 0,
  "bearish_count": 0,
  "neutral_count": 0,
  "bullish_percent": 0.00,
  "bearish_percent": 0.00,
  "sentiment_ratio": 0.00,
  "watchlist_count": 0,
  "recent_messages": [
    {
      "body": "message text",
      "sentiment": "Bullish|Bearish|null",
      "created_at": "ISO-8601 timestamp"
    }
  ],
  "source": "stocktwits",
  "scraped_at": "ISO-8601 timestamp"
}
```

### Error Handling
- 404: Ticker not found on StockTwits — save empty result with `"error": "ticker_not_found"`
- 429: Rate limited — wait 10 seconds and retry once
- No sentiment data: Set all sentiment fields to null, note in `"warnings"` array

## 3. Validation
After extraction, run:
```bash
python scripts/validate_stock_data.py <output_json_file>
```
Exit code 0 = valid, 1 = invalid (check stderr for details).
