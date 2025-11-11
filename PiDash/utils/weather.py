import streamlit as st
import datetime
from utils.weather import get_weather
from utils.get_l_train_alerts import get_l_train_alerts
from utils.get_l_train_arrivals import get_l_train_arrivals
from streamlit_autorefresh import st_autorefresh
import pytz

# ---- Page Config ----
st.set_page_config(
    page_title="Ebichu Dashboard",
    page_icon="📊",
    layout="wide",
)

# ---- Custom CSS for sleek design ----
st.markdown("""
<style>
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Card styling that adapts to theme */
    .metric-card {
        background-color: var(--background-color);
        border: 1px solid var(--secondary-background-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Weather details grid */
    .weather-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .weather-item {
        background-color: var(--secondary-background-color);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    
    .weather-label {
        font-size: 0.85rem;
        opacity: 0.7;
        margin-bottom: 0.5rem;
    }
    
    .weather-value {
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Train arrival cards */
    .train-card {
        background: linear-gradient(135deg, var(--secondary-background-color) 0%, var(--background-color) 100%);
        border-left: 4px solid #0066CC;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .train-time {
        font-size: 1.75rem;
        font-weight: 700;
    }
    
    .train-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* Alert styling */
    .alert-box {
        background-color: #FFF3CD;
        color: #856404;
        border-left: 4px solid #FFC107;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    [data-theme="dark"] .alert-box {
        background-color: #3d3416;
        color: #ffd966;
    }
    
    /* Header styling */
    .dashboard-header {
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--secondary-background-color);
    }
    
    .time-display {
        font-size: 2.5rem;
        font-weight: 300;
        margin-bottom: 0.5rem;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ---- Auto Refresh Every 30s ----
count = st_autorefresh(interval=30 * 1000, key="datarefresh")

# ---- Get NYC Time ----
nyc_time = datetime.datetime.now(pytz.timezone("America/New_York"))

# ---- Header ----
st.markdown('<div class="dashboard-header">', unsafe_allow_html=True)
st.title("🏠 Ebichu Dashboard")
st.caption(f"Last updated: {nyc_time.strftime('%B %d, %Y at %I:%M:%S %p')}")
st.markdown('</div>', unsafe_allow_html=True)

# ---- Split Page into Two Columns ----
col1, col2 = st.columns([1, 1], gap="large")

# ================================================================
# LEFT COLUMN: WEATHER
# ================================================================
with col1:
    # Display current time
    current_time = nyc_time.strftime("%I:%M %p")
    current_date = nyc_time.strftime("%A, %B %d")
    
    st.markdown(f'<div class="time-display">{current_time}</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size: 1.1rem; opacity: 0.8; margin-bottom: 2rem;">{current_date}</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">🌤️ Outdoor Weather</div>', unsafe_allow_html=True)
    
    lat, lon = 40.7128, -74.0060

    with st.spinner("Fetching weather data..."):
        data = get_weather(lat, lon)

    if data:
        
        # Main weather card
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin-top: 0;">{data['name']}</h3>
            <div style="font-size: 3rem; font-weight: 300; margin: 1rem 0;">
                {data['temperature']:.1f}°C
            </div>
            <p style="font-size: 1.1rem; margin: 0; opacity: 0.9;">
                {data['shortForecast']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Weather details grid
        st.markdown(f"""
        <div class="weather-grid">
            <div class="weather-item">
                <div class="weather-label">Wind Speed</div>
                <div class="weather-value">{data['windSpeed']}</div>
            </div>
            <div class="weather-item">
                <div class="weather-label">Temperature</div>
                <div class="weather-value">{data['temperature']}°F</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed forecast
        with st.expander("📋 Detailed Forecast", expanded=False):
            st.write(data["detailedForecast"])
    else:
        st.error("Failed to load weather data.")

# ================================================================
# RIGHT COLUMN: L TRAIN
# ================================================================
with col2:
    st.markdown('<div class="section-header">🚇 L Train @ Jefferson St</div>', unsafe_allow_html=True)

    # Fetch alerts and arrival data
    alerts = get_l_train_alerts()
    arrivals = get_l_train_arrivals(["L15N", "L15S"])

    # ---- Alerts ----
    if alerts:
        st.markdown("**⚠️ Service Alerts**")
        for alert in alerts:
            st.markdown(f'<div class="alert-box">{alert}</div>', unsafe_allow_html=True)
    else:
        st.markdown("✅ **No current alerts**")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Arrivals in Two Columns ----
    up_col, down_col = st.columns(2)

    with up_col:
        st.markdown("**⬆️ To 8 Av**")
        northbound = arrivals.get("L15N", [])[:3]
        if northbound:
            for arrival in northbound:
                st.markdown(f"""
                <div class="train-card">
                    <div>
                        <div class="train-time">{arrival['minutes']}</div>
                        <div class="train-label">minutes</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<p style="opacity: 0.6; text-align: center;">No upcoming trains</p>', unsafe_allow_html=True)

    with down_col:
        st.markdown("**⬇️ To Canarsie**")
        southbound = arrivals.get("L15S", [])[:3]
        if southbound:
            for arrival in southbound:
                st.markdown(f"""
                <div class="train-card">
                    <div>
                        <div class="train-time">{arrival['minutes']}</div>
                        <div class="train-label">minutes</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<p style="opacity: 0.6; text-align: center;">No upcoming trains</p>', unsafe_allow_html=True)