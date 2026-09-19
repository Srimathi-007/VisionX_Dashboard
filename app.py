import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Team VisionX Dashboard", layout="wide")
st.title("🛩️ Team VisionX - Flight Data Logger")
st.subheader("Precision In Every Parameter, Clarity In Every Flight")

uploaded_file = st.file_uploader("Upload Flight Log (.csv file)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Max Altitude", value=f"{df['Altitude'].max() if 'Altitude' in df.columns else 0} m")
    with col2:
        st.metric(label="Peak Accel", value=f"{df['Accel'].max() if 'Accel' in df.columns else 0} m/s²")
    with col3:
        st.metric(label="Min Battery", value=f"{df['Battery'].min() if 'Battery' in df.columns else 0} V")

    st.markdown("---")
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        if 'Time' in df.columns and 'Accel' in df.columns:
            st.plotly_chart(px.line(df, x='Time', y='Accel', title='Acceleration (m/s²)'), use_container_width=True)
    with chart_col2:
        if 'Time' in df.columns and 'Altitude' in df.columns:
            st.plotly_chart(px.line(df, x='Time', y='Altitude', title='Altitude (m)'), use_container_width=True)
    
    st.dataframe(df, use_container_width=True)
else:
    st.info("💡 Please upload your flight CSV file.")
