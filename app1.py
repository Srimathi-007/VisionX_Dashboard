"""
VisionX: Crash-Safe UAV Flight Data Logger & Telemetry Dashboard
Target Hardware: STM32 MCU + Dual FRAM (Blackbox Buffer) + MicroSD Card Storage
Designed for Streamlit Community Cloud & Production Ground Station Operations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timezone, timedelta
import requests
import time
import json
import math

# -----------------------------------------------------------------------------
# 1. THRESHOLD CONFIGURATION (Easily tuneable flight safety bounds)
# -----------------------------------------------------------------------------
THRESHOLDS = {
    # Acceleration Magnitude Thresholds (|a| = sqrt(x^2 + y^2 + z^2)) in G's
    "accel_caution_g": 2.5,
    "accel_critical_g": 4.0,

    # Battery Voltage Thresholds (Volts) for 1S/regulated cell monitoring
    "battery_caution_v": 3.5,
    "battery_critical_v": 3.3,

    # Altitude Descent / Drop Rate Thresholds (m/s)
    "alt_drop_caution_mps": 3.0,
    "alt_drop_critical_mps": 6.0,

    # Crash determination: Number of consecutive CRITICAL samples required
    "crash_consecutive_critical_samples": 3,

    # Pre-event blackbox extraction window (seconds)
    "crash_window_seconds": 10.0,

    # Nominal flight reference values
    "nominal_voltage": 3.8,
    "nominal_accel_z": 1.0,  # 1G gravity
}

# -----------------------------------------------------------------------------
# 2. STREAMLIT PAGE CONFIGURATION & INLINE STYLES
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VisionX | UAV Flight Data Logger",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom High-Contrast Tactical Dark Theme CSS
st.markdown("""
<style>
    .stApp { background-color: #0B0F17; color: #F1F5F9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .visionx-header { text-align: center; padding: 0.5rem 0 1.25rem 0; border-bottom: 1px solid #1E293B; margin-bottom: 1.5rem; }
    .visionx-title { font-size: 2.2rem; font-weight: 800; letter-spacing: 0.08em; color: #38BDF8; margin: 0; text-transform: uppercase; }
    .visionx-subtitle { color: #94A3B8; font-size: 0.85rem; margin-top: 0.25rem; letter-spacing: 0.05em; }
    .metric-container { background-color: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 1rem 1.25rem; }
    .zone-badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 700; font-size: 0.85rem; }
    .zone-SAFE { background-color: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid #059669; }
    .zone-CAUTION { background-color: rgba(245, 158, 11, 0.2); color: #FBBF24; border: 1px solid #D97706; }
    .zone-CRITICAL { background-color: rgba(239, 68, 68, 0.25); color: #F87171; border: 1px solid #DC2626; }
    .zone-CRASH { background-color: #991B1B; color: #FFFFFF; border: 1px solid #EF4444; }
    .crash-alert-box { background: linear-gradient(135deg, #7F1D1D 0%, #450A0A 100%); border: 2px solid #EF4444; border-radius: 8px; padding: 1.25rem; color: #FFFFFF; margin-bottom: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# Full production code includes:
# - Centered st.secrets login gateway
# - Auto-refresh 1Hz live telemetry engine with Firebase REST + DEMO MODE simulation
# - Real-time metrics (Altitude, |a|, Battery, Zone) & reverse-chronological table
# - Plotly charts for Altitude Analysis, Orientation Profile, Acceleration Core, Battery Diagnostics
# - YouTube-style Flight History cards and replay scrubber
# - 10-second pre-event Crash blackbox window & full-width alert
# (See app.py in project repository)