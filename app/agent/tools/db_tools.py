from sqlalchemy import text
from langchain_core.tools import tool

from app.core.database import SessionLocal


@tool
def fetch_flight_data(sql_query: str) -> str:
    """
    Execute the provided SQL query to fetch flight data from the database.

    Args:
        sql_query (str): The SQL query string to be executed.

    Returns:
        str: Query results as a string, or an error message if something goes wrong.
    """
    db = SessionLocal()
    try:
        result = db.execute(text(sql_query))
        rows = result.fetchall()

        if not rows:
            return "No data found."

        # Convert result rows to list of dictionaries
        columns = result.keys()
        data = [dict(zip(columns, row)) for row in rows]

        return str(data)

    except Exception as e:
        return f"Database error: {str(e)}"

    finally:
        db.close()
