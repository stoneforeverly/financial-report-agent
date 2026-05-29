from duckduckgo_search import DDGS


def search_news(query: str, max_results: int = 6) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))
        if not results:
            return "No recent news found."
        lines = [f"- {r.get('title', '')}: {r.get('body', '')[:200]}" for r in results]
        return "\n".join(lines)
    except Exception as e:
        return f"News search unavailable: {str(e)}"
