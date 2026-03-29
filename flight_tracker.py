import requests
import sqlite3
import time
from datetime import datetime

# DATABASE
conn = sqlite3.connect("flights.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    icao24 TEXT,
    callsign TEXT,
    latitude REAL,
    longitude REAL,
    altitude REAL,
    timestamp TEXT
)
""")
conn.commit()

# PERAK BOUNDARY
LAT_MIN, LAT_MAX = 3.5, 5.5
LON_MIN, LON_MAX = 100.0, 101.5

def fetch_flights():
    url = "https://opensky-network.org/api/states/all"
    try:
        res = requests.get(url)
        data = res.json()
        return data.get("states", [])
    except:
        return []

def filter_perak(states):
    result = []
    for s in states:
        lat, lon = s[6], s[5]
        if lat and lon:
            if LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX:
                result.append(s)
    return result

def save_data(flights):
    for f in flights:
        cursor.execute("""
        INSERT INTO flights (icao24, callsign, latitude, longitude, altitude, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            f[0],
            f[1].strip() if f[1] else "N/A",
            f[6],
            f[5],
            f[7],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
    conn.commit()

print("Running flight tracker...")

while True:
    states = fetch_flights()
    perak = filter_perak(states)

    print(f"Flights found: {len(perak)}")

    save_data(perak)

    time.sleep(60)