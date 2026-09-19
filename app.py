import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# 1. Page Global Setup
st.set_page_config(page_title="VisionX - Flight Control", layout="wide", page_icon="🛩️")

# Custom Status Box Colors Style Configuration
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e0e0e0; }
    .status-box { padding: 20px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 8px solid; }
    .status-normal { background-color: #d4edda; color: #155724; border-color: #28a745; }
    .status-warning { background-color: #fff3cd; color: #856404; border-color: #ffc107; }
    .status-critical { background-color: #f8d7da; color: #721c24; border-color: #dc3545; }
    </style>
""", unsafe_allow_html=True)

# 2. Read Flight Log Safely
try:
    df = pd.read_csv("flight_data.csv")
    df.columns = df.columns.str.strip()
except FileNotFoundError:
    st.error("🚨 'flight_data.csv' file missing inside repository!")
    st.stop()

# Extract essential telemetry limits parameters
latest_row = df.iloc[-1]
alt_val = latest_row.get('Altitude', 0.0)
acc_val = latest_row.get('Accel', 0.0)
bat_val = latest_row.get('Battery', 0.0)

# 3. Dynamic Threshold Status Check Generator Function
def get_status_meta(val, metric_type):
    if metric_type == "Altitude":
        if val > 120.0: return "CRITICAL", "status-critical", "🔴 CRITICAL DESCENT / CEILING BREAKED"
        elif val > 110.0: return "WARNING", "status-warning", "🟡 WARNING - Approaching Extreme Alt Bound"
        return "NORMAL", "status-normal", "🟢 NORMAL - Safe Barometric Altitude Operational Zone"
        
    elif metric_type == "Acceleration":
        if val > 20.0: return "CRITICAL", "status-critical", "🔴 CRITICAL IMPACT / HIGH FORCE DETECTED"
        elif val > 5.0: return "WARNING", "status-warning", "🟡 WARNING - High G-Force Vibration Anomalies"
        return "NORMAL", "status-normal", "🟢 NORMAL - Stable IMU Axis Orientations"
        
    elif metric_type == "Voltage":
        if val < 7.2: return "CRITICAL", "status-critical", "🔴 CRITICAL BROWNOUT / BATT DEPLETION STAGE"
        elif val < 7.5: return "WARNING", "status-warning", "🟡 WARNING - Battery Charging Discharge State"
        return "NORMAL", "status-normal", "🟢 NORMAL - Power Rail System Stable"
    return "UNKNOWN", "status-normal", "⚪ NO CONTEXT LOGGED"

# 4. Blogger-Inspired Top Navigation Menubar (Allows individual selection check)
st.title("🛩️ Team VisionX - Flight Log Controller Platform")
st.markdown("### VisionX - Modular Sensor Data Analyzer")

selected_metric = option_menu(
    menu_title=None, 
    options=["Altitude Analytics Only", "Acceleration Analytics Only", "Battery Voltage Analytics Only"], 
    icons=["cloud-arrow-up", "speedometer2", "lightning-charge"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#ffffff", "border-radius": "5px", "box-shadow": "0 1px 3px rgba(0,0,0,0.1)"},
        "icon": {"color": "#ffaa00", "font-size": "18px"}, 
        "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "color": "#333", "--hover-color": "#f1f1f1"},
        "nav-link-selected": {"background-color": "#111111", "color": "#ffffff", "font-weight": "bold"},
    }
)

# 5. Shared Reusable Graph Extrema Plotter with Highlights Bounds
def draw_extrema_chart(col_name, label_title, unit_symbol):
    max_idx = df[col_name].idxmax()
    min_idx = df[col_name].idxmin()
    
    max_v, max_t = df.loc[max_idx, col_name], df.loc[max_idx, 'Time']
    min_v, min_t = df.loc[min_idx, col_name], df.loc[min_idx, 'Time']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Time'], y=df[col_name], mode='lines', name=col_name, line=dict(color='#111111', width=3)))
    
    # 🔺 Peak Point Highlight
    fig.add_trace(go.Scatter(
        x=[max_t], y=[max_v], mode='markers+text', name='Max Peak',
        text=[f"🔺 Peak Max: {max_v}{unit_symbol}"], textposition="top center",
        marker=dict(color='#dc3545', size=14, symbol='circle')
    ))
    
    # 🔻 Valley Minimum Highlight
    fig.add_trace(go.Scatter(
        x=[min_t], y=[min_v], mode='markers+text', name='Min Valley',
        text=[f"🔻 Minimum: {min_v}{unit_symbol}"], textposition="bottom center",
        marker=dict(color='#28a745', size=14, symbol='circle')
    ))
    
    fig.update_layout(
        title=label_title, xaxis_title="Time (seconds)", yaxis_title=f"{col_name} ({unit_symbol})",
        hovermode="x unified", margin=dict(l=20, r=20, t=50, b=20), plot_bgcolor='#fafafa'
    )
    st.plotly_chart(fig, use_container_width=True)

# 6. Render Segmented View Layout blocks based on Menu Select Actions
st.markdown("---")

if selected_metric == "Altitude Analytics Only":
    status_type, css_class, message = get_status_meta(alt_val, "Altitude")
    
    st.markdown(f"""
        <div class="status-box {css_class}">
            <h3 style="margin:0; font-weight:bold;">{message}</h3>
            <p style="margin:5px 0 0 0;">Current Registered Reading: <b>{alt_val} meters</b> | Target Source: BMP280 Barometer Array</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display specialized isolated graphic logs vector
    draw_extrema_chart('Altitude', "BMP280 Isolated Flight Altitude Trajectory Vector", "m")

elif selected_metric == "Acceleration Analytics Only":
    status_type, css_class, message = get_status_meta(acc_val, "Acceleration")
    
    st.markdown(f"""
        <div class="status-box {css_class}">
            <h3 style="margin:0; font-weight:bold;">{message}</h3>
            <p style="margin:5px 0 0 0;">Current Registered Reading: <b>{acc_val} m/s²</b> | Target Source: MPU6050 6-Axis Inertial Block</p>
        </div>
    """, unsafe_allow_html=True)
    
    draw_extrema_chart('Accel', "MPU6050 Acceleration Load Vector Analysis", "m/s²")

elif selected_metric == "Battery Voltage Analytics Only":
    status_type, css_class, message = get_status_meta(bat_val, "Voltage")
    
    st.markdown(f"""
        <div class="status-box {css_class}">
            <h3 style="margin:0; font-weight:bold;">{message}</h3>
            <p style="margin:5px 0 0 0;">Current Registered Reading: <b>{bat_val} Volts</b> | Target Source: ADC Battery Sensor Rail</p>
        </div>
    """, unsafe_allow_html=True)
    
    draw_extrema_chart('Battery', "Power Cells Discharge Curve & System Logging Diagnostics", "V")

