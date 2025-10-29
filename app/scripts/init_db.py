from app.core.database import engine, Base
from app.model.Flight_Tracer import FlightTracer

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully!")
