from app.agent.state import State
from app.core.database import SessionLocal
from app.model.Flight_Tracer import FlightTracer
import re
from sqlalchemy import or_


def execute_database_query(state: State) -> State:
    """Execute database query to fetch flight information"""
    print("[EXECUTE_DB] Executing database query")

    user_query = state.get("user_query", "").lower()
    db = SessionLocal()

    try:
        # Extract flight number if present
        flight_number = _extract_flight_number(user_query)

        if flight_number:
            result = _get_flight_by_number(db, flight_number)
        elif any(word in user_query for word in ["cheap", "price", "expensive"]):
            result = _get_flights_by_price(db, user_query)
        elif "from" in user_query or "to" in user_query:
            result = _get_flights_by_route(db, user_query)
        elif any(word in user_query for word in ["airline", "carrier"]):
            result = _get_flights_by_airline(db, user_query)
        elif "all" in user_query or "list" in user_query:
            result = _get_all_flights(db)
        else:
            result = "I can help you search for flights. Try asking about specific flight numbers, routes, or airlines."

        state["database_result"] = result
        state["query_executed"] = True
        print("[EXECUTE_DB] Query executed successfully")

    except Exception as e:
        print(f"[EXECUTE_DB] Error: {e}")
        state["database_result"] = f"Sorry, I encountered an error: {str(e)}"
        state["query_executed"] = False
    finally:
        db.close()

    return state


def _extract_flight_number(query: str) -> str:
    """Extract flight number from query"""
    pattern = r'\b([A-Z]{2}\d{2,4})\b'
    match = re.search(pattern, query.upper())
    return match.group(1) if match else None


def _get_flight_by_number(db, flight_number: str) -> str:
    """Get flight details by flight number"""
    flight = db.query(FlightTracer).filter(
        FlightTracer.flight_number == flight_number
    ).first()

    if not flight:
        return f"❌ No flight found with number {flight_number}"

    return (
        f"✈️ **{flight.airline} {flight.flight_number}**\n"
        f"📍 Route: {flight.origin} → {flight.destination}\n"
        f"🛫 Departure: {flight.departure.strftime('%Y-%m-%d %H:%M') if flight.departure else 'N/A'}\n"
        f"🛬 Arrival: {flight.arrival.strftime('%Y-%m-%d %H:%M') if flight.arrival else 'N/A'}\n"
        f"💰 Ticket Price: ${flight.ticket_price:.2f}"
    )


def _get_flights_by_price(db, query: str) -> str:
    """Get flights sorted by price"""
    if "cheap" in query or "under" in query:
        flights = db.query(FlightTracer).order_by(FlightTracer.ticket_price.asc()).limit(5).all()
        title = "💰 **Cheapest Flights:**"
    else:
        flights = db.query(FlightTracer).order_by(FlightTracer.ticket_price.desc()).limit(5).all()
        title = "💎 **Premium Flights:**"

    if not flights:
        return "❌ No flights available"

    result = f"{title}\n\n"
    for flight in flights:
        result += f"• {flight.flight_number} ({flight.airline}): {flight.origin} → {flight.destination} - ${flight.ticket_price:.2f}\n"

    return result


def _get_flights_by_route(db, query: str) -> str:
    """Get flights by route"""
    origin, destination = None, None

    if "from" in query and "to" in query:
        parts = query.split("from")[1].split("to")
        origin = parts[0].strip().title()
        destination = parts[1].strip().title() if len(parts) > 1 else None

    q = db.query(FlightTracer)
    if origin:
        q = q.filter(FlightTracer.origin.ilike(f"%{origin}%"))
    if destination:
        q = q.filter(FlightTracer.destination.ilike(f"%{destination}%"))

    flights = q.limit(5).all()

    if not flights:
        return "❌ No flights found for this route"

    route_desc = f"{origin or 'Any'} → {destination or 'Any'}"
    result = f"✈️ **Flights for {route_desc}:**\n\n"
    for flight in flights:
        result += f"• {flight.flight_number} ({flight.airline}): {flight.origin} → {flight.destination} - ${flight.ticket_price:.2f}\n"

    return result


def _get_flights_by_airline(db, query: str) -> str:
    """Get flights by airline"""
    airlines = {
        "air india": "Air India",
        "emirates": "Emirates",
        "qatar": "Qatar Airways",
        "british": "British Airways",
        "singapore": "Singapore Airlines"
    }

    airline_name = None
    for key, value in airlines.items():
        if key in query:
            airline_name = value
            break

    if not airline_name:
        return "❌ Please specify an airline name"

    flights = db.query(FlightTracer).filter(
        FlightTracer.airline.ilike(f"%{airline_name}%")
    ).limit(5).all()

    if not flights:
        return f"❌ No flights found for {airline_name}"

    result = f"✈️ **{airline_name} Flights:**\n\n"
    for flight in flights:
        result += f"• {flight.flight_number}: {flight.origin} → {flight.destination} (${flight.ticket_price:.2f})\n"

    return result


def _get_all_flights(db) -> str:
    """Get all available flights"""
    flights = db.query(FlightTracer).limit(10).all()

    if not flights:
        return "❌ No flights available in the database"

    result = "✈️ **Available Flights:**\n\n"
    for flight in flights:
        result += f"• {flight.flight_number} ({flight.airline}): {flight.origin} → {flight.destination} - ${flight.ticket_price:.2f}\n"

    if len(flights) == 10:
        result += "\n(Showing first 10 flights)"

    return result

