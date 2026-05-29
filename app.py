import streamlit as st
from agents.graph import build_graph

_I18N = {
    "en": {
        "title": "Financial Research Report Generator",
        "caption": "Multi-Agent AI · LangGraph · Price / News / Financial / Risk",
        "config": "Configuration",
        "ticker_label": "Stock Ticker Symbol",
        "ticker_placeholder": "Enter ticker, e.g. AAPL",
        "lang_label": "Report Language",
        "pipeline_title": "Agents Pipeline",
        "pipeline": (
            "Planner\n"
            "  ├─ Price Agent   ┐\n"
            "  ├─ News Agent    │ parallel\n"
            "  ├─ Financial     │\n"
            "  └─ Risk Agent   ─┘\n"
            "       Writer\n"
            "     Compliance\n"
            "    Localization"
        ),
        "generate_btn": "Generate Report",
        "spinner": "Analyzing {ticker} — running 4 agents in parallel...",
        "success": "Report ready: **{company}** ({ticker})",
        "download_pdf": "Download PDF",
        "download_md": "Download Markdown",
        "pdf_unavailable": "PDF export unavailable. Download Markdown instead.",
    },
    "zh-cn": {
        "title": "金融研究报告生成器",
        "caption": "多智能体 AI · LangGraph · 行情 / 新闻 / 财务 / 风险",
        "config": "设置",
        "ticker_label": "股票代码",
        "ticker_placeholder": "输入代码，例如 AAPL",
        "lang_label": "报告语言",
        "pipeline_title": "智能体流程",
        "pipeline": (
            "规划器\n"
            "  ├─ 行情 Agent   ┐\n"
            "  ├─ 新闻 Agent   │ 并行\n"
            "  ├─ 财务 Agent   │\n"
            "  └─ 风险 Agent  ─┘\n"
            "      撰写 Agent\n"
            "      合规审查\n"
            "      多语言本地化"
        ),
        "generate_btn": "生成报告",
        "spinner": "正在分析 {ticker} — 4 个 Agent 并行运行中...",
        "success": "报告已生成：**{company}**（{ticker}）",
        "download_pdf": "下载 PDF",
        "download_md": "下载 Markdown",
        "pdf_unavailable": "PDF 导出不可用，请下载 Markdown 版本。",
    },
    "zh-tw": {
        "title": "金融研究報告生成器",
        "caption": "多智能體 AI · LangGraph · 行情 / 新聞 / 財務 / 風險",
        "config": "設定",
        "ticker_label": "股票代碼",
        "ticker_placeholder": "輸入代碼，例如 AAPL",
        "lang_label": "報告語言",
        "pipeline_title": "智能體流程",
        "pipeline": (
            "規劃器\n"
            "  ├─ 行情 Agent   ┐\n"
            "  ├─ 新聞 Agent   │ 並行\n"
            "  ├─ 財務 Agent   │\n"
            "  └─ 風險 Agent  ─┘\n"
            "      撰寫 Agent\n"
            "      合規審查\n"
            "      多語言本地化"
        ),
        "generate_btn": "生成報告",
        "spinner": "正在分析 {ticker} — 4 個 Agent 並行運行中...",
        "success": "報告已生成：**{company}**（{ticker}）",
        "download_pdf": "下載 PDF",
        "download_md": "下載 Markdown",
        "pdf_unavailable": "PDF 匯出不可用，請下載 Markdown 版本。",
    },
    "de": {
        "title": "Finanz-Research-Report Generator",
        "caption": "Multi-Agenten KI · LangGraph · Kurs / Nachrichten / Finanzen / Risiko",
        "config": "Einstellungen",
        "ticker_label": "Aktien-Ticker",
        "ticker_placeholder": "Ticker eingeben, z.B. SAP.DE",
        "lang_label": "Berichtssprache",
        "pipeline_title": "Agenten-Pipeline",
        "pipeline": (
            "Planer\n"
            "  ├─ Kurs-Agent    ┐\n"
            "  ├─ News-Agent    │ parallel\n"
            "  ├─ Finanz-Agent  │\n"
            "  └─ Risiko-Agent ─┘\n"
            "      Autor-Agent\n"
            "      Compliance\n"
            "      Lokalisierung"
        ),
        "generate_btn": "Bericht erstellen",
        "spinner": "{ticker} wird analysiert — 4 Agenten laufen parallel...",
        "success": "Bericht fertig: **{company}** ({ticker})",
        "download_pdf": "PDF herunterladen",
        "download_md": "Markdown herunterladen",
        "pdf_unavailable": "PDF-Export nicht verfügbar. Bitte Markdown herunterladen.",
    },
}

st.set_page_config(
    page_title="Financial Research Report Generator",
    page_icon="📈",
    layout="centered",
)

# 语言选择放最前面，后续所有 UI 文字依赖它
with st.sidebar:
    language = st.selectbox(
        "Report Language / 报告语言",
        options=["en", "zh-cn", "zh-tw", "de"],
        format_func=lambda x: {
            "en": "English",
            "zh-cn": "中文简体",
            "zh-tw": "中文繁體",
            "de": "Deutsch",
        }[x],
    )

_COMMON_STOCKS = [
    ("AAPL",    "Apple Inc."),
    ("MSFT",    "Microsoft"),
    ("NVDA",    "NVIDIA"),
    ("TSLA",    "Tesla"),
    ("GOOGL",   "Alphabet (Google)"),
    ("AMZN",    "Amazon"),
    ("META",    "Meta"),
    ("0700.HK", "腾讯 Tencent"),
    ("9988.HK", "阿里巴巴 Alibaba"),
    ("0005.HK", "汇丰 HSBC"),
    ("SAP.DE",  "SAP"),
    ("SIE.DE",  "Siemens"),
]

_CUSTOM_LABEL = {
    "en":    "✏️ Custom input...",
    "zh-cn": "✏️ 自定义输入...",
    "zh-tw": "✏️ 自訂輸入...",
    "de":    "✏️ Eigene Eingabe...",
}

t = _I18N[language]

st.title(f"📈 {t['title']}")
st.caption(t["caption"])

with st.sidebar:
    st.header(t["config"])

    stock_options = [f"{sym} — {name}" for sym, name in _COMMON_STOCKS] + [_CUSTOM_LABEL[language]]
    selected = st.selectbox(t["ticker_label"], options=stock_options)

    if selected == _CUSTOM_LABEL[language]:
        ticker = st.text_input(
            t["ticker_placeholder"],
            placeholder=t["ticker_placeholder"],
        ).upper().strip()
    else:
        ticker = selected.split(" — ")[0]

    st.divider()
    st.markdown(
        f"**{t['pipeline_title']}**\n\n"
        f"```\n{t['pipeline']}\n```"
    )

    generate = st.button(t["generate_btn"], type="primary", use_container_width=True)

if "graph" not in st.session_state:
    with st.spinner("Initializing agents..."):
        st.session_state.graph = build_graph()

if generate:
    if not ticker:
        st.warning("⚠️")
    else:
        st.session_state.report_result = None
        with st.spinner(t["spinner"].format(ticker=ticker)):
            try:
                initial_state = {
                    "ticker": ticker,
                    "language": language,
                    "company_name": ticker,
                    "price_data": "",
                    "news_data": "",
                    "financial_data": "",
                    "risk_data": "",
                    "draft_report": "",
                    "compliant_report": "",
                    "final_report": "",
                }
                st.session_state.report_result = st.session_state.graph.invoke(initial_state)
            except Exception as e:
                st.error(f"Error: {e}")
                st.exception(e)

if st.session_state.get("report_result"):
    result = st.session_state.report_result
    # 报告展示用生成时的语言翻译
    rt = _I18N[result["language"]]

    st.divider()
    st.success(rt["success"].format(company=result["company_name"], ticker=result["ticker"]))
    st.markdown(result["final_report"])

    _lang_suffix = {"en": "en", "zh-cn": "sc", "zh-tw": "tc", "de": "de"}
    lang_tag = _lang_suffix.get(result["language"], result["language"])
    base_name = f"{result['ticker']}_report_{lang_tag}"

    col1, col2 = st.columns(2)
    with col1:
        try:
            from utils.pdf_export import md_to_pdf
            pdf_bytes = md_to_pdf(result["final_report"])
            st.download_button(
                label=rt["download_pdf"],
                data=pdf_bytes,
                file_name=f"{base_name}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )
        except Exception:
            st.warning(rt["pdf_unavailable"])
    with col2:
        st.download_button(
            label=rt["download_md"],
            data=result["final_report"],
            file_name=f"{base_name}.md",
            mime="text/markdown",
            use_container_width=True,
        )
