"""
Validate stock data JSON files.

Usage: python scripts/validate_stock_data.py <json_file>

Detects file type from filename (_tickertape, _stocktwits, _sentiment, etc.)
and validates required fields and value ranges.

Exit code 0 = valid, 1 = invalid (errors printed to stderr).
"""

import json
import os
import sys


def validate_tickertape(data: dict) -> list[str]:
    """Validate Tickertape data JSON."""
    errors = []
    required = ["name", "ticker", "current_price"]
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "current_price" in data:
        price = data["current_price"]
        if not isinstance(price, (int, float)) or price <= 0:
            errors.append(f"Invalid current_price: {price} (must be positive number)")

    if "market_cap" in data:
        mc = data["market_cap"]
        if not isinstance(mc, (int, float)) or mc < 0:
            errors.append(f"Invalid market_cap: {mc} (must be non-negative)")

    if "pe_ratio" in data and data["pe_ratio"] is not None:
        pe = data["pe_ratio"]
        if isinstance(pe, (int, float)) and pe < 0:
            errors.append(f"Negative pe_ratio: {pe} (unusual, verify)")

    if "week_52_high" in data and "week_52_low" in data:
        high = data.get("week_52_high", 0)
        low = data.get("week_52_low", 0)
        if isinstance(high, (int, float)) and isinstance(low, (int, float)):
            if high < low:
                errors.append(f"52-week high ({high}) is less than low ({low})")

    if "dividend_yield" in data and data["dividend_yield"] is not None:
        dy = data["dividend_yield"]
        if isinstance(dy, (int, float)) and (dy < 0 or dy > 100):
            errors.append(f"Invalid dividend_yield: {dy} (expected 0-100)")

    return errors


def validate_stocktwits(data: dict) -> list[str]:
    """Validate StockTwits data JSON."""
    errors = []

    if "error" in data:
        # Error response is valid (documented unavailability)
        return errors

    if "bullish_percent" in data:
        bp = data["bullish_percent"]
        if isinstance(bp, (int, float)) and (bp < 0 or bp > 100):
            errors.append(f"Invalid bullish_percent: {bp} (expected 0-100)")

    if "bearish_percent" in data:
        bp = data["bearish_percent"]
        if isinstance(bp, (int, float)) and (bp < 0 or bp > 100):
            errors.append(f"Invalid bearish_percent: {bp} (expected 0-100)")

    return errors


def validate_sentiment(data: dict) -> list[str]:
    """Validate sentiment analysis JSON."""
    errors = []
    required = ["overall_sentiment", "confidence_score"]
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "overall_sentiment" in data:
        score = data["overall_sentiment"]
        if isinstance(score, (int, float)) and (score < -1.0 or score > 1.0):
            errors.append(f"Invalid overall_sentiment: {score} (expected -1.0 to +1.0)")

    if "confidence_score" in data:
        conf = data["confidence_score"]
        if isinstance(conf, (int, float)) and (conf < 0 or conf > 100):
            errors.append(f"Invalid confidence_score: {conf} (expected 0-100)")

    return errors


def validate_technical(data: dict) -> list[str]:
    """Validate technical analysis JSON."""
    errors = []
    required = ["current_price", "current_trend", "technical_signal"]
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "current_price" in data:
        price = data["current_price"]
        if not isinstance(price, (int, float)) or price <= 0:
            errors.append(f"Invalid current_price: {price} (must be positive)")

    if "current_trend" in data:
        valid_trends = ["Uptrend", "Downtrend", "Sideways"]
        if data["current_trend"] not in valid_trends:
            errors.append(f"Invalid current_trend: {data['current_trend']} (expected {valid_trends})")

    if "entry_strategy" in data:
        strategy = data["entry_strategy"]
        if "stop_loss" in strategy and "recommended_entry" in strategy:
            sl = strategy["stop_loss"]
            entry = strategy["recommended_entry"]
            if isinstance(sl, (int, float)) and isinstance(entry, (int, float)):
                if sl >= entry:
                    errors.append(f"Stop loss ({sl}) should be below entry ({entry})")

    return errors


def validate_recommendation(data: dict) -> list[str]:
    """Validate recommendation JSON."""
    errors = []
    required = ["recommendation", "conviction", "investment_thesis"]
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "recommendation" in data:
        valid = ["BUY", "SELL", "HOLD"]
        if data["recommendation"] not in valid:
            errors.append(f"Invalid recommendation: {data['recommendation']} (expected {valid})")

    if "conviction" in data:
        valid = ["HIGH", "MEDIUM", "LOW"]
        if data["conviction"] not in valid:
            errors.append(f"Invalid conviction: {data['conviction']} (expected {valid})")

    if "composite_score" in data:
        score = data["composite_score"]
        if isinstance(score, (int, float)) and (score < -1.0 or score > 1.0):
            errors.append(f"Invalid composite_score: {score} (expected -1.0 to +1.0)")

    return errors


def validate_financials(data: dict) -> list[str]:
    """Validate financial analysis JSON."""
    errors = []
    if "valuations" in data:
        vals = data["valuations"]
        bfv = vals.get("blended_fair_value")
        if bfv is not None and isinstance(bfv, (int, float)) and bfv <= 0:
            errors.append(f"Invalid blended_fair_value: {bfv} (must be positive)")
    if "financial_health_score" in data:
        score = data["financial_health_score"]
        if isinstance(score, (int, float)) and (score < 0 or score > 100):
            errors.append(f"Invalid financial_health_score: {score} (expected 0-100)")
    return errors


def validate_peers(data: dict) -> list[str]:
    """Validate peer comparison JSON."""
    errors = []
    if "percentile_ranks" in data:
        ranks = data["percentile_ranks"]
        for key in ("pe_percentile", "roe_percentile", "composite_score"):
            val = ranks.get(key)
            if val is not None and isinstance(val, (int, float)) and (val < 0 or val > 100):
                errors.append(f"Invalid {key}: {val} (expected 0-100)")
    return errors


def validate_news(data: dict) -> list[str]:
    """Validate news analysis JSON."""
    errors = []
    if "aggregate_news_score" in data:
        score = data["aggregate_news_score"]
        if isinstance(score, (int, float)) and (score < -10 or score > 10):
            errors.append(f"Unusual aggregate_news_score: {score}")
    return errors


def validate_risk(data: dict) -> list[str]:
    """Validate risk analysis JSON."""
    errors = []
    if "risk_rating" in data:
        valid = ["Low", "Moderate", "High", "Very High"]
        if data["risk_rating"] not in valid:
            errors.append(f"Invalid risk_rating: {data['risk_rating']} (expected {valid})")
    if "volatility" in data:
        vol = data["volatility"].get("estimated_annual")
        if vol is not None and isinstance(vol, (int, float)) and (vol < 0 or vol > 200):
            errors.append(f"Invalid volatility: {vol} (expected 0-200)")
    return errors


VALIDATORS = {
    "tickertape": validate_tickertape,
    "stocktwits": validate_stocktwits,
    "sentiment": validate_sentiment,
    "technical": validate_technical,
    "recommendation": validate_recommendation,
    "financials": validate_financials,
    "peers": validate_peers,
    "news": validate_news,
    "risk": validate_risk,
}


def detect_file_type(filepath: str) -> str | None:
    """Detect the data type from the filename."""
    basename = os.path.basename(filepath)
    for key in VALIDATORS:
        if f"_{key}" in basename:
            return key
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_stock_data.py <json_file>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        with open(filepath) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

    file_type = detect_file_type(filepath)
    if file_type is None:
        print(f"WARNING: Cannot detect file type from filename: {filepath}", file=sys.stderr)
        print("VALID (no specific validation rules for this file type)")
        sys.exit(0)

    validator = VALIDATORS[file_type]
    errors = validator(data)

    if errors:
        print(f"INVALID: {filepath} ({file_type})", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"VALID: {filepath} ({file_type})")
        sys.exit(0)


if __name__ == "__main__":
    main()
