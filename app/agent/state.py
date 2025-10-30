from typing import TypedDict, List, Optional, Any
from datetime import datetime
from langchain_core.messages import BaseMessage


class State(TypedDict, total=False):
    """Main agent state for conversation and database queries"""
    message: List[BaseMessage]
    user_query: str
    response: str
    session_id: Optional[str]
    intent: Optional[str]  # classified intent: "conversation", "database", etc.
    awaiting_confirmation: bool  # whether we're waiting for user confirmation
    user_confirmed: Optional[bool]  # user's confirmation response
    database_result: Optional[str]  # result from database query
    query_executed: bool  # whether database query was executed
    sql_query: Optional[str]  # generated SQL query (if needed)
    error: Optional[str]  # any error messages


class FlightState(TypedDict):
    """Flight-specific state for flight booking workflows"""
    flight_number: str
    airline: str
    departure: Optional[datetime]
    arrival: Optional[datetime]
    origin: str
    destination: str
    ticket_price: float
    ticket_price_lkr: Optional[float]
    summary: Optional[str]

