from fastapi.openapi.models import Schema
from pydantic import BaseModel


class MessageRequestSchema(BaseModel):
    message : str

class MessageResponseSchema(BaseModel):
    message : str
