from agents.state import ReportState
from tools.stock_tools import get_financial_data


def planner_node(state: ReportState) -> ReportState:
    ticker = state["ticker"]
    print(f"\n[planner] 开始分析: {ticker}, 语言: {state['language']}")

    try:
        data = get_financial_data(ticker)
        company_name = data.get("company_name") or ticker
    except Exception:
        company_name = ticker

    print(f"[planner] 公司名称: {company_name}")
    return {"company_name": company_name}
