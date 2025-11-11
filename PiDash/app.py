import streamlit as st
import datetime
from utils.weather import get_weather
from utils.get_l_train_alerts import get_l_train_alerts
from utils.get_l_train_arrivals import get_l_train_arrivals
from streamlit_autorefresh import st_autorefresh
import time

# ---- Page Config ----
st.set_page_config(
    page_title="4B Dashboard",
    page_icon="📊",
    layout="wide",
)

# ---- Auto Refresh Every 30s ----
count = st_autorefresh(interval=30 * 1000, key="datarefresh")

# ---- Top Bar ----
st.title("4B")
st.caption(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# ---- Split Page into Two Columns ----
col1, col2 = st.columns(2)

# ================================================================
# LEFT COLUMN: WEATHER
# ================================================================
with col1:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    st.markdown(
    f"""
    <div style='text-align: center;'>
        <h1>🕒 {current_time}</h1>
    </div>
    """,
    unsafe_allow_html=True
)
    st.header("🌤 Outdoor Weather (Bushwick)")
    lat, lon = 40.7128, -74.0060

    with st.spinner("Fetching weather data..."):
        data = get_weather(lat, lon)

    if data:
        st.success(f"**{data['name']}**: {data['shortForecast']}")
        st.markdown(
            f"""
            <div style='display: flex; justify-content: space-between;
                        border: 1px solid #ddd; border-radius: 10px;
                        padding: 10px; margin-bottom: 10px;'>
                <div style='flex: 1; margin-right: 10px;'>
                    <h3>Temperature</h3>
                    <p style='font-size:18px;'>{data['temperature']} °{data['unit']}</p>
                </div>
                <div style='flex: 1; margin-left: 10px;'>
                    <h3>Wind</h3>
                    <p style='font-size:18px;'>{data['windSpeed']}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.info(data["detailedForecast"])
    else:
        st.error("Failed to load weather data.")

# ================================================================
# RIGHT COLUMN: L TRAIN
# ================================================================
with col2:
    st.header("🚇 L Train @ Jefferson St")

    # Fetch alerts and arrival data
    alerts = get_l_train_alerts()
    arrivals = get_l_train_arrivals(["L15N", "L15S"])

    # ---- Alerts ----
    st.subheader("🚨 Alerts")
    if alerts:
        for a in alerts:
            st.warning(a)
    else:
        st.success("No current alerts for L train.")

    # ---- Arrivals in Two Columns ----
    up_col, down_col = st.columns(2)

    with up_col:
        st.subheader("⬆ To 8 Av")
        northbound = arrivals.get("L15N", [])[:3]
        if northbound:
            for arrival in northbound:
                st.markdown(
                    f"""
                    <div style='border: 1px solid #ddd; border-radius: 10px;
                                padding: 10px; margin-bottom: 10px;
                                '>
                        <h4 style='margin:0;'>Departs In: {arrival['minutes']} min</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.write("No data")

    with down_col:
        st.subheader("⬇ To Canarsie")
        southbound = arrivals.get("L15S", [])[:3]
        if southbound:
            for arrival in southbound:
                st.markdown(
                    f"""
                    <div style='border: 1px solid #ddd; border-radius: 10px;
                                padding: 10px; margin-bottom: 10px;
                                '>
                        <h4 style='margin:0;'>Departs In: {arrival['minutes']} min</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.write("No data")
