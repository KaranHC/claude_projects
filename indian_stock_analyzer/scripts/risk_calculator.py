"""
Risk metrics and position sizing calculator.

Usage: python scripts/risk_calculator.py <tickertape_json> [recommendation_json]

Computes:
- Volatility and beta estimates
- Value at Risk (daily/monthly)
- Maximum drawdown estimate
- Position sizing (for Rs.10L portfolio)
- Risk-reward ratios
- Bull/base/bear scenarios

Outputs risk analysis JSON to stdout.
"""

import json
import math
import sys


# Sector beta benchmarks
SECTOR_BETA = {
    "Technology": 0.85, "IT Services": 0.85,
    "Banking": 1.15, "Financial Services": 1.1,
    "FMCG": 0.65, "Consumer Goods": 0.65,
    "Pharma": 0.75, "Healthcare": 0.75,
    "Automobile": 1.2, "Auto": 1.2,
    "Energy": 0.95, "Oil & Gas": 0.95,
    "Metals": 1.5, "Mining": 1.5,
    "Telecom": 0.95, "Real Estate": 1.6, "Realty": 1.6,
    "Cement": 1.1, "Power": 0.9, "Utilities": 0.9,
    "Infrastructure": 1.3, "Chemicals": 1.1,
}

PORTFOLIO_VALUE = 1_000_000  # Rs.10 lakhs default


def get_sector_beta(sector: str | None) -> float:
    if not sector:
        return 1.0
    for key, val in SECTOR_BETA.items():
        if key.lower() in sector.lower() or sector.lower() in key.lower():
            return val
    return 1.0


def estimate_volatility(price: float, high: float, low: float) -> dict:
    """Estimate annual volatility from 52-week range."""
    if high <= 0 or low <= 0:
        return {"annual": 30.0, "daily": 1.89, "category": "Moderate"}

    midpoint = (high + low) / 2
    range_pct = ((high - low) / midpoint) * 100

    # Range-based volatility estimate (Parkinson-inspired)
    annual_vol = round(range_pct * 0.6, 2)  # Empirical scaling

    if annual_vol < 20:
        category = "Low"
    elif annual_vol < 35:
        category = "Moderate"
    elif annual_vol < 50:
        category = "High"
    else:
        category = "Very High"

    daily_vol = round(annual_vol / math.sqrt(252), 2)

    return {"annual": annual_vol, "daily": daily_vol, "category": category}


def calculate_var(position_value: float, daily_vol_pct: float) -> dict:
    """Calculate Value at Risk."""
    daily_vol = daily_vol_pct / 100
    return {
        "daily_var_95": round(position_value * daily_vol * 1.645, 2),
        "daily_var_99": round(position_value * daily_vol * 2.326, 2),
        "monthly_var_95": round(position_value * daily_vol * 1.645 * math.sqrt(21), 2),
    }


def estimate_max_drawdown(vol_category: str, current_from_high_pct: float) -> dict:
    """Estimate max drawdown based on volatility category."""
    dd_ranges = {
        "Low": (15, 25),
        "Moderate": (25, 40),
        "High": (40, 60),
        "Very High": (50, 80),
    }
    low_dd, high_dd = dd_ranges.get(vol_category, (25, 40))
    estimated_max = round((low_dd + high_dd) / 2, 1)
    recovery_months = round(estimated_max / 2)

    return {
        "current_from_high_pct": round(current_from_high_pct, 2),
        "estimated_max_pct": estimated_max,
        "estimated_recovery_months": recovery_months,
    }


def calculate_position_size(
    entry: float, stop_loss: float, conviction: str = "MEDIUM"
) -> dict:
    """Calculate position sizes for different conviction levels."""
    if entry <= 0 or stop_loss <= 0 or stop_loss >= entry:
        return {
            "error": "Invalid entry/stop_loss",
            "high": {"shares": 0, "value": 0},
            "medium": {"shares": 0, "value": 0},
            "low": {"shares": 0, "value": 0},
        }

    risk_per_share = entry - stop_loss
    levels = {
        "high": 0.02,    # 2% portfolio risk
        "medium": 0.01,  # 1% portfolio risk
        "low": 0.005,    # 0.5% portfolio risk
    }

    result = {"portfolio_value": PORTFOLIO_VALUE}
    for level, risk_pct in levels.items():
        max_risk = PORTFOLIO_VALUE * risk_pct
        shares = int(max_risk / risk_per_share)
        value = round(shares * entry, 2)
        result[level] = {"shares": shares, "value": value, "pct_of_portfolio": round(value / PORTFOLIO_VALUE * 100, 1)}

    return result


def calculate_risk_reward(entry: float, stop_loss: float, targets: list[float]) -> dict:
    """Calculate risk-reward ratios for each target."""
    if entry <= 0 or stop_loss >= entry:
        return {"error": "Invalid entry/stop_loss"}

    risk = entry - stop_loss
    if risk <= 0:
        return {"error": "Stop loss must be below entry"}

    rr = {}
    for i, target in enumerate(targets, 1):
        reward = target - entry
        ratio = round(reward / risk, 2) if risk > 0 else 0
        rr[f"target_{i}"] = {
            "price": target,
            "reward": round(reward, 2),
            "rr_ratio": ratio,
            "acceptable": ratio >= 2.0,
        }

    # Weighted R:R (probability-weighted)
    probabilities = [0.70, 0.45, 0.25]
    weighted_reward = sum(
        p * (t - entry) for p, t in zip(probabilities[:len(targets)], targets)
    )
    weighted_rr = round(weighted_reward / risk, 2) if risk > 0 else 0
    rr["weighted_rr"] = weighted_rr
    rr["risk_per_share"] = round(risk, 2)

    return rr


def scenario_analysis(price: float, pe: float | None, sector: str | None) -> dict:
    """Build bull/base/bear scenario targets."""
    # Bull: +30% from current
    bull = round(price * 1.30, 2)
    # Base: +10%
    base = round(price * 1.10, 2)
    # Bear: -20%
    bear = round(price * 0.80, 2)

    expected = round(0.25 * bull + 0.50 * base + 0.25 * bear, 2)
    expected_return = round(((expected - price) / price) * 100, 2)

    return {
        "bull": {"price": bull, "probability": 0.25, "return_pct": 30.0},
        "base": {"price": base, "probability": 0.50, "return_pct": 10.0},
        "bear": {"price": bear, "probability": 0.25, "return_pct": -20.0},
        "expected_value": expected,
        "expected_return_pct": expected_return,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/risk_calculator.py <tickertape_json> [recommendation_json]", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Load recommendation if provided
    rec_data = {}
    if len(sys.argv) > 2:
        try:
            with open(sys.argv[2]) as f:
                rec_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    price = data.get("current_price", 0)
    high = data.get("week_52_high", price * 1.1)
    low = data.get("week_52_low", price * 0.9)
    sector = data.get("sector")
    pe = data.get("pe_ratio")

    if not price or price <= 0:
        print(json.dumps({"error": "Invalid or missing current_price"}))
        sys.exit(1)

    # Volatility
    vol = estimate_volatility(price, high, low)

    # Beta
    beta = get_sector_beta(sector)

    # VaR (for a 100-share position as example)
    position_value = price * 100
    var = calculate_var(position_value, vol["daily"])

    # Drawdown
    current_from_high = ((high - price) / high * 100) if high > 0 else 0
    drawdown = estimate_max_drawdown(vol["category"], current_from_high)

    # Position sizing
    entry = price
    stop_loss = price * 0.92  # Default 8% stop
    if rec_data:
        es = rec_data.get("entry_strategy", {})
        entry = es.get("recommended_entry", price)
        stop_loss = es.get("stop_loss", price * 0.92)

    position = calculate_position_size(entry, stop_loss)

    # Risk-reward
    targets = [price * 1.12, price * 1.25, price * 1.40]  # Default targets
    if rec_data and "profit_targets" in rec_data:
        rec_targets = [t["price"] for t in rec_data["profit_targets"] if "price" in t]
        if rec_targets:
            targets = rec_targets
    rr = calculate_risk_reward(entry, stop_loss, targets)

    # Scenarios
    scenarios = scenario_analysis(price, pe, sector)

    # Overall risk rating
    risk_score = 0
    if vol["category"] == "Very High":
        risk_score += 3
    elif vol["category"] == "High":
        risk_score += 2
    elif vol["category"] == "Moderate":
        risk_score += 1

    if beta > 1.3:
        risk_score += 2
    elif beta > 1.0:
        risk_score += 1

    if current_from_high > 30:
        risk_score += 1

    if risk_score >= 5:
        risk_rating = "Very High"
    elif risk_score >= 3:
        risk_rating = "High"
    elif risk_score >= 2:
        risk_rating = "Moderate"
    else:
        risk_rating = "Low"

    result = {
        "company": data.get("name", "Unknown"),
        "ticker": data.get("ticker", "Unknown"),
        "volatility": {**vol, "estimated_beta": beta},
        "value_at_risk": var,
        "drawdown": drawdown,
        "position_sizing": position,
        "risk_reward": rr,
        "scenarios": scenarios,
        "risk_rating": risk_rating,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
