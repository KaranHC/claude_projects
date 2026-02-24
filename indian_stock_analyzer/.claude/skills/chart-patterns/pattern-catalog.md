# Chart Pattern Catalog

## 1. Reversal Patterns

### Head and Shoulders (Top) — Bearish Reversal
```
Identification from available data:
- Price near 52W high after sustained uptrend
- Recent failed attempt to break above 52W high
- Volume declining on recent rallies

Probability: 65-70% success rate
Target: Measured move = Distance from head to neckline, projected downward
```

### Inverse Head and Shoulders (Bottom) — Bullish Reversal
```
Identification:
- Price near 52W low after sustained downtrend
- Recent bounce from 52W low area with higher volume
- Price showing higher lows in recent sessions

Probability: 65-70% success rate
Target: Measured move = Distance from head to neckline, projected upward
```

### Double Top — Bearish Reversal
```
Identification:
- Two attempts to break above 52W high or resistance
- Price currently pulling back from second test
- Lower volume on second attempt

Probability: 60-65% success rate
Target: Distance between top and support, projected downward
```

### Double Bottom — Bullish Reversal
```
Identification:
- Two bounces from 52W low or support area
- Price currently recovering from second test
- Higher volume on second bounce

Probability: 60-65% success rate
Target: Distance between bottom and resistance, projected upward
```

### Rounding Bottom (Cup) — Bullish Reversal
```
Identification:
- Price was near 52W low 3-6 months ago
- Gradual recovery with improving fundamentals
- Currently approaching or exceeding midpoint of 52W range
- Volume U-shaped (high at start, low at bottom, rising now)

Probability: 65-70% (one of the most reliable patterns)
Target: Depth of cup, projected above breakout
```

## 2. Continuation Patterns

### Bull Flag
```
Identification:
- Strong prior uptrend (price well above 52W low)
- Recent small pullback (5-10%) on declining volume
- Price holding above key support levels
- Consolidating in narrow range

Probability: 65-70% continuation
Target: Height of flagpole, projected from breakout
```

### Bear Flag
```
Identification:
- Prior downtrend (price well below 52W high)
- Recent small bounce (5-10%) on declining volume
- Failing to break above resistance
- Lower highs pattern

Probability: 65-70% continuation
Target: Height of flagpole, projected downward
```

### Ascending Triangle — Usually Bullish
```
Identification:
- Repeated tests of same resistance level (52W high area)
- Higher lows being made (rising support)
- Volume contracting toward apex
- Typically resolves upward (70% of the time)

Target: Height of triangle projected above breakout
```

### Descending Triangle — Usually Bearish
```
Identification:
- Repeated tests of same support level (52W low area)
- Lower highs being made (falling resistance)
- Volume contracting
- Typically resolves downward (70% of the time)

Target: Height of triangle projected below breakdown
```

## 3. Pattern Detection from Limited Data

### Available Data Points
From Tickertape data, we have:
- Current price
- 52-week high and low
- Day change %
- Volume vs average volume
- Price position in 52W range

### Detection Algorithm

```python
def detect_pattern(price, high_52w, low_52w, day_change, volume_ratio):
    position = (price - low_52w) / (high_52w - low_52w)
    range_pct = (high_52w - low_52w) / low_52w * 100

    patterns = []

    # Near 52W high patterns
    if position > 0.90:
        if volume_ratio < 0.8:
            patterns.append({
                "pattern": "Potential Double Top",
                "bias": "Bearish",
                "confidence": "Medium",
                "note": "Near 52W high with declining volume"
            })
        elif volume_ratio > 1.5:
            patterns.append({
                "pattern": "Breakout Attempt",
                "bias": "Bullish",
                "confidence": "Medium-High",
                "note": "Testing 52W high with strong volume"
            })

    # Near 52W low patterns
    elif position < 0.10:
        if volume_ratio > 1.5 and day_change > 0:
            patterns.append({
                "pattern": "Potential Double Bottom",
                "bias": "Bullish",
                "confidence": "Medium",
                "note": "Bouncing from 52W low with volume"
            })
        elif volume_ratio < 0.5:
            patterns.append({
                "pattern": "Falling Knife",
                "bias": "Bearish",
                "confidence": "Medium",
                "note": "Near 52W low, no buying interest"
            })

    # Middle range patterns
    elif 0.40 < position < 0.60:
        if range_pct > 50:
            patterns.append({
                "pattern": "Wide Range Consolidation",
                "bias": "Neutral",
                "confidence": "Low",
                "note": "High volatility, middle of range"
            })

    # Uptrend patterns (above midpoint)
    elif position > 0.60:
        if day_change < -2:
            patterns.append({
                "pattern": "Bull Flag Pullback",
                "bias": "Bullish",
                "confidence": "Medium",
                "note": "Pullback within uptrend"
            })
        elif volume_ratio > 1.3:
            patterns.append({
                "pattern": "Uptrend Continuation",
                "bias": "Bullish",
                "confidence": "Medium",
                "note": "Strong volume in upper range"
            })

    # Downtrend patterns (below midpoint)
    elif position < 0.40:
        if day_change > 2:
            patterns.append({
                "pattern": "Bear Market Rally",
                "bias": "Neutral-Bearish",
                "confidence": "Medium",
                "note": "Bounce in downtrend - verify sustainability"
            })
        elif 0.20 < position < 0.40:
            patterns.append({
                "pattern": "Potential Accumulation",
                "bias": "Neutral-Bullish",
                "confidence": "Low-Medium",
                "note": "Below midpoint but above extreme low"
            })

    return patterns
```

## 4. Indian Market-Specific Patterns

### Nifty Correlation Patterns
- When Nifty is at ATH: most stocks participate, breakouts more reliable
- When Nifty is falling: individual stock patterns less reliable
- Expiry week (last Thursday): increased volatility, patterns less reliable
- Budget/RBI policy days: all patterns invalidated by event risk

### Round Number Support/Resistance
In Indian markets, significant support/resistance at:
- Multiples of Rs.100 for stocks Rs.100-1000
- Multiples of Rs.500 for stocks Rs.1000-5000
- Multiples of Rs.1000 for stocks above Rs.5000
- Rs.10,000 and Rs.20,000 are major psychological levels

### FII-Driven Patterns
- Morning gap-ups with FII buying: trend continuation likely
- Afternoon selloffs: potential FII rebalancing, may reverse
- Consistent buying on dips: strong pattern, follow the flow

## 5. Output Schema

```json
{
  "company": "Company Name",
  "ticker": "TICKER",
  "current_price": 0.00,
  "detected_patterns": [
    {
      "pattern": "Pattern Name",
      "type": "Reversal|Continuation",
      "bias": "Bullish|Bearish|Neutral",
      "confidence": "High|Medium|Low",
      "implied_target": 0.00,
      "implied_stop": 0.00,
      "description": "string"
    }
  ],
  "round_number_levels": {
    "nearest_support": 0.00,
    "nearest_resistance": 0.00
  },
  "volume_pattern": "Accumulation|Distribution|Neutral",
  "overall_technical_bias": "Bullish|Bearish|Neutral",
  "pattern_reliability_note": "string",
  "analyzed_at": "ISO-8601 timestamp"
}
```
