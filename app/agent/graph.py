from langgraph.graph import StateGraph

from app.agent.state import State


def gen_graph():
    workflow = StateGraph(State)

    return workflow.compile()