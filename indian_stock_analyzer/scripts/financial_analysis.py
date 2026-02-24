"""
Financial analysis and intrinsic valuation calculator.

Usage: python scripts/financial_analysis.py <tickertape_json>

Computes:
- Graham Number
- PE-based fair value
- PEG assessment
- Simplified DCF fair value
- Financial health score
- Blended intrinsic value estimate

Outputs computed financial analysis JSON to stdout.
"""

import json
import math
import sys


# Sector fair PE multiples (Indian market)
SECTOR_FAIR_PE = {
    "Technology": 28, "IT Services": 28, "Information Technology": 28,
    "Banking": 15, "Financial Services": 18,
    "FMCG": 45, "Consumer Goods": 42,
    "Pharma": 25, "Healthcare": 25, "Pharmaceutical": 25,
    "Automobile": 22, "Auto": 22,
    "Energy": 12, "Oil & Gas": 12,
    "Metals": 10, "Mining": 10,
    "Telecom": 20, "Telecommunications": 20,
    "Real Estate": 22, "Realty": 22,
    "Cement": 20, "Chemicals": 25,
    "Power": 15, "Utilities": 15, "Infrastructure": 18,
}

DEFAULT_PE = 22  # Nifty 50 average


def get_sector_pe(sector: str | None) -> float:
    if not sector:
        return DEFAULT_PE
    for key, val in SECTOR_FAIR_PE.items():
        if key.lower() in sector.lower() or sector.lower() in key.lower():
            return val
    return DEFAULT_PE


def graham_number(eps: float | None, book_value: float | None) -> float | None:
    """Calculate Benjamin Graham's intrinsic value formula."""
    if not eps or not book_value or eps <= 0 or book_value <= 0:
        return None
    return round(math.sqrt(22.5 * eps * book_value), 2)


def pe_fair_value(eps: float | None, sector: str | None) -> dict:
    """Calculate PE-based fair value using sector-appropriate multiple."""
    if not eps or eps <= 0:
        return {"fair_value": None, "fair_pe": None, "note": "EPS not positive"}
    fair_pe = get_sector_pe(sector)
    return {
        "fair_value": round(eps * fair_pe, 2),
        "fair_pe": fair_pe,
    }


def peg_assessment(pe: float | None, growth_rate: float | None) -> dict:
    """Assess PEG ratio (PE divided by earnings growth rate)."""
    if not pe or not growth_rate or pe <= 0 or growth_rate <= 0:
        return {"peg": None, "assessment": "N/A", "note": "Insufficient data"}
    peg = round(pe / growth_rate, 2)
    if peg < 0.5:
        assessment = "Significantly Undervalued"
    elif peg < 1.0:
        assessment = "Undervalued"
    elif peg < 1.5:
        assessment = "Fairly Valued"
    elif peg < 2.0:
        assessment = "Moderately Overvalued"
    else:
        assessment = "Overvalued"
    return {"peg": peg, "assessment": assessment}


def simplified_dcf(
    eps: float | None, growth_rate: float | None, pe: float | None
) -> float | None:
    """Simplified DCF: project 5 years of earnings growth, discount back."""
    if not eps or not growth_rate or eps <= 0:
        return None
    # Project earnings 5 years forward
    future_eps = eps * ((1 + growth_rate / 100) ** 5)
    # Apply a terminal multiple (sector PE or current PE, whichever is lower)
    terminal_pe = min(pe or 20, get_sector_pe(None), 30)
    future_price = future_eps * terminal_pe
    # Discount back at 12% (Indian cost of equity)
    discount_rate = 0.12
    present_value = future_price / ((1 + discount_rate) ** 5)
    return round(present_value, 2)


def financial_health_score(data: dict) -> dict:
    """Score financial health 0-100 from available metrics."""
    score = 50  # Start at neutral
    observations = []

    # ROE assessment
    roe = data.get("roe")
    if roe is not None:
        if roe > 20:
            score += 12
            observations.append(f"Excellent ROE of {roe}%")
        elif roe > 15:
            score += 8
            observations.append(f"Good ROE of {roe}%")
        elif roe > 10:
            score += 3
        elif roe > 0:
            score -= 5
            observations.append(f"Below-average ROE of {roe}%")
        else:
            score -= 15
            observations.append(f"Negative ROE of {roe}%")

    # ROCE assessment
    roce = data.get("roce")
    if roce is not None:
        if roce > 20:
            score += 10
        elif roce > 15:
            score += 5
        elif roce < 10:
            score -= 5

    # Debt assessment
    de = data.get("debt_to_equity")
    if de is not None:
        if de < 0.1:
            score += 10
            observations.append("Virtually debt-free")
        elif de < 0.5:
            score += 5
            observations.append("Conservative debt levels")
        elif de > 1.5:
            score -= 10
            observations.append(f"High debt-to-equity of {de}")
        elif de > 1.0:
            score -= 5

    # Promoter holding
    promoter = data.get("promoter_holding")
    if promoter is not None:
        if promoter > 60:
            score += 5
        elif promoter < 35:
            score -= 5
            observations.append(f"Low promoter holding of {promoter}%")

    # Dividend yield (bonus for payers)
    div_yield = data.get("dividend_yield")
    if div_yield is not None and div_yield > 1.0:
        score += 3
        observations.append(f"Dividend yield of {div_yield}%")

    return {
        "score": max(0, min(100, score)),
        "observations": observations,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/financial_analysis.py <tickertape_json>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    price = data.get("current_price", 0)
    eps = data.get("eps")
    book_value = data.get("book_value")
    pe = data.get("pe_ratio")
    sector = data.get("sector")
    roe = data.get("roe")

    # Estimate growth rate from available data
    # If no explicit growth rate, estimate from ROE and payout
    growth_rate = data.get("earnings_growth")
    if growth_rate is None and roe and roe > 0:
        # Sustainable growth = ROE * retention ratio (assume 70% retention)
        growth_rate = round(roe * 0.7, 2)

    # Calculate valuations
    graham = graham_number(eps, book_value)
    pe_val = pe_fair_value(eps, sector)
    peg = peg_assessment(pe, growth_rate)
    dcf = simplified_dcf(eps, growth_rate, pe)

    # Blend fair values (weight available methods)
    fair_values = []
    weights = []
    if pe_val.get("fair_value"):
        fair_values.append(pe_val["fair_value"])
        weights.append(0.35)
    if graham:
        fair_values.append(graham)
        weights.append(0.25)
    if dcf:
        fair_values.append(dcf)
        weights.append(0.40)

    blended = None
    if fair_values and weights:
        total_weight = sum(weights[:len(fair_values)])
        blended = round(
            sum(v * w for v, w in zip(fair_values, weights)) / total_weight, 2
        )

    # Health score
    health = financial_health_score(data)

    upside = None
    if blended and price and price > 0:
        upside = round(((blended - price) / price) * 100, 2)

    result = {
        "company": data.get("name", "Unknown"),
        "ticker": data.get("ticker", "Unknown"),
        "current_price": price,
        "valuations": {
            "graham_number": graham,
            "pe_fair_value": pe_val.get("fair_value"),
            "pe_fair_multiple": pe_val.get("fair_pe"),
            "peg_ratio": peg.get("peg"),
            "peg_assessment": peg.get("assessment"),
            "dcf_fair_value": dcf,
            "blended_fair_value": blended,
            "upside_to_fair_value_pct": upside,
        },
        "financial_health_score": health["score"],
        "key_observations": health["observations"],
        "growth_rate_used": growth_rate,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
