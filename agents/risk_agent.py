from agents.state import ReportState
from tools.stock_tools import get_risk_data
from config import get_llm


def risk_node(state: ReportState) -> ReportState:
    ticker = state["ticker"]
    print(f"[risk_agent] 评估风险: {ticker}")

    try:
        d = get_risk_data(ticker)
        prompt = (
            f"Write a concise 3-4 sentence risk assessment for {state['company_name']} ({ticker}) in English.\n\n"
            f"Annualized Volatility: {d['annualized_volatility']}%\n"
            f"Beta: {d['beta']}\n"
            f"52-Week High: {d['week52_high']} | 52-Week Low: {d['week52_low']}\n"
            f"Max Drawdown (6mo): {d['max_drawdown_6mo']}%\n\n"
            "Assess the risk level (Low / Medium / High) with key risk factors. "
            "Do NOT make any investment guarantees or promises."
        )
        result = get_llm().invoke(prompt).content
    except Exception as e:
        result = f"Risk assessment unavailable: {e}"

    print("[risk_agent] 完成")
    return {"risk_data": result}
