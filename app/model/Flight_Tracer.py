from sqlalchemy import Column, Integer

from app.schema.chat import MessageRequestSchema


class FlightTracer:
    __tablename__ = "flight_tracer"

    id = Column(Integer, primary_key=True)

