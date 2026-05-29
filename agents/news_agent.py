from agents.state import ReportState
from tools.search_tools import search_news
from config import get_llm


def news_node(state: ReportState) -> ReportState:
    company = state["company_name"]
    ticker = state["ticker"]
    print(f"[news_agent] 搜索新闻: {company}")

    try:
        raw = search_news(f"{company} {ticker} stock news earnings", max_results=6)
        prompt = (
            f"Based on the following recent news about {company} ({ticker}), "
            f"write a concise 3-4 sentence news analysis in English. "
            f"Highlight the most significant developments and their potential impact:\n\n{raw}"
        )
        result = get_llm().invoke(prompt).content
    except Exception as e:
        result = f"News analysis unavailable: {e}"

    print("[news_agent] 完成")
    return {"news_data": result}
