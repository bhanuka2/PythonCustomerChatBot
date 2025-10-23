from fastapi import APIRouter

from app.schema.chat import MessageRequestSchema, MessageResponseSchema

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message", response_model=MessageResponseSchema)
def send_message(
        request: MessageRequestSchema,
):

    return "Lakmal"
