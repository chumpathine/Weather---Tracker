import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Weather Tracker", page_icon="⛅", layout="wide")

st.title("⛅ Mokuleia Beach Park Temperature Tracker")
st.write("Live temperature readings logged automatically from the Open-Meteo API.")

# Load the data from your repo
df = pd.read_csv("daily_log.csv", skipinitialspace=True)
df["datetime"] = pd.to_datetime(df["time"])
df = df.sort_values("datetime")

# Find the hottest and coldest readings
max_idx = df["temp_f"].idxmax()
min_idx = df["temp_f"].idxmin()

# Quick numbers at the top
col1, col2, col3 = st.columns(3)
col1.metric("Latest temp", f"{df['temp_f'].iloc[-1]} F")
col2.metric("Highest", f"{df.loc[max_idx, 'temp_f']} F")
col3.metric("Lowest", f"{df.loc[min_idx, 'temp_f']} F")

# Build the chart (same idea as in weather.py)
fig = go.Figure()
fig.add_scatter(
    x=df["datetime"], y=df["temp_f"],
    mode="lines+markers", name="Temp (F)"
)
fig.add_scatter(
    x=[df.loc[max_idx, "datetime"]], y=[df.loc[max_idx, "temp_f"]],
    mode="markers+text",
    marker=dict(color="red", size=14, symbol="star"),
    text=[f"Max: {round(df.loc[max_idx, 'temp_f'], 1)}F"],
    textposition="top right", name="Max"
)
fig.add_scatter(
    x=[df.loc[min_idx, "datetime"]], y=[df.loc[min_idx, "temp_f"]],
    mode="markers+text",
    marker=dict(color="royalblue", size=14, symbol="star"),
    text=[f"Min: {round(df.loc[min_idx, 'temp_f'], 1)}F"],
    textposition="bottom right", name="Min"
)

st.plotly_chart(fig, use_container_width=True)