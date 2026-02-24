"""
Format a complete stock analysis report.

Usage: python scripts/format_report.py <company_slug> [data_dir]

Loads all data/{slug}_*.json files and produces a formatted text report
with sections: Company Overview, Recommendation, Technical Analysis,
Sentiment, Risks, and Disclaimer.
"""

import json
import os
import sys
from datetime import datetime, timezone


def load_json(filepath: str) -> dict | None:
    """Load a JSON file, return None if not found."""
    try:
        with open(filepath) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def format_price(value: float | None) -> str:
    """Format a price value in INR."""
    if value is None:
        return "N/A"
    if value >= 10000000:  # 1 crore
        return f"Rs.{value / 10000000:,.2f} Cr"
    if value >= 100000:  # 1 lakh
        return f"Rs.{value / 100000:,.2f} L"
    return f"Rs.{value:,.2f}"


def format_percent(value: float | None) -> str:
    """Format a percentage value."""
    if value is None:
        return "N/A"
    return f"{value:+.2f}%"


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/format_report.py <company_slug> [data_dir]", file=sys.stderr)
        sys.exit(1)

    slug = sys.argv[1]
    data_dir = sys.argv[2] if len(sys.argv) > 2 else "data"

    # Load all data files
    tickertape = load_json(os.path.join(data_dir, f"{slug}_tickertape.json"))
    stocktwits = load_json(os.path.join(data_dir, f"{slug}_stocktwits.json"))
    financials = load_json(os.path.join(data_dir, f"{slug}_financials.json"))
    news = load_json(os.path.join(data_dir, f"{slug}_news.json"))
    peers = load_json(os.path.join(data_dir, f"{slug}_peers.json"))
    sentiment = load_json(os.path.join(data_dir, f"{slug}_sentiment.json"))
    technical = load_json(os.path.join(data_dir, f"{slug}_technical.json"))
    recommendation = load_json(os.path.join(data_dir, f"{slug}_recommendation.json"))
    risk = load_json(os.path.join(data_dir, f"{slug}_risk.json"))

    if not tickertape and not recommendation:
        print(f"ERROR: No data files found for slug '{slug}' in {data_dir}/", file=sys.stderr)
        sys.exit(1)

    company_name = "Unknown Company"
    if tickertape:
        company_name = tickertape.get("name", company_name)
    elif recommendation:
        company_name = recommendation.get("company", company_name)

    report_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Build report
    lines = []
    w = 60  # Report width

    lines.append("=" * w)
    lines.append(f"  STOCK ANALYSIS REPORT")
    lines.append(f"  {company_name}")
    lines.append(f"  Generated: {report_time}")
    lines.append("=" * w)

    # === Company Overview ===
    lines.append("")
    lines.append("-" * w)
    lines.append("  COMPANY OVERVIEW")
    lines.append("-" * w)
    if tickertape:
        lines.append(f"  Ticker:          {tickertape.get('ticker', 'N/A')}")
        lines.append(f"  Exchange:        {tickertape.get('exchange', 'NSE')}")
        lines.append(f"  Sector:          {tickertape.get('sector', 'N/A')}")
        lines.append(f"  Industry:        {tickertape.get('industry', 'N/A')}")
        lines.append(f"  Current Price:   {format_price(tickertape.get('current_price'))}")
        lines.append(f"  Market Cap:      {format_price(tickertape.get('market_cap'))}")
        lines.append(f"  PE Ratio:        {tickertape.get('pe_ratio', 'N/A')}")
        lines.append(f"  PB Ratio:        {tickertape.get('pb_ratio', 'N/A')}")
        lines.append(f"  52W High:        {format_price(tickertape.get('week_52_high'))}")
        lines.append(f"  52W Low:         {format_price(tickertape.get('week_52_low'))}")
        lines.append(f"  Day Change:      {format_percent(tickertape.get('day_change_percent'))}")
    else:
        lines.append("  [Tickertape data unavailable]")

    # === Recommendation ===
    lines.append("")
    lines.append("-" * w)
    lines.append("  RECOMMENDATION")
    lines.append("-" * w)
    if recommendation:
        action = recommendation.get("recommendation", "N/A")
        conviction = recommendation.get("conviction", "N/A")
        lines.append(f"  Action:          {action}")
        lines.append(f"  Conviction:      {conviction}")
        lines.append(f"  Composite Score: {recommendation.get('composite_score', 'N/A')}")
        lines.append("")
        lines.append(f"  Thesis: {recommendation.get('investment_thesis', 'N/A')}")

        entry = recommendation.get("entry_strategy", {})
        if entry:
            lines.append("")
            lines.append(f"  Entry Price:     {format_price(entry.get('recommended_entry'))}")
            lines.append(f"  Stop Loss:       {format_price(entry.get('stop_loss'))} ({format_percent(entry.get('stop_loss_percent'))})")

        targets = recommendation.get("profit_targets", [])
        if targets:
            lines.append("")
            lines.append("  Profit Targets:")
            for t in targets:
                lines.append(f"    {t.get('label', '?')}: {format_price(t.get('price'))} ({format_percent(t.get('return_percent'))}) - {t.get('timeframe', 'N/A')}")
    else:
        lines.append("  [Recommendation data unavailable]")

    # === Technical Analysis ===
    lines.append("")
    lines.append("-" * w)
    lines.append("  TECHNICAL ANALYSIS")
    lines.append("-" * w)
    if technical:
        lines.append(f"  Trend:           {technical.get('current_trend', 'N/A')}")
        lines.append(f"  Strength:        {technical.get('trend_strength', 'N/A')}")
        lines.append(f"  52W Position:    {technical.get('week_52_position', 'N/A')}%")
        lines.append(f"  Signal:          {technical.get('technical_signal', 'N/A')}")

        indicators = technical.get("indicators", {})
        if indicators:
            lines.append("")
            lines.append(f"  RSI Estimate:    {indicators.get('rsi_estimate', 'N/A')}")
            lines.append(f"  Momentum:        {indicators.get('momentum', 'N/A')}")
            lines.append(f"  Volume Signal:   {indicators.get('volume_signal', 'N/A')}")

        sr = technical.get("support_resistance", {})
        if sr:
            lines.append("")
            lines.append(f"  Support 1:       {format_price(sr.get('support_1'))}")
            lines.append(f"  Support 2:       {format_price(sr.get('support_2'))}")
            lines.append(f"  Resistance 1:    {format_price(sr.get('resistance_1'))}")
            lines.append(f"  Resistance 2:    {format_price(sr.get('resistance_2'))}")
    else:
        lines.append("  [Technical analysis unavailable]")

    # === Sentiment ===
    lines.append("")
    lines.append("-" * w)
    lines.append("  SENTIMENT ANALYSIS")
    lines.append("-" * w)
    if sentiment:
        lines.append(f"  Overall:         {sentiment.get('sentiment_label', 'N/A')} ({sentiment.get('overall_sentiment', 'N/A')})")
        lines.append(f"  Confidence:      {sentiment.get('confidence_score', 'N/A')}/100")

        breakdown = sentiment.get("sentiment_breakdown", {})
        if breakdown:
            lines.append("")
            lines.append(f"  Social Score:    {breakdown.get('social_score', 'N/A')} (weight: {breakdown.get('social_weight', 0.4)})")
            lines.append(f"  Market Score:    {breakdown.get('market_score', 'N/A')} (weight: {breakdown.get('market_weight', 0.3)})")
            lines.append(f"  Fundamental:     {breakdown.get('fundamental_score', 'N/A')} (weight: {breakdown.get('fundamental_weight', 0.3)})")

        insights = sentiment.get("key_insights", [])
        if insights:
            lines.append("")
            lines.append("  Key Insights:")
            for insight in insights:
                lines.append(f"    - {insight}")
    else:
        lines.append("  [Sentiment analysis unavailable]")

    # === Financial Analysis ===
    lines.append("")
    lines.append("-" * w)
    lines.append("  FINANCIAL ANALYSIS")
    lines.append("-" * w)
    if financials:
        vals = financials.get("valuations", {})
        lines.append(f"  Health Score:    {financials.get('financial_health_score', 'N/A')}/100")
        lines.append(f"  Signal:          {financials.get('financial_signal', 'N/A')}")
        lines.append("")
        lines.append(f"  Graham Number:   {format_price(vals.get('graham_number'))}")
        lines.append(f"  PE Fair Value:   {format_price(vals.get('pe_fair_value'))} (at {vals.get('pe_fair_multiple', 'N/A')}x PE)")
        lines.append(f"  DCF Fair Value:  {format_price(vals.get('dcf_fair_value'))}")
        lines.append(f"  Blended Fair:    {format_price(vals.get('blended_fair_value'))}")
        upside = vals.get("upside_to_fair_value_pct")
        if upside is not None:
            lines.append(f"  Upside to Fair:  {format_percent(upside)}")

        growth = financials.get("annual_growth", {})
        if growth:
            lines.append("")
            lines.append(f"  Rev CAGR 3Y:     {format_percent(growth.get('revenue_cagr_3yr'))}")
            lines.append(f"  Rev CAGR 5Y:     {format_percent(growth.get('revenue_cagr_5yr'))}")
            lines.append(f"  Profit CAGR 3Y:  {format_percent(growth.get('profit_cagr_3yr'))}")

        observations = financials.get("key_observations", [])
        if observations:
            lines.append("")
            for obs in observations:
                lines.append(f"    - {obs}")
    else:
        lines.append("  [Financial analysis unavailable]")

    # === Peer Comparison ===
    lines.append("")
    lines.append("-" * w)
    lines.append("  PEER COMPARISON")
    lines.append("-" * w)
    if peers:
        lines.append(f"  Sector:          {peers.get('sector', 'N/A')}")
        rel_pos = peers.get("relative_position", {})
        lines.append(f"  PE Percentile:   {rel_pos.get('pe_percentile', 'N/A')}th")
        lines.append(f"  ROE Percentile:  {rel_pos.get('roe_percentile', 'N/A')}th")
        lines.append(f"  Composite Rank:  #{rel_pos.get('composite_rank', 'N/A')} of {rel_pos.get('out_of', 'N/A')}")
        lines.append(f"  Verdict:         {peers.get('peer_verdict', 'N/A')}")

        rel_val = peers.get("relative_valuation", {})
        if rel_val:
            lines.append("")
            lines.append(f"  Peer Fair Value: {format_price(rel_val.get('blended_peer_fair_value'))}")
            lines.append(f"  Premium/Disc:    {format_percent(rel_val.get('premium_discount_percent'))}")

        peer_list = peers.get("peers", [])
        if peer_list:
            lines.append("")
            lines.append("  Peers:")
            for p in peer_list[:5]:
                lines.append(f"    - {p.get('name', '?')} (PE: {p.get('pe_ratio', 'N/A')}, ROE: {p.get('roe', 'N/A')}%)")
    else:
        lines.append("  [Peer comparison unavailable]")

    # === News & Events ===
    lines.append("")
    lines.append("-" * w)
    lines.append("  NEWS & EVENTS")
    lines.append("-" * w)
    if news:
        lines.append(f"  News Score:      {news.get('aggregate_news_score', 'N/A')}")
        lines.append(f"  Sentiment:       {news.get('news_sentiment_label', 'N/A')}")
        lines.append(f"  Items Analyzed:  {news.get('total_items', 0)}")

        red_flags = news.get("red_flags", [])
        if red_flags:
            lines.append("")
            lines.append("  RED FLAGS:")
            for flag in red_flags:
                lines.append(f"    !! {flag}")

        catalysts = news.get("upcoming_catalysts", [])
        if catalysts:
            lines.append("")
            lines.append("  Upcoming Catalysts:")
            for cat in catalysts:
                lines.append(f"    - {cat.get('event', '?')} ({cat.get('expected_date', 'TBD')})")

        themes = news.get("key_themes", [])
        if themes:
            lines.append("")
            lines.append("  Key Themes:")
            for theme in themes:
                lines.append(f"    - {theme}")
    else:
        lines.append("  [News analysis unavailable]")

    # === Risk Assessment (enhanced) ===
    lines.append("")
    lines.append("-" * w)
    lines.append("  RISK ASSESSMENT")
    lines.append("-" * w)

    if risk:
        lines.append(f"  Risk Rating:     {risk.get('risk_rating', 'N/A')}")
        vol = risk.get("volatility", {})
        lines.append(f"  Annual Vol:      {vol.get('estimated_annual', 'N/A')}%")
        lines.append(f"  Est. Beta:       {vol.get('estimated_beta', 'N/A')}")

        dd = risk.get("drawdown", {})
        lines.append(f"  Max Drawdown:    {dd.get('estimated_max_pct', 'N/A')}%")
        lines.append(f"  Recovery Time:   ~{dd.get('estimated_recovery_months', 'N/A')} months")

        var_data = risk.get("value_at_risk", {})
        if var_data:
            lines.append("")
            lines.append(f"  Daily VaR 95%:   {format_price(var_data.get('daily_var_95'))} (per 100 shares)")
            lines.append(f"  Monthly VaR 95%: {format_price(var_data.get('monthly_var_95'))} (per 100 shares)")

        pos = risk.get("position_sizing", {})
        if pos and "high" in pos:
            lines.append("")
            lines.append(f"  Position Sizing (for Rs.10L portfolio):")
            lines.append(f"    High conviction:   {pos['high'].get('shares', 0)} shares ({format_price(pos['high'].get('value', 0))})")
            lines.append(f"    Medium conviction: {pos['medium'].get('shares', 0)} shares ({format_price(pos['medium'].get('value', 0))})")
            lines.append(f"    Low conviction:    {pos['low'].get('shares', 0)} shares ({format_price(pos['low'].get('value', 0))})")

        rr = risk.get("risk_reward", {})
        if rr and "weighted_rr" in rr:
            lines.append("")
            lines.append(f"  Weighted R:R:    1:{rr['weighted_rr']}")

        scenarios = risk.get("scenarios", {})
        if scenarios:
            lines.append("")
            lines.append("  Scenario Analysis:")
            for case in ("bull", "base", "bear"):
                s = scenarios.get(case, {})
                lines.append(f"    {case.title()} ({int(s.get('probability', 0)*100)}%): {format_price(s.get('price'))} ({format_percent(s.get('return_pct'))})")
            lines.append(f"    Expected Value: {format_price(scenarios.get('expected_value'))}")

    elif recommendation and "risk_assessment" in recommendation:
        risk = recommendation["risk_assessment"]
        lines.append(f"  Risk Level:      {risk.get('risk_level', 'N/A')}")
        lines.append(f"  Max Downside:    {format_percent(risk.get('max_downside_percent'))}")
        lines.append("")
        lines.append(f"  Downside Scenario: {risk.get('downside_scenario', 'N/A')}")
        lines.append("")
        lines.append("  Key Risks:")
        for r in risk.get("key_risks", []):
            lines.append(f"    - {r}")
    else:
        lines.append("  [Risk assessment unavailable]")

    # === Disclaimer ===
    lines.append("")
    lines.append("=" * w)
    lines.append("  DISCLAIMER")
    lines.append("=" * w)
    lines.append("  This report is generated by an automated analysis")
    lines.append("  system and is for informational purposes only.")
    lines.append("  It does NOT constitute financial advice.")
    lines.append("  Always consult a qualified financial advisor")
    lines.append("  before making investment decisions.")
    lines.append("  Past performance does not guarantee future results.")
    lines.append("=" * w)

    print("\n".join(lines))


if __name__ == "__main__":
    main()
