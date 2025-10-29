# scripts/load_sample_data.py
from datetime import datetime
from app.model.Flight_Tracer import FlightTracer, Base
from app.core.database import engine, SessionLocal

Base.metadata.create_all(bind=engine)
db = SessionLocal()

flights = [
    FlightTracer(flight_number="AI202", airline="Lufthansa", origin="New York (JFK)", destination="Los Angeles (LAX)",
                 departure=datetime(2024, 7, 15, 10, 0), arrival=datetime(2024, 7, 15, 14, 0), ticket_price=350),
    FlightTracer(flight_number="EK317", airline="Emirates", origin="Dubai (DXB)", destination="Tokyo (HND)",
                 departure=datetime(2024, 8, 1, 9, 45), arrival=datetime(2024, 8, 1, 18, 10), ticket_price=820),
    # ... add the rest of your 10 flights here
]
db.add_all(flights)
db.commit()
db.close()
