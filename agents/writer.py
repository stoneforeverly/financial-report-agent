from datetime import date
from agents.state import ReportState
from config import get_llm


def writer_node(state: ReportState) -> ReportState:
    print("\n[writer] 生成报告草稿")

    prompt = (
        f"You are a professional financial analyst. Write a structured investment research report "
        f"in English for {state['company_name']} ({state['ticker']}) using the analysis below.\n\n"
        f"## Price Analysis\n{state['price_data']}\n\n"
        f"## News Highlights\n{state['news_data']}\n\n"
        f"## Financial Overview\n{state['financial_data']}\n\n"
        f"## Risk Assessment\n{state['risk_data']}\n\n"
        f"Use this exact Markdown structure:\n"
        f"# {state['company_name']} ({state['ticker']}) — Investment Research Report\n"
        f"*{date.today().strftime('%B %d, %Y')}*\n\n"
        f"## Executive Summary\n"
        f"## Price Performance\n"
        f"## Recent Developments\n"
        f"## Financial Overview\n"
        f"## Risk Assessment\n"
        f"## Disclaimer\n\n"
        "The Disclaimer must clearly state this report is for informational purposes only "
        "and does not constitute financial or investment advice."
    )

    result = get_llm().invoke(prompt).content
    print(f"[writer] 草稿完成 ({len(result)} 字符)")
    return {**state, "draft_report": result}
