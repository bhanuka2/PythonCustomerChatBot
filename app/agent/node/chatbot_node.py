from app.agent.graph import flight_graph
from app.model.Flight_Tracer import FlightTracer

from langgraph.graph import StateGraph, START, END

builder = StateGraph(dict)

builder.add_node("get_flight_details", flight_graph)
builder.add_edge(START, "get_flight_details")
builder.add_edge("get_flight_details", END)

graph = builder.compile()
graph.invoke({})

def convert_to_lkr(state: FlightTracer) -> FlightTracer:
    usd_to_lkr = 325.50
    usd_amount = state.get("ticket_price") or state.get("total_price_usd") or 0
    state["ticket_price_lkr"] = usd_amount * usd_to_lkr
    return state

def show_ticket_summary(state: FlightTracer) -> FlightTracer:
    print("---- Flight Ticket Summary ----")
    print(f"Airline: {state.get('airline', 'N/A')}")
    print(f"Flight No: {state.get('flight_number', 'N/A')}")
    print(f"From: {state.get('origin', 'N/A')} To: {state.get('destination', 'N/A')}")
    print(f"Departure: {state.get('departure', 'N/A')}")
    print(f"Arrival: {state.get('arrival', 'N/A')}")
    print(f"Total (USD): {state.get('ticket_price', state.get('total_price_usd', 'N/A'))}")
    print(f"Total (LKR): {state.get('ticket_price_lkr', 'N/A')}")
    print("--------------------------------")
    return state