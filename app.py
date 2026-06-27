import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Weather Tracker", page_icon="⛅", layout="wide")

st.title("My City Temperature Dashboard")

# Load the data from your repo
df = pd.read_csv("daily_log.csv", skipinitialspace=True)
df["datetime"] = pd.to_datetime(df["time"])
df = df.sort_values("datetime")
# Drop exact duplicate readings left over from the old double-logging bug
df = df.drop_duplicates(subset=["datetime", "temp_f"]).reset_index(drop=True)

# Find the hottest and coldest readings
max_idx = df["temp_f"].idxmax()
min_idx = df["temp_f"].idxmin()

# --- Feature 1: key readings (unchanged) ---
col1, col2, col3 = st.columns(3)
col1.metric("Latest temp", f"{df['temp_f'].iloc[-1]} F")
col2.metric("Highest", f"{df.loc[max_idx, 'temp_f']} F")
col3.metric("Lowest", f"{df.loc[min_idx, 'temp_f']} F")

st.divider()

# --- Feature 2: alert thresholds ---
st.subheader("Alert Thresholds")
col_hot, col_cold = st.columns(2)
hot_threshold = col_hot.slider("Hot alert (F)", min_value=60, max_value=110, value=90)
cold_threshold = col_cold.slider("Cold alert (F)", min_value=20, max_value=65, value=45)

latest_temp = df["temp_f"].iloc[-1]
if latest_temp >= hot_threshold:
    st.error(f"🔥 Heat alert: latest reading {latest_temp}F is at or above your {hot_threshold}F limit.")
elif latest_temp <= cold_threshold:
    st.warning(f"❄️ Cold alert: latest reading {latest_temp}F is at or below your {cold_threshold}F limit.")
else:
    st.success(f"✅ Latest reading {latest_temp}F is within your {cold_threshold}F–{hot_threshold}F range.")

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

# Draw the alert thresholds as dashed lines on the chart
fig.add_hline(
    y=hot_threshold, line_dash="dash", line_color="red",
    annotation_text=f"Hot: {hot_threshold}F", annotation_position="top right"
)
fig.add_hline(
    y=cold_threshold, line_dash="dash", line_color="royalblue",
    annotation_text=f"Cold: {cold_threshold}F", annotation_position="bottom right"
)

fig.update_layout(xaxis_title="Date / Time", yaxis_title="Temperature (F)")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Feature 3: incoming data log (Celsius + Fahrenheit) ---
st.subheader("Incoming Data Log")
log = df.sort_values("datetime", ascending=False).copy()
log["Date / Time"] = log["datetime"].dt.strftime("%b %d, %Y %H:%M")
log = log.rename(columns={"temperature_2m": "Temp (C)", "temp_f": "Temp (F)"})
log = log[["Date / Time", "Temp (C)", "Temp (F)"]]
st.dataframe(log, use_container_width=True, hide_index=True)
