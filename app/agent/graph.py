from langgraph.graph import StateGraph, START, END
from app.agent.state import State


def gen_graph():
    """Build a simple conversation graph"""
    workflow = StateGraph(State)

    # Basic graph - nodes can be added as needed
    return workflow.compile()


# Create the compiled graph
flight_graph = gen_graph()
