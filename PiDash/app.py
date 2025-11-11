import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# Import utility functions
from utils.weather import get_weather, fahrenheit_to_celsius
from utils.get_l_train_alerts import get_l_train_alerts
from utils.get_l_train_arrivals import get_l_train_arrivals

# ---- Page Config ----
st.set_page_config(
    page_title="Ebichu Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---- Custom CSS for sleek, compact design ----
st.markdown("""
<style>
    /* Remove default padding and maximize space */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        max-width: 100%;
        display: flex;
        flex-direction: column;
        height: 100vh;
    }
    
    /* Make columns flex containers */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    
    /* Flex container for sections */
    .flex-container {
        display: flex;
        flex-direction: column;
        flex: 1;
        min-height: 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Compact typography */
    h1 {
        font-size: 1.75rem !important;
        font-weight: 600 !important;
        margin: 0 0 0.25rem 0 !important;
        padding: 0 !important;
    }
    
    .stMarkdown p {
        margin-bottom: 0.5rem;
    }
    
    /* Time and date */
    .time-display {
        font-size: 3rem;
        font-weight: 200;
        line-height: 1;
        margin-bottom: 0.25rem;
    }
    
    .date-display {
        font-size: 1rem;
        opacity: 0.7;
        margin-bottom: 1.5rem;
    }
    
    .last-updated {
        font-size: 0.8rem;
        opacity: 0.5;
        margin-bottom: 1rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.8;
        border-bottom: 1px solid var(--secondary-background-color);
        padding-bottom: 0.5rem;
    }
    
    /* Weather main card */
    .weather-main {
        background-color: var(--secondary-background-color);
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
        flex-shrink: 0;
    }
    
    .temp-large {
        font-size: 3.5rem;
        font-weight: 200;
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    .weather-condition {
        font-size: 1.2rem;
        opacity: 0.85;
        margin-bottom: 0.5rem;
    }
    
    .weather-location {
        font-size: 0.85rem;
        opacity: 0.6;
    }
    
    /* Weather details grid */
    .weather-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .weather-item {
        background-color: var(--secondary-background-color);
        border-radius: 6px;
        padding: 0.75rem;
        text-align: center;
    }
    
    .weather-label {
        font-size: 0.75rem;
        opacity: 0.6;
        margin-bottom: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .weather-value {
        font-size: 1.25rem;
        font-weight: 600;
    }
    
    /* Detailed forecast */
    .forecast-detail {
        background-color: var(--secondary-background-color);
        border-radius: 6px;
        padding: 1rem;
        font-size: 0.9rem;
        line-height: 1.5;
        opacity: 0.85;
        flex: 1;
        overflow-y: auto;
        min-height: 0;
    }
    
    /* Train section */
    .train-section {
        display: flex;
        flex-direction: column;
        flex: 1;
        min-height: 0;
    }
    
    .train-arrivals {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-height: 0;
    }
    
    .train-direction {
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        opacity: 0.8;
        flex-shrink: 0;
    }
    
    /* Train arrival cards */
    .train-card {
        background-color: var(--secondary-background-color);
        border-left: 3px solid #0066CC;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .train-time {
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .train-label {
        font-size: 0.8rem;
        opacity: 0.7;
    }
    
    /* Alert styling */
    .alert-box {
        background-color: #FFF3CD;
        color: #856404;
        border-left: 3px solid #FFC107;
        border-radius: 6px;
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        font-size: 0.9rem;
    }
    
    [data-theme="dark"] .alert-box {
        background-color: #3d3416;
        color: #ffd966;
    }
    
    .no-alert {
        background-color: var(--secondary-background-color);
        border-left: 3px solid #28a745;
        border-radius: 6px;
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .no-data {
        text-align: center;
        opacity: 0.5;
        font-size: 0.85rem;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ---- Auto Refresh Every 30s ----
count = st_autorefresh(interval=30 * 1000, key="datarefresh")

# ---- Get NYC Time ----
nyc_time = datetime.datetime.now(pytz.timezone("America/New_York"))

# ---- Header ----
st.title("Ebichu")
st.markdown(f'<div class="last-updated">Last updated: {nyc_time.strftime("%B %d, %Y at %I:%M:%S %p")}</div>', unsafe_allow_html=True)

# ---- Split Page into Two Columns ----
col1, col2 = st.columns([1, 1], gap="medium")

# ================================================================
# LEFT COLUMN: TIME & WEATHER
# ================================================================
with col1:
    # Display current time
    current_time = nyc_time.strftime("%I:%M %p")
    current_date = nyc_time.strftime("%A, %B %d")
    
    st.markdown(f'<div class="time-display">{current_time}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-display">{current_date}</div>', unsafe_allow_html=True)
    
    # Weather Section
    st.markdown('<div class="section-header">Outdoor Weather</div>', unsafe_allow_html=True)
    
    lat, lon = 40.7128, -74.0060

    data = get_weather(lat, lon)

    if data:
        celsius_temp = fahrenheit_to_celsius(data['temperature'])
        
        # Main weather display
        st.markdown(f"""
        <div class="weather-main">
            <div class="temp-large">{celsius_temp:.1f}°C</div>
            <div class="weather-condition">{data['shortForecast']}</div>
            <div class="weather-location">{data['name']}</div>
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
                <div class="weather-label">Fahrenheit</div>
                <div class="weather-value">{data['temperature']}°F</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed forecast (always visible)
        st.markdown(f'<div class="forecast-detail">{data["detailedForecast"]}</div>', unsafe_allow_html=True)
    else:
        st.error("Failed to load weather data.")

# ================================================================
# RIGHT COLUMN: L TRAIN
# ================================================================
with col2:
    st.markdown('<div class="train-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">L Train at Jefferson St</div>', unsafe_allow_html=True)

    # Fetch alerts and arrival data
    alerts = get_l_train_alerts()
    arrivals = get_l_train_arrivals(["L15N", "L15S"])

    # ---- Alerts ----
    if alerts:
        for alert in alerts:
            st.markdown(f'<div class="alert-box">{alert}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="no-alert">No current service alerts</div>', unsafe_allow_html=True)

    st.markdown('<div class="train-arrivals">', unsafe_allow_html=True)
    # ---- Arrivals in Two Columns ----
    up_col, down_col = st.columns(2)

    with up_col:
        st.markdown('<div class="train-direction">To 8 Av</div>', unsafe_allow_html=True)
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
            st.markdown('<div class="no-data">No upcoming trains</div>', unsafe_allow_html=True)

    with down_col:
        st.markdown('<div class="train-direction">To Canarsie</div>', unsafe_allow_html=True)
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
            st.markdown('<div class="no-data">No upcoming trains</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close train-arrivals
    st.markdown('</div>', unsafe_allow_html=True)  # Close train-section