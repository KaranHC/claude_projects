# Analysis Frameworks

## 1. Technical Indicators

### RSI (Relative Strength Index) — 14-period
- **Overbought**: RSI > 70 → potential sell signal
- **Oversold**: RSI < 30 → potential buy signal
- **Neutral zone**: 30-70
- Calculation: RSI = 100 - (100 / (1 + RS)), where RS = Avg Gain / Avg Loss over 14 periods

### MACD (Moving Average Convergence Divergence) — (12, 26, 9)
- MACD Line = 12-period EMA - 26-period EMA
- Signal Line = 9-period EMA of MACD Line
- **Bullish crossover**: MACD crosses above signal → buy signal
- **Bearish crossover**: MACD crosses below signal → sell signal
- Histogram = MACD - Signal (positive = bullish momentum)

### Moving Averages
- **SMA 20**: Short-term trend (trading)
- **SMA 50**: Medium-term trend (swing)
- **SMA 200**: Long-term trend (investing)
- **EMA 20/50**: More responsive to recent prices
- **Golden Cross**: 50-day SMA crosses above 200-day SMA → strong bullish
- **Death Cross**: 50-day SMA crosses below 200-day SMA → strong bearish

### Bollinger Bands (20-period, 2 std dev)
- Upper Band = SMA(20) + 2 * StdDev(20)
- Lower Band = SMA(20) - 2 * StdDev(20)
- Price near upper band → overbought
- Price near lower band → oversold
- Band squeeze → volatility breakout expected

### 52-Week Range Position
- Position = (Current Price - 52W Low) / (52W High - 52W Low) * 100
- **0-20%**: Near yearly low — potential value or falling knife
- **20-40%**: Below midpoint — possible accumulation zone
- **40-60%**: Midrange — neutral
- **60-80%**: Above midpoint — uptrend
- **80-100%**: Near yearly high — momentum or overextended

## 2. Fundamental Benchmarks (Indian Market)

### PE Ratio
- **Nifty 50 average**: ~22x
- **Below 15x**: Potentially undervalued (check for value traps)
- **15-25x**: Fair value range for large caps
- **25-40x**: Growth premium — justify with earnings growth
- **Above 40x**: Expensive — needs strong growth thesis
- Sector-specific: IT (25-35x), Banking (12-18x), FMCG (40-60x), Pharma (20-30x)

### PB Ratio (Price-to-Book)
- **Below 1.0**: Trading below book value (banks often do during stress)
- **1.0-3.0**: Reasonable for most sectors
- **Above 3.0**: High premium — asset-light or high-growth businesses

### Debt-to-Equity Ratio
- **Below 0.5**: Conservative/healthy balance sheet
- **0.5-1.0**: Moderate leverage
- **1.0-2.0**: High leverage — acceptable for capital-intensive sectors
- **Above 2.0**: Risky — needs strong cash flows

### ROE (Return on Equity)
- **Above 20%**: Excellent
- **15-20%**: Good
- **10-15%**: Average
- **Below 10%**: Below average — needs justification

### Promoter Holding
- **Above 60%**: Strong promoter confidence
- **40-60%**: Moderate
- **Below 40%**: Low — check for institutional support

## 3. Sentiment Scoring

### Weighted Model
- **Social media sentiment (StockTwits)**: 40% weight
- **News sentiment (from Tickertape data)**: 30% weight
- **Analyst consensus**: 30% weight

### Score Scale: -1.0 to +1.0
- **+0.6 to +1.0**: Strongly bullish
- **+0.2 to +0.6**: Moderately bullish
- **-0.2 to +0.2**: Neutral
- **-0.6 to -0.2**: Moderately bearish
- **-1.0 to -0.6**: Strongly bearish

### Confidence Score: 0 to 100
Based on:
- Data availability (all sources present = higher confidence)
- Sample size (more messages/signals = higher confidence)
- Signal agreement (consistent signals = higher confidence)

## 4. Recommendation Criteria

### Signal Weighting
- Technical signals: 40%
- Sentiment signals: 30%
- Fundamental signals: 30%

### Final Score → Action
- **Above +0.4**: BUY
- **-0.2 to +0.4**: HOLD
- **Below -0.2**: SELL

### Conviction Levels
- **HIGH**: All three signal categories agree + strong individual signals
- **MEDIUM**: Two categories agree or mixed but leaning one direction
- **LOW**: Signals are conflicting or data is incomplete

### Entry/Exit Strategy
- **Entry price**: Current price adjusted for support levels
- **Stop loss**: Below nearest support or -8% to -10% from entry
- **Target 1 (Short-term)**: Nearest resistance level or +10-15%
- **Target 2 (Medium-term)**: Next resistance or +20-30%
- **Target 3 (Long-term)**: Fair value estimate or +40-50%
