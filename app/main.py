import uvicorn
from fastapi import FastAPI

from app.api import chat
from app.core.database import engine, Base
from app.model.Flight_Tracer import FlightTracer

app = FastAPI(docs_url="/docs")
app.include_router(chat.router)


Base.metadata.create_all(bind=engine)

def main():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
