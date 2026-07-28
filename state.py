from typing import TypedDict, List, Annotated
import operator

class SMEState(TypedDict):
    user_query: str
    intent: str
    retrieved_docs: List[str]
    financial_analysis: str
    final_report: str
    messages: Annotated[List[str], operator.add]