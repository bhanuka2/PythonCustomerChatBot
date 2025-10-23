from app.schema.chat import MessageRequestSchema


class ChatService:

    def __init__(self):
        pass

    async def send_message(self, request: MessageRequestSchema):
        return {
            "message": "Good Morning"
        }

def get_chat_service():
    return ChatService()