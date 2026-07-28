from langgraph.graph import StateGraph, END
from state import SMEState
from agents import (
    orchestrator_router_agent,
    regulation_search_agent,
    financial_suggestion_agent,
    report_generator_agent
)

graph_builder = StateGraph(SMEState)

graph_builder.add_node("Orchestrator", orchestrator_router_agent)
graph_builder.add_node("RAGSearch", regulation_search_agent)
graph_builder.add_node("FinancialAdvisor", financial_suggestion_agent)
graph_builder.add_node("ReportGenerator", report_generator_agent)

graph_builder.set_entry_point("Orchestrator")
graph_builder.add_edge("Orchestrator", "RAGSearch")
graph_builder.add_edge("RAGSearch", "FinancialAdvisor")
graph_builder.add_edge("FinancialAdvisor", "ReportGenerator")
graph_builder.add_edge("ReportGenerator", END)

app_graph = graph_builder.compile()