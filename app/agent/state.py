from typing import TypedDict, List, Optional, Any
from datetime import datetime
from langchain_core.messages import BaseMessage


class State(TypedDict, total=False):
    message: List[BaseMessage]
    user_query: str
    response: str
    decision: str
    sql_query: str




