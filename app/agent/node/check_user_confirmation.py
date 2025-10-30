from app.agent.state import State
from typing import Dict


def classify_intent(state: State) -> State:
    """Classify user intent from the message"""
    user_query = state.get("user_query", "").lower()

    print(f"[CLASSIFY_INTENT] Processing query: {user_query}")

    # Flight/database query keywords
    database_keywords = [
        "flight", "show", "search", "find", "price", "airline",
        "from", "to", "cheap", "expensive", "list", "all flights",
        "route", "destination", "origin"
    ]

    # Check if query contains database keywords
    if any(keyword in user_query for keyword in database_keywords):
        state["intent"] = "database"
        print("[CLASSIFY_INTENT] Intent classified as: database")
    else:
        state["intent"] = "conversation"
        print("[CLASSIFY_INTENT] Intent classified as: conversation")

    return state

