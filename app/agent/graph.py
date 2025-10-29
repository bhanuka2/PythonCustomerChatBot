from langgraph.graph import StateGraph

from app.agent.node.chatbot_node import flight_graph, show_ticket_summary, convert_to_lkr
from app.agent.state import State
from langgraph.graph import StateGraph, START, END

from app.model.Flight_Tracer import FlightTracer


def gen_graph():
    workflow = StateGraph(State)

    return workflow.compile()

builder = StateGraph(FlightTracer)

builder.add_node("get_details", get_flight_details)
builder.add_node("convert_lkr", convert_to_lkr())
builder.add_node("summary", show_ticket_summary)

builder.add_edge(START, "get_details")
builder.add_edge("get_details", "calc_total")
builder.add_edge("calc_total", "convert_lkr")
builder.add_edge("convert_lkr", "summary")
builder.add_edge("summary", END)

flight_graph = builder.compile()