from typing import TypedDict


class ReportState(TypedDict):
    ticker: str
    language: str        # "en" | "zh-cn" | "zh-tw" | "de"
    company_name: str
    price_data: str
    news_data: str
    financial_data: str
    risk_data: str
    draft_report: str
    compliant_report: str
    final_report: str
