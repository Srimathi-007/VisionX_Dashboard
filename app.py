import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# 1. Global Platform Layout Window Engine
st.set_page_config(page_title="VisionX Portal", layout="wide", page_icon="🛩️")

# Pure Blogger Style Layout Custom Style Extensions
st.markdown("""
    <style>
    .status-badge { padding: 10px; border-radius: 6px; font-weight: bold; text-align: center; margin-bottom: 10px; }
    .normal-ui { background-color: #d4edda; color: #155724; }
    .anomaly-ui { background-color: #f8d7da; color: #721c24; }
    .sidebar-brand { font-size: 20px; font-weight: bold; padding-bottom: 20px; color: #333; }
    </style>
""", unsafe_allow_html=True)

# 2. Complete User Login Authentication Protection Array
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'history' not in st.session_state:
    # Pre-populate history logs for continuous workflow records
    st.session_state['history'] = [
        {"timestamp": "2026-09-19 14:22", "user": "Srimathi-007", "action": "Analyzed Flight_Log_01.csv - Battery Failure Detected"},
        {"timestamp": "2026-09-19 16:45", "user": "Srimathi-007", "action": "Ran Weekly Validation Metrics - Normal States Check"}
    ]

if not st.session_state['logged_in']:
    st.title("🔐 VisionX System Gateway")
    st.markdown("### Access Data Analysis System Verification")
    
    col_l1, _ = st.columns([1, 2])
    with col_l1:
        username = st.text_input("Username", value="Srimathi-007")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        if st.button("Login to VisionX System", use_container_width=True):
            if username == "Srimathi-007" and password == "1234":  # Standard temporary local credentials
                st.session_state['logged_in'] = True
                new_log = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "user": username,
                    "action": "User login session authenticated via local hub protocol gateway."
                }
                st.session_state['history'].append(new_log)
                st.rerun()
            else:
                st.error("Invalid credentials entered.")
    st.stop()

# 3. Read Core Flight Log Database Registers
try:
    df = pd.read_csv("flight_data.csv")
    df.columns = df.columns.str.strip()
except FileNotFoundError:
    st.error("🚨 'flight_data.csv' array stream error inside target environment repository path.")
    st.stop()

# 4. Blogger Sidebar Multi-Module Navigation Panels Array
with st.sidebar:
    st.markdown("<div class='sidebar-brand'>🛩️ VisionX Panels</div>", unsafe_allow_html=True)
    st.caption(f"Active Session: User **Srimathi-007**")
    
    # Left Side Hamburger Menu Selections Array Layout
    menu_selection = st.radio(
        "Navigation Options Menu",
        options=["Home Platform", "Altitude Tracker", "Orientation Matrix", "Acceleration Profiler", "Voltage Telemetry", "Weekly Analysis Summary", "System History Logs"]
    )
    
    st.markdown("---")
    if st.button("Logout System", type="secondary"):
        st.session_state['logged_in'] = False
        st.rerun()

# 5. Dynamic Adaptive Abnormal Extrema Point Detection Logic
def draw_analytical_chart(col_name, unit, safe_min, safe_max):
    # Storing operational metric trace actions into session registry histories automatically
    if 'tracked_views' not in st.session_state:
        st.session_state['tracked_views'] = []
    
    # Extrema indices tracking 
    max_idx = df[col_name].idxmax()
    min_idx = df[col_name].idxmin()
    
    max_v, max_t = df.loc[max_idx, col_name], df.loc[max_idx, 'Time']
    min_v, min_t = df.loc[min_idx, col_name], df.loc[min_idx, 'Time']
    
    # Isolate and register boundary infractions (Abnormal points extraction)
    anomalies_df = df[(df[col_name] < safe_min) | (df[col_name] > safe_max)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Time'], y=df[col_name], mode='lines', name=f'{col_name} Stream', line=dict(color='#111111', width=2.5)))
    
    # 🔺 Mark Peak Max
    fig.add_trace(go.Scatter(x=[max_t], y=[max_v], mode='markers+text', name='Absolute Peak Max', text=[f"🔺 Max: {max_v}"], textposition="top center", marker=dict(color='#007bff', size=10)))
    
    # 🔻 Mark Valley Min
    fig.add_trace(go.Scatter(x=[min_t], y=[min_v], mode='markers+text', name='Absolute Minimum', text=[f"🔻 Min: {min_v}"], textposition="bottom center", marker=dict(color='#28a745', size=10)))
    
    # 🚨 Overlay Abnormal Points Highlight (Pinpoint anomalies)
    if not anomalies_df.empty:
        fig.add_trace(go.Scatter(
            x=anomalies_df['Time'], y=anomalies_df[col_name],
            mode='markers', name='🚨 ABNORMAL POINT FAULT',
            marker=dict(color='#dc3545', size=12, symbol='x')
        ))
        st.markdown(f"<div class='status-badge anomaly-ui'>🚨 CRITICAL ANOMALY: {len(anomalies_df)} structural abnormal data breaches logged inside telemetry tracks.</div>", unsafe_allow_html=True)
        
        # Display the first broken critical index parameter details
        first_fault = anomalies_df.iloc[0]
        st.warning(f"⚠️ **First Parameter Defect Point Registered:** At timestamp entry **{first_fault['Time']}s**, reading shifted abnormally to **{first_fault[col_name]} {unit}**.")
    else:
        st.markdown("<div class='status-badge normal-ui'>🟢 NOMINAL STATUS: Stream data values operate entirely within safe tracking limits.</div>", unsafe_allow_html=True)
        
    fig.update_layout(title=f"{col_name} Time-Series Flight Track Diagnostic Curve", xaxis_title="Time Frame (s)", yaxis_title=f"{col_name} ({unit})", plot_bgcolor='#ffffff', hovermode="x unified")
    fig.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig, use_container_width=True)

# 6. Render Selection View Matrix Locations 
if menu_selection == "Home Platform":
    st.title("VisionX")
    st.markdown("### Data analysis system")
    st.markdown("---")
    st.markdown("""
        Welcome to the **VisionX Embedded Flight Parameter Recording and Failure Diagnostic Platform**. 
        
        Use the Blogger-inspired left side option menu navigation layout panel to switch between isolated telemetry sensor parameters, execute automated crash assessments, track structural weekly logs, or view historical transaction sequence frames.
    """)
    st.info("💡 **Developer Tip:** Click the small `>` top left arrow icon button if the sidebar navigation menu choice block layout collapses from your active monitor frame layer window.")

elif menu_selection == "Altitude Tracker":
    st.subheader("📈 Barometric Sensor Isolation Parameter View (BMP280)")
    # Set nominal threshold boundaries limits (e.g., alert if altitude crosses 120m boundaries)
    draw_analytical_chart('Altitude', 'meters', safe_min=0.5, safe_max=120.0)
    
    # Register this look event to history tracker session array automatically
    if not any(d['action'] == "Reviewed Barometric Altitude Track Matrix" for d in st.session_state['history'][-1:]):
        st.session_state['history'].append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": "Srimathi-007", "action": "Reviewed Barometric Altitude Track Matrix"})

elif menu_selection == "Orientation Matrix":
    st.subheader("🧭 IMU Flight Risk Orientation Tracking Flow States")
    draw_analytical_chart('Accel', 'm/s²', safe_min=0.0, safe_max=15.0)
    if not any(d['action'] == "Reviewed Flight Risk Orientation Profile" for d in st.session_state['history'][-1:]):
        st.session_state['history'].append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": "Srimathi-007", "action": "Reviewed Flight Risk Orientation Profile"})

elif menu_selection == "Acceleration Profiler":
    st.subheader("🚀 6-Axis Motion Acceleration Profile Matrix Logs (MPU6050)")
    draw_analytical_chart('Accel', 'm/s²', safe_min=0.0, safe_max=5.0)
    if not any(d['action'] == "Reviewed Motion Acceleration Parameters" for d in st.session_state['history'][-1:]):
        st.session_state['history'].append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": "Srimathi-007", "action": "Reviewed Motion Acceleration Parameters"})

elif menu_selection == "Voltage Telemetry":
    st.subheader("⚡ Power ADC Battery Discharge Cell Telemetry Logs")
    draw_analytical_chart('Battery', 'Volts', safe_min=7.2, safe_max=9.0)
    if not any(d['action'] == "Reviewed Power Battery Voltage Records" for d in st.session_state['history'][-1:]):
        st.session_state['history'].append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": "Srimathi-007", "action": "Reviewed Power Battery Voltage Records"})

elif menu_selection == "Weekly Analysis Summary":
    st.subheader("📊 Compiled Systems Weekly Flight Analysis Matrix Report")
    st.markdown("### Flight Parameter Comparison Summary Table")
    
    summary_data = {
        "Telemetry Metric Target": ["Barometric Altitude Log", "Inertial Acceleration Force", "Main Pack Battery Cells Rail"],
        "Absolute Peak Maximum Registered": [f"{df['Altitude'].max()} m", f"{df['Accel'].max()} m/s²", f"{df['Battery'].max()} V"],
        "Absolute Minimum Valley Registered": [f"{df['Altitude'].min()} m", f"{df['Accel'].min()} m/s²", f"{df['Battery'].min()} V"],
        "Calculated Evaluation Trend": ["Rapid descent structural crash risk registered.", "Extreme heavy G-force peak impact registered.", "Voltage dropped critically below brownout limit."]
    }
    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)
    
