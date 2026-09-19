import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# 1. Authentic Template Page Setup
st.set_page_config(page_title="Sri's Tech Pulse - Controller Layout", layout="wide", page_icon="🛩️")

# Pure White Modern Grid Minimalist Styling to perfectly match the blogger mockup look
st.markdown("""
    <style>
    .reportview-container { background: #fafafa; }
    .status-panel { padding: 18px; border-radius: 6px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .status-normal { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .status-warning { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
    .status-critical { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .metric-card { background: #ffffff; padding: 15px; border-radius: 6px; border: 1px solid #e0e0e0; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 2. Extract Data Assets
try:
    df = pd.read_csv("flight_data.csv")
    df.columns = df.columns.str.strip()
except FileNotFoundError:
    st.error("🚨 'flight_data.csv' array stream error!")
    st.stop()

latest = df.iloc[-1]
alt_now = latest.get('Altitude', 0.0)
acc_now = latest.get('Accel', 0.0)
bat_now = latest.get('Battery', 0.0)

# 3. Dedicated Status Decider Engine
def calculate_status_bounds(value, sensor_name):
    if sensor_name == "Altitude":
        if value > 120.0 or value < 0.5: return "CRITICAL", "status-critical", "🔴 CRITICAL - Abnormal Altitude Bounds Fault"
        elif value > 110.0: return "WARNING", "status-warning", "🟡 WARNING - High Ceiling Fluctuations Detected"
        return "NORMAL", "status-normal", "🟢 NORMAL - Altitude System Matrix Optimal"
    elif sensor_name == "Acceleration":
        if value > 20.0: return "CRITICAL", "status-critical", "🔴 CRITICAL - Excessive G-Force Impact Shock"
        elif value > 5.0: return "WARNING", "status-warning", "🟡 WARNING - Instability & Vibrations Present"
        return "NORMAL", "status-normal", "🟢 NORMAL - Inertial Axis Alignment Stable"
    elif sensor_name == "Voltage":
        if value < 7.2: return "CRITICAL", "status-critical", "🔴 CRITICAL - Battery Brownout / Failure Cutoff"
        elif value < 7.5: return "WARNING", "status-warning", "🟡 WARNING - Power Reserve Discharging Fast"
        return "NORMAL", "status-normal", "🟢 NORMAL - DC Bus Voltage Normal"
    return "UNKNOWN", "status-normal", "⚪ Status Context Null"

st.title("📊 Sri's Tech Pulse")
st.markdown("#### Embedded Flight Parameter Controller Monitoring Platform")

# 4. Global Sensor Status Cards Block Row (Displays everything at a single glance)
st.markdown("### 🖥️ Real-time Sensor Status Row Highlights")
s_col1, s_col2, s_col3 = st.columns(3)

with s_col1:
    _, c_class, msg = calculate_status_bounds(alt_now, "Altitude")
    st.markdown(f"<div class='status-panel {c_class}'><b>Altitude State:</b><br>{msg}<br>Value: {alt_now} m</div>", unsafe_allow_html=True)
with s_col2:
    _, c_class, msg = calculate_status_bounds(acc_now, "Acceleration")
    st.markdown(f"<div class='status-panel {c_class}'><b>Acceleration State:</b><br>{msg}<br>Value: {acc_now} m/s²</div>", unsafe_allow_html=True)
with s_col3:
    _, c_class, msg = calculate_status_bounds(bat_now, "Voltage")
    st.markdown(f"<div class='status-panel {c_class}'><b>Battery State:</b><br>{msg}<br>Value: {bat_now} V</div>", unsafe_allow_html=True)

st.markdown("---")

# 5. Professional Blogger Integrated Menu Navigation Bar Layout
selected_view = option_menu(
    menu_title=None,
    options=["Altitude Deep Analysis Only", "Acceleration Tracking Only", "Voltage Telemetry Only"],
    icons=["cloud-lightning", "activity", "battery-charging"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"background-color": "#ffffff", "border": "1px solid #e0e0e0", "padding": "0!important"},
        "nav-link": {"font-size": "14px", "color": "#555", "--hover-color": "#f8f9fa"},
        "nav-link-selected": {"background-color": "#000000", "color": "#ffffff", "font-weight": "600"}
    }
)

# 6. Extrema Peak Detection Rendering Core Engine
def display_extrema_plot(metric_key, chart_title, symbol_units):
    max_idx = df[metric_key].idxmax()
    min_idx = df[metric_key].idxmin()
    
    mx_val, mx_time = df.loc[max_idx, metric_key], df.loc[max_idx, 'Time']
    mn_val, mn_time = df.loc[min_idx, metric_key], df.loc[min_idx, 'Time']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Time'], y=df[metric_key], mode='lines', name='Trajectory', line=dict(color='#000000', width=2.5)))
    
    # 🔺 Absolute Peak Highlight
    fig.add_trace(go.Scatter(
        x=[mx_time], y=[mx_val], mode='markers+text', name='Max Peak',
        text=[f"🔺 Max: {mx_val} {symbol_units}"], textposition="top center",
        marker=dict(color='#dc3545', size=13, symbol='circle')
    ))
    
    # 🔻 Absolute Min Highlight
    fig.add_trace(go.Scatter(
        x=[mn_time], y=[mn_val], mode='markers+text', name='Min Valley',
        text=[f"🔻 Min: {mn_val} {symbol_units}"], textposition="bottom center",
        marker=dict(color='#28a745', size=13, symbol='circle')
    ))
    
    fig.update_layout(
        title=chart_title, xaxis_title="Time Frame Vector (s)", yaxis_title=f"{metric_key} ({symbol_units})",
        plot_bgcolor='#ffffff', margin=dict(l=15, r=15, t=40, b=15), hovermode="x unified"
    )
    fig.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig, use_container_width=True)

# 7. Isolated Split Selection Logic
if selected_view == "Altitude Deep Analysis Only":
    st.subheader("📋 Segmented Isolation Vector: Barometric Altitude")
    display_extrema_plot('Altitude', "BMP280 Isolated Real-time Altitude Flight Vector", "m")

elif selected_view == "Acceleration Tracking Only":
    st.subheader("📋 Segmented Isolation Vector: IMU Motion Forces")
    display_extrema_plot('Accel', "MPU6050 Motion Force Inertial Spectrum Curves", "m/s²")

elif selected_view == "Voltage Telemetry Only":
    st.subheader("📋 Segmented Isolation Vector: Main Power Grid")
    display_extrema_plot('Battery', "Lithium Pack Discharge Metrics Analytics", "V")
