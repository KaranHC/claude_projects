"""
Peer comparison analysis calculator.

Usage: python scripts/peer_comparison.py <tickertape_json> [peers_json]

Computes:
- Percentile ranking among peers for key metrics
- Sector averages
- Composite peer score
- Relative valuation premium/discount

If peers_json is not provided, uses sector benchmark defaults.
Outputs peer analysis JSON to stdout.
"""

import json
import sys


# Default sector peer benchmarks (medians)
SECTOR_BENCHMARKS = {
    "Technology": {"pe": 28, "pb": 8, "roe": 25, "opm": 25, "growth": 12},
    "IT Services": {"pe": 28, "pb": 8, "roe": 25, "opm": 25, "growth": 12},
    "Banking": {"pe": 15, "pb": 2.5, "roe": 14, "opm": None, "growth": 15},
    "Financial Services": {"pe": 18, "pb": 3, "roe": 15, "opm": None, "growth": 18},
    "FMCG": {"pe": 50, "pb": 15, "roe": 30, "opm": 22, "growth": 10},
    "Consumer Goods": {"pe": 45, "pb": 12, "roe": 28, "opm": 20, "growth": 10},
    "Pharma": {"pe": 25, "pb": 4, "roe": 15, "opm": 20, "growth": 12},
    "Healthcare": {"pe": 25, "pb": 4, "roe": 15, "opm": 20, "growth": 12},
    "Automobile": {"pe": 22, "pb": 4, "roe": 15, "opm": 12, "growth": 12},
    "Auto": {"pe": 22, "pb": 4, "roe": 15, "opm": 12, "growth": 12},
    "Energy": {"pe": 12, "pb": 1.5, "roe": 12, "opm": 15, "growth": 5},
    "Oil & Gas": {"pe": 12, "pb": 1.5, "roe": 12, "opm": 15, "growth": 5},
    "Metals": {"pe": 10, "pb": 1.5, "roe": 12, "opm": 18, "growth": 8},
    "Telecom": {"pe": 20, "pb": 3, "roe": 10, "opm": 35, "growth": 10},
    "Real Estate": {"pe": 22, "pb": 2.5, "roe": 10, "opm": 25, "growth": 15},
    "Cement": {"pe": 20, "pb": 3, "roe": 12, "opm": 18, "growth": 10},
    "Power": {"pe": 15, "pb": 2, "roe": 10, "opm": 25, "growth": 8},
}

DEFAULT_BENCHMARK = {"pe": 22, "pb": 3, "roe": 15, "opm": 18, "growth": 12}


def get_benchmark(sector: str | None) -> dict:
    if not sector:
        return DEFAULT_BENCHMARK
    for key, val in SECTOR_BENCHMARKS.items():
        if key.lower() in sector.lower() or sector.lower() in key.lower():
            return val
    return DEFAULT_BENCHMARK


def percentile_rank(value: float, benchmark: float, higher_is_better: bool = True) -> int:
    """Estimate percentile rank relative to a benchmark median (50th percentile)."""
    if benchmark == 0:
        return 50
    ratio = value / benchmark
    if higher_is_better:
        # Higher than benchmark = above 50th percentile
        percentile = min(95, max(5, int(50 * (1 + (ratio - 1) * 1.5))))
    else:
        # Lower than benchmark = above 50th percentile (e.g., PE — lower is cheaper)
        percentile = min(95, max(5, int(50 * (1 + (1 - ratio) * 1.5))))
    return percentile


def quality_adjustment_factor(company: dict, benchmark: dict) -> float:
    """Calculate quality adjustment factor for relative valuation (0.7 to 1.5)."""
    factor = 1.0

    # ROE comparison
    company_roe = company.get("roe") or 0
    bench_roe = benchmark.get("roe") or 15
    if company_roe > bench_roe * 1.2:
        factor += 0.1
    elif company_roe < bench_roe * 0.8:
        factor -= 0.1

    # Growth comparison
    company_growth = company.get("earnings_growth") or company.get("revenue_growth") or 0
    bench_growth = benchmark.get("growth") or 12
    if company_growth > bench_growth * 1.3:
        factor += 0.15
    elif company_growth < bench_growth * 0.7:
        factor -= 0.1

    # Debt comparison
    de = company.get("debt_to_equity")
    if de is not None:
        if de < 0.3:
            factor += 0.1
        elif de > 1.0:
            factor -= 0.1

    # Promoter holding
    promoter = company.get("promoter_holding")
    if promoter is not None:
        if promoter > 60:
            factor += 0.05
        elif promoter < 35:
            factor -= 0.05

    return round(max(0.7, min(1.5, factor)), 2)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/peer_comparison.py <tickertape_json>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    sector = data.get("sector")
    benchmark = get_benchmark(sector)

    # Calculate percentile ranks
    pe = data.get("pe_ratio")
    roe = data.get("roe")
    opm = data.get("operating_margin")
    de = data.get("debt_to_equity")

    pe_pctile = percentile_rank(pe, benchmark["pe"], higher_is_better=False) if pe else 50
    roe_pctile = percentile_rank(roe, benchmark["roe"], higher_is_better=True) if roe else 50

    # Composite score
    scores = [pe_pctile, roe_pctile]
    if opm and benchmark.get("opm"):
        opm_pctile = percentile_rank(opm, benchmark["opm"], higher_is_better=True)
        scores.append(opm_pctile)

    composite = round(sum(scores) / len(scores))

    # Relative valuation
    quality_adj = quality_adjustment_factor(data, benchmark)
    eps = data.get("eps")
    fair_pe = round(benchmark["pe"] * quality_adj, 1)
    relative_fair_value = round(eps * fair_pe, 2) if eps and eps > 0 else None

    price = data.get("current_price", 0)
    premium_discount = None
    if relative_fair_value and price > 0:
        premium_discount = round(((price - relative_fair_value) / relative_fair_value) * 100, 2)

    # Verdict
    if composite >= 75:
        verdict = "Best-in-class"
    elif composite >= 55:
        verdict = "Above Average"
    elif composite >= 40:
        verdict = "Average"
    elif composite >= 25:
        verdict = "Below Average"
    else:
        verdict = "Laggard"

    result = {
        "company": data.get("name", "Unknown"),
        "ticker": data.get("ticker", "Unknown"),
        "sector": sector,
        "sector_benchmarks": benchmark,
        "percentile_ranks": {
            "pe_percentile": pe_pctile,
            "roe_percentile": roe_pctile,
            "composite_score": composite,
        },
        "relative_valuation": {
            "quality_adjustment_factor": quality_adj,
            "fair_pe_multiple": fair_pe,
            "relative_fair_value": relative_fair_value,
            "current_price": price,
            "premium_discount_pct": premium_discount,
        },
        "peer_verdict": verdict,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
