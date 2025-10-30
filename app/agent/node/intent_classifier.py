from app.agent.state import State
from app.service.chat_service import ChatService


def classify_intent(state: State) -> State:
    """
    Classify user intent from the message using chat service patterns
    Maps to the intelligent query processing in ChatService
    """
    user_query = state.get("user_query", "").lower().strip()

    print(f"[CLASSIFY_INTENT] Processing query: {user_query}")

    # Use ChatService's intelligent extraction methods
    chat_service = ChatService()

    # Check for flight number query (e.g., "show flight AI202")
    if chat_service._extract_flight_number(user_query):
        state["intent"] = "database"
        print("[CLASSIFY_INTENT] Intent: database (flight number detected)")
        return state

    # Check for airline query
    if chat_service._extract_airline_name(user_query):
        state["intent"] = "database"
        print("[CLASSIFY_INTENT] Intent: database (airline detected)")
        return state

    # Check for route query (from/to)
    origin, destination = chat_service._extract_route(user_query)
    if origin or destination:
        state["intent"] = "database"
        print("[CLASSIFY_INTENT] Intent: database (route detected)")
        return state

    # Check for price queries
    if any(keyword in user_query for keyword in ["price", "cost", "cheap", "expensive"]):
        state["intent"] = "database"
        print("[CLASSIFY_INTENT] Intent: database (price query)")
        return state

    # Check for list/search queries
    if any(keyword in user_query for keyword in ["all flights", "show all", "list flights", "search", "find"]):
        state["intent"] = "database"
        print("[CLASSIFY_INTENT] Intent: database (list query)")
        return state

    # Default to conversation for greetings, help, or general chat
    state["intent"] = "conversation"
    print("[CLASSIFY_INTENT] Intent: conversation")

    return state

