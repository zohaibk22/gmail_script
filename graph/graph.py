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
    email_id: Optional[str]  # Optional, if you want to track email IDs
    is_relevant: bool
    reason: str
    job_info: dict
    index: int
    end_graph: bool

def fetch_node(state) -> dict:
    emails = fetch_today_emails()
    return {"emails": emails, 'index': 0}

# def classify_node(state):
#     email:str  = state["email"]
#     print('------EMAIL------', email)
#     result: dict = classify_email(email)
#     return {"email": email, "is_relevant": result["is_job_application"], "reason": result["reason"]}

def classify_node(state):
    # print(state, " STATE IN CLASSIFY NODE")
    index = state["index"]
    email = state["emails"][index]
    result = classify_email(email)
    return {
        "email": email,
        "is_relevant": result["is_job_application"],
        "reason": result["reason"],
        "email_id": email.get("id")  # Include email ID if needed
    }

def extract_node(state):
    # print(state, " STATE IN EXTRACT NODE")
    info = extract_email_content(state["email"])
    return {"email": state["email"], "job_info": info}

def write_node(state):
    print(state.get("email"), " STATE IN WRITE NODE")
    write_to_sheet({**state["job_info"], 'email_id': state.get("email_id")})
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

    graph.add_edge("fetch_emails", "classify_email")

    # The graph processes one email at a time by using the 'index' to track the current email.
    # After processing (classify -> extract -> write), it increments 'index' and loops back if more emails remain.

    graph.add_conditional_edges(
        "classify_email",
        lambda state: "extract_info" if state["is_relevant"] else 'write_next'
    )

    def write_next_node(state):
        # print(state, " STATE IN WRITE NEXT NODE")
        next_index = state['index'] + 1
        if next_index < len(state['emails']):
            return {'index': next_index, 'end_graph': False}
        else:
            return {'end_graph': True}
        
    graph.add_node("write_next", write_next_node)

    graph.add_edge("extract_info", "write_sheet")
    graph.add_edge("write_sheet", "write_next")
 # graph.add_edge(te_sheet", END)
    graph.add_conditional_edges(
    "write_next",
    lambda state: "classify_email" if not state['end_graph'] else END
    )

    return graph.compile()
