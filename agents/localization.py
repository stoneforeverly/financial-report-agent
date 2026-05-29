from agents.state import ReportState
from config import get_llm

_LANGUAGE_NAMES = {
    "en": "English",
    "zh-cn": "Simplified Chinese (简体中文)",
    "zh-tw": "Traditional Chinese (繁體中文)",
    "de": "German (Deutsch)",
}


def localization_node(state: ReportState) -> ReportState:
    language = state["language"]
    print(f"[localization] 目标语言: {language}")

    if language == "en":
        return {**state, "final_report": state["compliant_report"]}

    lang_name = _LANGUAGE_NAMES.get(language, "English")
    prompt = (
        f"Translate the following investment research report into {lang_name}. "
        f"Preserve all Markdown formatting and section structure exactly. "
        f"Translate all text including section headers naturally and professionally "
        f"as a financial document. Keep ticker symbols, numbers, and dates unchanged.\n\n"
        f"{state['compliant_report']}"
    )

    result = get_llm().invoke(prompt).content
    print("[localization] 翻译完成")
    return {**state, "final_report": result}
