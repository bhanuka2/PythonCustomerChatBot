from typing import TypedDict, List

from langchain_core.messages import BaseMessage


class State(TypedDict):
    message: List[BaseMessage]
    user_query: str
    response: str
