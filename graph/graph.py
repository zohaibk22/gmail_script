from langgraph.graph import StateGraph, END
from agents import fetch_today_emails
from agents import classify_email
from agents import extract_email_content
from agents import write_to_sheet
from typing import TypedDict, Optional

# Step 1: Define each LangGraph-compatible node

class GraphState(TypedDict, total=False):
    emails: list
    email: dict
    is_relevant: bool
    reason: str
    job_info: dict

def fetch_node(state):
    emails = fetch_today_emails()
    return {"emails": emails}

def classify_node(state):
    email = state["email"]
    result = classify_email(email)
    return {"email": email, "is_relevant": result["is_job_application"], "reason": result["reason"]}

def extract_node(state):
    info = extract_email_content(state["email"])
    return {"email": state["email"], "job_info": info}

def write_node(state):
    write_to_sheet(state["job_info"])
    return {}

# Step 2: Build the graph
def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("fetch_emails", fetch_node)
    graph.add_node("classify_email", classify_node)
    graph.add_node("extract_info", extract_node)
    graph.add_node("write_sheet", write_node)

    # Entry point
    graph.set_entry_point("fetch_emails")

    # Fan out each email for classification
    graph.add_conditional_edges(
        "fetch_emails",
        lambda state: [
            {"email": email} for email in state["emails"]
        ],
        next_node="classify_email"
    )

    graph.add_conditional_edges(
        "classify_email",
        lambda state: "extract_info" if state["is_relevant"] else END
    )

    graph.add_edge("extract_info", "write_sheet")
    graph.add_edge("write_sheet", END)

    return graph.compile()
