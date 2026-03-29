import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# CONNECT DATABASE
conn = sqlite3.connect("flights.db")

st.title("✈️ Flight Monitoring System (Perak)")

# LOAD DATA
df = pd.read_sql_query("SELECT * FROM flights", conn)

if df.empty:
    st.warning("No data available yet. Run flight_tracker.py first.")
else:
    st.subheader("Raw Data")
    st.dataframe(df.tail(50))

    # =========================
    # FLIGHTS OVER TIME
    # =========================
    st.subheader("📈 Flights Over Time")

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    flights_per_time = df.groupby(df['timestamp'].dt.hour).size()

    fig1, ax1 = plt.subplots()
    ax1.plot(flights_per_time.index, flights_per_time.values)
    ax1.set_xlabel("Hour")
    ax1.set_ylabel("Number of Flights")

    st.pyplot(fig1)

    # =========================
    # ALTITUDE DISTRIBUTION
    # =========================
    st.subheader("📊 Altitude Distribution")

    fig2, ax2 = plt.subplots()
    ax2.hist(df['altitude'].dropna(), bins=20)
    ax2.set_xlabel("Altitude")
    ax2.set_ylabel("Frequency")

    st.pyplot(fig2)

    # =========================
    # MAP VISUALIZATION
    # =========================
    st.subheader("🗺️ Aircraft Locations")

    map_data = df[['latitude', 'longitude']].dropna()
    st.map(map_data)