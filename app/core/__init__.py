from app.model.Flight_Tracer import Base
from app.core.database import engine

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database setup complete!")

if __name__ == "__main__":
    init_db()
