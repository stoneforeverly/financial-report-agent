from langgraph.graph import StateGraph, START, END
from agents.state import ReportState
from agents.planner import planner_node
from agents.price_agent import price_node
from agents.news_agent import news_node
from agents.financial_agent import financial_node
from agents.risk_agent import risk_node
from agents.writer import writer_node
from agents.compliance import compliance_node
from agents.localization import localization_node


def build_graph():
    graph = StateGraph(ReportState)

    graph.add_node("planner", planner_node)
    graph.add_node("price_agent", price_node)
    graph.add_node("news_agent", news_node)
    graph.add_node("financial_agent", financial_node)
    graph.add_node("risk_agent", risk_node)
    graph.add_node("writer", writer_node)
    graph.add_node("compliance", compliance_node)
    graph.add_node("localization", localization_node)

    graph.add_edge(START, "planner")

    # Fan-out: 4 agents run in parallel
    graph.add_edge("planner", "price_agent")
    graph.add_edge("planner", "news_agent")
    graph.add_edge("planner", "financial_agent")
    graph.add_edge("planner", "risk_agent")

    # Fan-in: writer waits for all 4
    graph.add_edge("price_agent", "writer")
    graph.add_edge("news_agent", "writer")
    graph.add_edge("financial_agent", "writer")
    graph.add_edge("risk_agent", "writer")

    graph.add_edge("writer", "compliance")
    graph.add_edge("compliance", "localization")
    graph.add_edge("localization", END)

    return graph.compile()
