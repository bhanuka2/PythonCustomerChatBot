# app/service/chat_service.py
from pyexpat.errors import messages
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.agent.graph import gen_graph
from app.agent.state import State
from app.core.database import SessionLocal
from app.model.Flight_Tracer import FlightTracer
from app.schema.chat import MessageRequestSchema, MessageResponseSchema
from datetime import datetime
import uuid
import re


class ChatService:

    def __init__(self):
        self.db: Session = SessionLocal()
        self.agent = gen_graph()
        self.chat_history = {}

    async def send_message(self, request: MessageRequestSchema) -> MessageResponseSchema:
        # Generate or use existing session ID
        session_id = request.session_id or str(uuid.uuid4())

        # Initialize session history if new
        if session_id not in self.chat_history:
            self.chat_history[session_id] = []

        user_msg = request.message.lower().strip()


        initialState : State = {"message" : [],
                                "user_query" : user_msg,
                                "response":""}

        agent_state = await self.agent.ainvoke(initialState)

        reply = agent_state["response"]

        # # Store conversation in history
        # self.chat_history[session_id].append({
        #     "user": request.message,
        #     "bot": reply,
        #     "timestamp": datetime.now()
        # })

        return MessageResponseSchema(
            message=reply,
            session_id=session_id,
            timestamp=datetime.now()
        )

    async def _process_message(self, user_msg: str) -> str:
        """Process user message and generate appropriate response"""

        # 1. Check for flight number query
        flight_number = self._extract_flight_number(user_msg)
        if flight_number:
            return await self._get_flight_details(flight_number)

        # 2. Search by airline
        if any(keyword in user_msg for keyword in ["airline", "carrier"]):
            airline_name = self._extract_airline_name(user_msg)
            if airline_name:
                return await self._search_by_airline(airline_name)

        # 3. Search by route (origin/destination)
        if any(keyword in user_msg for keyword in ["from", "to", "route"]):
            origin, destination = self._extract_route(user_msg)
            if origin or destination:
                return await self._search_by_route(origin, destination)

        # 4. Price queries
        if any(keyword in user_msg for keyword in ["price", "cost", "cheap", "expensive"]):
            return await self._search_by_price(user_msg)

        # 5. List all flights
        if any(keyword in user_msg for keyword in ["all flights", "show all", "list flights"]):
            return await self._list_all_flights()

        # 6. Help/Greeting
        if any(keyword in user_msg for keyword in ["hello", "hi", "hey", "help"]):
            return self._get_help_message()

        # Default fallback
        return (
            "I can help you with:\n"
            "• Flight details (e.g., 'show flight AI202')\n"
            "• Search by airline (e.g., 'Air India flights')\n"
            "• Search by route (e.g., 'flights from Delhi to Mumbai')\n"
            "• Price queries (e.g., 'cheap flights')\n"
            "• List all flights (e.g., 'show all flights')"
        )

    def _extract_flight_number(self, msg: str) -> str:
        """Extract flight number from message"""
        # Match common airline codes followed by digits
        pattern = r'\b([A-Z]{2}\d{2,4})\b'
        match = re.search(pattern, msg.upper())
        return match.group(1) if match else None

    def _extract_airline_name(self, msg: str) -> str:
        """Extract airline name from message"""
        airlines = {
            "air india": "Air India",
            "emirates": "Emirates",
            "qatar": "Qatar Airways",
            "british": "British Airways",
            "singapore": "Singapore Airlines",
            "cathay": "Cathay Pacific",
            "delta": "Delta",
            "qantas": "Qantas",
            "air france": "Air France",
            "turkish": "Turkish Airlines"
        }
        for key, value in airlines.items():
            if key in msg:
                return value
        return None

    def _extract_route(self, msg: str):
        """Extract origin and destination from message"""
        # Simple extraction (can be enhanced with NLP)
        origin = None
        destination = None

        if "from" in msg and "to" in msg:
            parts = msg.split("from")[1].split("to")
            origin = parts[0].strip().title()
            destination = parts[1].strip().title()

        return origin, destination

    async def _get_flight_details(self, flight_number: str) -> str:
        """Get details for a specific flight"""
        flight = self.db.query(FlightTracer).filter(
            FlightTracer.flight_number == flight_number
        ).first()

        if not flight:
            return f"❌ No data found for flight {flight_number}. Try 'list flights' to see available flights."

        return (
            f"✈️ **{flight.airline} {flight.flight_number}**\n"
            f"📍 Route: {flight.origin} → {flight.destination}\n"
            f"🛫 Departure: {flight.departure.strftime('%Y-%m-%d %H:%M') if flight.departure else 'N/A'}\n"
            f"🛬 Arrival: {flight.arrival.strftime('%Y-%m-%d %H:%M') if flight.arrival else 'N/A'}\n"
            f"💰 Ticket Price: ${flight.ticket_price:.2f}\n\n"
            f"Need more info? Ask about other flights or routes!"
        )

    async def _search_by_airline(self, airline_name: str) -> str:
        """Search flights by airline"""
        flights = self.db.query(FlightTracer).filter(
            FlightTracer.airline.ilike(f"%{airline_name}%")
        ).limit(5).all()

        if not flights:
            return f"❌ No flights found for {airline_name}."

        result = f"✈️ **{airline_name} Flights:**\n\n"
        for flight in flights:
            result += (
                f"• {flight.flight_number}: {flight.origin} → {flight.destination} "
                f"(${flight.ticket_price:.2f})\n"
            )

        return result + "\nAsk about a specific flight number for more details!"

    async def _search_by_route(self, origin: str, destination: str) -> str:
        """Search flights by route"""
        query = self.db.query(FlightTracer)

        if origin:
            query = query.filter(FlightTracer.origin.ilike(f"%{origin}%"))
        if destination:
            query = query.filter(FlightTracer.destination.ilike(f"%{destination}%"))

        flights = query.limit(5).all()

        if not flights:
            return f"❌ No flights found for this route."

        route_desc = f"{origin or 'Any'} → {destination or 'Any'}"
        result = f"✈️ **Flights for {route_desc}:**\n\n"

        for flight in flights:
            result += (
                f"• {flight.flight_number} ({flight.airline}): "
                f"{flight.origin} → {flight.destination} - ${flight.ticket_price:.2f}\n"
            )

        return result + "\nAsk about a specific flight for full details!"

    async def _search_by_price(self, msg: str) -> str:
        """Search flights by price criteria"""
        if "cheap" in msg or "under" in msg:
            flights = self.db.query(FlightTracer).order_by(
                FlightTracer.ticket_price.asc()
            ).limit(5).all()
            title = "💰 **Cheapest Flights:**"
        else:
            flights = self.db.query(FlightTracer).order_by(
                FlightTracer.ticket_price.desc()
            ).limit(5).all()
            title = "💎 **Premium Flights:**"

        if not flights:
            return "❌ No flight data available."

        result = f"{title}\n\n"
        for flight in flights:
            result += (
                f"• {flight.flight_number} ({flight.airline}): "
                f"{flight.origin} → {flight.destination} - ${flight.ticket_price:.2f}\n"
            )

        return result

    async def _list_all_flights(self) -> str:
        """List all available flights"""
        flights = self.db.query(FlightTracer).limit(10).all()

        if not flights:
            return "❌ No flights available in the database."

        result = "✈️ **Available Flights:**\n\n"
        for flight in flights:
            result += (
                f"• {flight.flight_number} ({flight.airline}): "
                f"{flight.origin} → {flight.destination} - ${flight.ticket_price:.2f}\n"
            )

        if len(flights) == 10:
            result += "\n(Showing first 10 flights. Ask about specific routes or airlines!)"

        return result

    def _get_help_message(self) -> str:
        """Return help message"""
        return (
            "👋 **Hello! I'm your Flight Assistant!**\n\n"
            "I can help you with:\n"
            "✈️ Flight details: 'show flight AI202'\n"
            "🏢 Search by airline: 'Emirates flights'\n"
            "📍 Search by route: 'flights from Delhi to Mumbai'\n"
            "💰 Price search: 'cheap flights' or 'expensive flights'\n"
            "📋 List all: 'show all flights'\n\n"
            "What would you like to know?"
        )

    def get_chat_history(self, session_id: str):
        """Get chat history for a session"""
        return self.chat_history.get(session_id, [])

    def __del__(self):
        """Clean up database session"""
        if hasattr(self, 'db'):
            self.db.close()


def get_chat_service():
    return ChatService()
