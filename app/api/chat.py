from fastapi import APIRouter, Depends

from app.schema.chat import MessageRequestSchema, MessageResponseSchema
from app.service.chat_service import ChatService, get_chat_service

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message", response_model=MessageResponseSchema)
async def send_message(
        request: MessageRequestSchema,
        chat_service: ChatService = Depends(get_chat_service)
):

    return await chat_service.send_message(request)

