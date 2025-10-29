# app/service/chat_service.py
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.model.Flight_Tracer import FlightTracer
from app.schema.chat import MessageRequestSchema, MessageResponseSchema

class ChatService:

    def __init__(self):
        self.db: Session = SessionLocal()

    async def send_message(self, request: MessageRequestSchema) -> MessageResponseSchema:
        user_msg = request.message.lower().strip()

        # Example: "show me flight AI202"
        if "flight" in user_msg:
            # extract flight number (basic)
            parts = user_msg.split()
            flight_number = None
            for p in parts:
                if p.upper().startswith(("AI", "EK", "QR", "BA", "SQ", "CX", "DL", "QF", "AF", "TK")):
                    flight_number = p.upper()

            if not flight_number:
                return {"message": "Please specify a valid flight number."}

            flight = self.db.query(FlightTracer).filter(
                FlightTracer.flight_number == flight_number
            ).first()

            if not flight:
                return {"message": f"No data found for flight {flight_number}."}

            # Format chatbot-style response
            reply = (
                f"✈️ **{flight.airline} {flight.flight_number}**\n"
                f"From: {flight.origin} → {flight.destination}\n"
                f"Departure: {flight.departure}\n"
                f"Arrival: {flight.arrival}\n"
                f"Ticket Price: ${flight.ticket_price:.2f}"
            )
            return {"message": reply}

        # Default fallback
        return {"message": "Hi! You can ask me about flight details like 'Show me flight AI202'."}


def get_chat_service():
    return ChatService()
