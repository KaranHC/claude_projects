"""
Calculate technical metrics from Tickertape data.

Usage: python scripts/calculate_metrics.py <tickertape_json>

Computes:
- Price position in 52-week range
- Estimated support and resistance levels
- PE valuation relative to sector averages
- Momentum indicators

Outputs computed metrics JSON to stdout.
"""

import json
import math
import sys

# Sector average PE ratios for Indian market (approximate)
SECTOR_PE_AVERAGES = {
    "Technology": 30,
    "IT Services": 28,
    "Information Technology": 28,
    "Banking": 15,
    "Financial Services": 18,
    "FMCG": 50,
    "Consumer Goods": 45,
    "Pharma": 25,
    "Healthcare": 25,
    "Pharmaceutical": 25,
    "Automobile": 22,
    "Auto": 22,
    "Energy": 12,
    "Oil & Gas": 12,
    "Metals": 10,
    "Mining": 10,
    "Telecom": 20,
    "Telecommunications": 20,
    "Real Estate": 25,
    "Realty": 25,
    "Infrastructure": 18,
    "Cement": 20,
    "Chemicals": 25,
    "Power": 15,
    "Utilities": 15,
}

# Default PE for Nifty 50
DEFAULT_MARKET_PE = 22


def calculate_52w_position(price: float, high: float, low: float) -> float:
    """Calculate price position in 52-week range (0-100)."""
    if high == low:
        return 50.0
    return round(((price - low) / (high - low)) * 100, 2)


def estimate_support_resistance(price: float, high: float, low: float) -> dict:
    """Estimate support and resistance levels."""
    range_size = high - low

    # Support levels: below current price
    support_1 = round(price - (range_size * 0.10), 2)
    support_2 = round(price - (range_size * 0.20), 2)

    # Resistance levels: above current price
    resistance_1 = round(price + (range_size * 0.10), 2)
    resistance_2 = round(price + (range_size * 0.20), 2)

    # Round number support/resistance (nearest 50 or 100)
    round_below = math.floor(price / 100) * 100
    round_above = math.ceil(price / 100) * 100

    return {
        "support_1": max(support_1, low),
        "support_2": max(support_2, low * 0.95),
        "resistance_1": min(resistance_1, high),
        "resistance_2": min(resistance_2, high * 1.05),
        "round_support": round_below if round_below < price else round_below - 100,
        "round_resistance": round_above if round_above > price else round_above + 100,
    }


def evaluate_pe_valuation(pe_ratio: float | None, sector: str | None) -> dict:
    """Evaluate PE ratio relative to sector and market averages."""
    if pe_ratio is None or pe_ratio <= 0:
        return {
            "pe_ratio": pe_ratio,
            "sector_average_pe": None,
            "valuation": "N/A",
            "pe_premium_discount": None,
            "note": "PE not applicable (negative earnings or unavailable)",
        }

    sector_pe = DEFAULT_MARKET_PE
    if sector:
        for key, value in SECTOR_PE_AVERAGES.items():
            if key.lower() in sector.lower() or sector.lower() in key.lower():
                sector_pe = value
                break

    premium_discount = round(((pe_ratio - sector_pe) / sector_pe) * 100, 2)

    if pe_ratio < sector_pe * 0.7:
        valuation = "Significantly Undervalued"
    elif pe_ratio < sector_pe * 0.9:
        valuation = "Undervalued"
    elif pe_ratio <= sector_pe * 1.1:
        valuation = "Fairly Valued"
    elif pe_ratio <= sector_pe * 1.3:
        valuation = "Overvalued"
    else:
        valuation = "Significantly Overvalued"

    return {
        "pe_ratio": pe_ratio,
        "sector_average_pe": sector_pe,
        "valuation": valuation,
        "pe_premium_discount": premium_discount,
    }


def assess_momentum(price: float, high: float, low: float, day_change: float | None) -> dict:
    """Assess price momentum from available data."""
    position = calculate_52w_position(price, high, low)

    if position > 80:
        trend = "Strong Uptrend"
        strength = "Strong"
    elif position > 60:
        trend = "Uptrend"
        strength = "Moderate"
    elif position > 40:
        trend = "Sideways"
        strength = "Weak"
    elif position > 20:
        trend = "Downtrend"
        strength = "Moderate"
    else:
        trend = "Strong Downtrend"
        strength = "Strong"

    # Adjust with day change if available
    day_signal = "Neutral"
    if day_change is not None:
        if day_change > 2:
            day_signal = "Strongly Positive"
        elif day_change > 0.5:
            day_signal = "Positive"
        elif day_change < -2:
            day_signal = "Strongly Negative"
        elif day_change < -0.5:
            day_signal = "Negative"

    return {
        "estimated_trend": trend,
        "trend_strength": strength,
        "day_signal": day_signal,
        "week_52_position": position,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/calculate_metrics.py <tickertape_json>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        with open(filepath) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    price = data.get("current_price", 0)
    high = data.get("week_52_high", price * 1.1)
    low = data.get("week_52_low", price * 0.9)
    pe = data.get("pe_ratio")
    sector = data.get("sector")
    day_change = data.get("day_change_percent")

    if not price or price <= 0:
        print(json.dumps({"error": "Invalid or missing current_price"}))
        sys.exit(1)

    metrics = {
        "company": data.get("name", "Unknown"),
        "ticker": data.get("ticker", "Unknown"),
        "current_price": price,
        "week_52_position": calculate_52w_position(price, high, low),
        "support_resistance": estimate_support_resistance(price, high, low),
        "pe_valuation": evaluate_pe_valuation(pe, sector),
        "momentum": assess_momentum(price, high, low, day_change),
    }

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
