from app.agent.state import State


def request_user_confirmation(state: State) -> State:
    """Request user confirmation before executing database query"""
    print("[REQUEST_CONFIRMATION] Requesting user confirmation")

    database_result = state.get("database_result", "")

    # Format confirmation message
    confirmation_msg = (
        f"{database_result}\n\n"
        f"Would you like more details or search for other flights? (yes/no)"
    )

    state["response"] = confirmation_msg
    state["awaiting_confirmation"] = True

    print("[REQUEST_CONFIRMATION] Awaiting user confirmation")

    return state

