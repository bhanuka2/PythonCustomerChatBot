from typing import TypedDict, List
from xmlrpc.client import DateTime

from langchain_core.messages import BaseMessage


class State(TypedDict):
    message: List[BaseMessage]
    user_query: str
    response: str

class FlightState(TypedDict):
    flight_number: str
    airline: str
    departure: DateTime
    arrival: DateTime
    origin: str
    destination: str
    ticket_price: float

