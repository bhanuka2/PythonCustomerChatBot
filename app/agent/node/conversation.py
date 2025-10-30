from app.agent.state import State
import uuid


def generate_conversational_response(state: State) -> State:
    """Generate simple conversational response"""
    user_query = state.get("user_query", "").lower().strip()
    session_id = state.get("session_id") or str(uuid.uuid4())

    # Simple greeting response
    if any(word in user_query for word in ["hello", "hi", "hey"]):
        state["response"] = "Hello! How can I help you with flight information?"
    elif any(word in user_query for word in ["help"]):
        state["response"] = "I can help you search for flights. Try asking about flight numbers, airlines, or routes."
    else:
        state["response"] = "I'm here to help with flight information. What would you like to know?"

    state["session_id"] = session_id
    state["awaiting_confirmation"] = False

    return state



