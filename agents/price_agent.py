from agents.state import ReportState
from tools.stock_tools import get_price_data
from config import get_llm


def price_node(state: ReportState) -> ReportState:
    ticker = state["ticker"]
    print(f"[price_agent] 获取行情数据: {ticker}")

    try:
        d = get_price_data(ticker)
        prompt = (
            f"Analyze the following market price data for {state['company_name']} ({ticker}) "
            f"and write a concise 3-4 sentence price performance analysis in English.\n\n"
            f"Current Price: {d['currency']} {d['current_price']}\n"
            f"3-Month Change: {d['pct_change_3mo']}%\n"
            f"52-Week High: {d['week52_high']}\n"
            f"52-Week Low: {d['week52_low']}\n"
            f"Average Daily Volume: {d['avg_volume']:,}\n\n"
            "Focus on price trend, momentum, and notable support/resistance levels."
        )
        result = get_llm().invoke(prompt).content
    except Exception as e:
        result = f"Price data unavailable: {e}"

    print("[price_agent] 完成")
    return {"price_data": result}
