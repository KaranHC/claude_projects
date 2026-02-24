# Candlestick Patterns for Indian Markets

## 1. Bullish Reversal Candles

### Hammer
```
Appearance: Small body at top, long lower shadow (2x+ body)
Location: After downtrend / near support
Signal: Buyers rejected lower prices, recovery likely
Reliability: 60-65% (higher with volume confirmation)
Indian context: Very reliable at round number supports
```

### Morning Star (3-candle)
```
Day 1: Large red candle (downtrend continuation)
Day 2: Small body candle with gap down (indecision)
Day 3: Large green candle closing above Day 1 midpoint
Signal: Strong reversal from bottom
Reliability: 70-75%
```

### Bullish Engulfing
```
Appearance: Green candle completely engulfs previous red candle
Location: After downtrend
Signal: Buyer strength overwhelming sellers
Reliability: 65-70%
Indian context: Especially strong on ex-dividend day recoveries
```

### Piercing Pattern
```
Day 1: Large red candle
Day 2: Opens below Day 1 low, closes above Day 1 midpoint
Signal: Strong buying into weakness
Reliability: 60-65%
```

## 2. Bearish Reversal Candles

### Shooting Star
```
Appearance: Small body at bottom, long upper shadow (2x+ body)
Location: After uptrend / near resistance
Signal: Sellers rejected higher prices, decline likely
Reliability: 60-65%
Indian context: Common at 52-week highs before correction
```

### Evening Star (3-candle)
```
Day 1: Large green candle (uptrend continuation)
Day 2: Small body candle with gap up (indecision)
Day 3: Large red candle closing below Day 1 midpoint
Signal: Strong reversal from top
Reliability: 70-75%
```

### Bearish Engulfing
```
Appearance: Red candle completely engulfs previous green candle
Location: After uptrend
Signal: Seller strength overwhelming buyers
Reliability: 65-70%
Indian context: Very significant when accompanied by high delivery %
```

### Dark Cloud Cover
```
Day 1: Large green candle
Day 2: Opens above Day 1 high, closes below Day 1 midpoint
Signal: Strong selling into strength
Reliability: 60-65%
```

## 3. Continuation Candles

### Three White Soldiers (Bullish)
```
Three consecutive green candles with higher closes
Each opens within previous candle's body
Signal: Strong bullish continuation
Reliability: 70%
Caution: If candles are very long, may signal exhaustion
```

### Three Black Crows (Bearish)
```
Three consecutive red candles with lower closes
Each opens within previous candle's body
Signal: Strong bearish continuation
Reliability: 70%
```

### Doji (Indecision)
```
Types:
- Standard Doji: Open ≈ Close, small body
- Long-legged Doji: Long shadows both sides
- Dragonfly Doji: Long lower shadow (bullish at bottom)
- Gravestone Doji: Long upper shadow (bearish at top)

Signal: Trend pause, reversal possible
Action: Wait for next candle confirmation
```

## 4. Detection from Day Change Data

### When Only Day Change % is Available
```
Strong bullish candle signal: day_change > +3%
Moderate bullish: +1% to +3%
Doji/indecision: -0.5% to +0.5%
Moderate bearish: -1% to -3%
Strong bearish candle signal: day_change < -3%
```

### Volume Context Enhances Signal
```
Bullish candle + High volume (>1.5x avg) = Strong buy signal
Bullish candle + Low volume (<0.7x avg) = Weak, may not sustain
Bearish candle + High volume = Strong sell signal
Bearish candle + Low volume = Weak selling, may bounce
```

## 5. Indian Market Candlestick Context

### Market Hours Impact
- 9:15-9:30 AM: Opening candle — often misleading (gap fills)
- 9:30-11:00 AM: Morning trend establishment
- 11:00-1:00 PM: Consolidation typically
- 1:00-2:30 PM: Afternoon trend (FII activity)
- 2:30-3:30 PM: Closing candle — most reliable for next day

### Expiry Day Patterns (Last Thursday)
- High volatility, large candles common
- Patterns less reliable for medium-term analysis
- Pin bars at round numbers = option writers defending positions

### Result Day Patterns
- Gap up/down on results: follow-through in 70% of cases if gap is >5%
- Small gap (<3%): often fills within session
- Volume on result day: 3-5x normal is standard

### Sector Rotation Candles
- If banking candles turn bullish while IT turns bearish: sector rotation
- Follow the money — sector that FIIs are buying shows strongest candles

## 6. Pattern Scoring

### Composite Candle Score (-10 to +10)
```
Base score from day change:
  >+5%: +4,  +3-5%: +3,  +1-3%: +2,  0-1%: +1
  -1-0%: -1,  -3 to -1%: -2,  -5 to -3%: -3,  <-5%: -4

Volume modifier:
  >2x avg: ±2,  1.5-2x: ±1,  1-1.5x: 0,  <1x: ∓1

Position modifier:
  Near support + bullish: +2
  Near resistance + bearish: +2
  Near support + bearish: -2 (breakdown risk)
  Near resistance + bullish: +2 (breakout potential)
```

### Interpretation
- +7 to +10: Very strong bullish candle signal
- +4 to +6: Bullish candle signal
- +1 to +3: Mildly bullish
- -3 to +0: Neutral to mildly bearish
- -6 to -4: Bearish candle signal
- -10 to -7: Very strong bearish candle signal
