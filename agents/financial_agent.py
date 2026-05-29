from agents.state import ReportState
from tools.stock_tools import get_financial_data
from config import get_llm


def financial_node(state: ReportState) -> ReportState:
    ticker = state["ticker"]
    print(f"[financial_agent] 分析财务数据: {ticker}")

    try:
        d = get_financial_data(ticker)
        market_cap = f"${d['market_cap']/1e9:.1f}B" if isinstance(d["market_cap"], (int, float)) else "N/A"
        revenue = f"${d['revenue']/1e9:.1f}B" if isinstance(d["revenue"], (int, float)) else "N/A"
        margin = f"{d['profit_margin']*100:.1f}%" if isinstance(d["profit_margin"], float) else "N/A"

        prompt = (
            f"Write a concise 3-4 sentence financial overview for {d['company_name']} ({ticker}) in English.\n\n"
            f"Sector: {d['sector']} | Industry: {d['industry']}\n"
            f"Market Cap: {market_cap} | P/E Ratio: {d['pe_ratio']} | EPS: {d['eps']}\n"
            f"Revenue: {revenue} | Profit Margin: {margin} | Dividend Yield: {d['dividend_yield']}\n\n"
            f"Business: {d['description']}\n\n"
            "Focus on valuation, profitability, and business strength."
        )
        result = get_llm().invoke(prompt).content
    except Exception as e:
        result = f"Financial analysis unavailable: {e}"

    print("[financial_agent] 完成")
    return {"financial_data": result}
