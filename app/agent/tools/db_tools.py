import sqlite3

def fetch_flight_data():

    conn = sqlite3.connect("flight_update.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Flight_Tracer")
    rows = cursor.fetchall()

    conn.close()
    return rows
