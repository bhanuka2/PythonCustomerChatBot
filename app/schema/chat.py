from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageRequestSchema(BaseModel):
    message: str
    session_id: Optional[str] = None


class MessageResponseSchema(BaseModel):
    message: str
    session_id: str
    timestamp: datetime
