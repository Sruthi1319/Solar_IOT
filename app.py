import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.insights import detect_anomalies, generate_tips

st.set_page_config(page_title="🔋 AI-Powered Solar IoT Energy Dashboard", layout="wide")

st.title("🧠 AI-Powered Solar IoT Energy Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("📤 Upload your Solar IoT CSV file", type=["csv"])

if uploaded_file:
    @st.cache_data
    def load_data(file):
        df = pd.read_csv(file)
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df

    data = load_data(uploaded_file)

    # Show available columns
    with st.expander("📄 Available Columns in Dataset"):
        st.write(data.columns.tolist())

    # 📈 Key Metrics
    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)

    col1.metric("🔆 Avg Power Output", f"{data['power_output_w'].mean():.2f} W")
    col2.metric("🌡️ Avg Panel Temp", f"{data['panel_temperature_c'].mean():.1f} °C")
    col3.metric("🔋 Avg Battery Level", f"{data['battery_charge_level_%'].mean():.1f} %")

    # 📅 Line Chart: Power Output Over Time
    st.subheader("📉 Power Output Over Time")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data['timestamp'], data['power_output_w'], color='orange')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Power Output (W)")
    st.pyplot(fig)

    # 🔥 Heatmap: Feature Correlations
    st.subheader("🔍 Feature Correlation Heatmap")
    fig2, ax2 = plt.subplots()
    sns.heatmap(data.corr(numeric_only=True), annot=True, cmap="YlOrBr", ax=ax2)
    st.pyplot(fig2)

    # 🚨 Anomaly Detection
    st.subheader("🚨 Detected Anomalies")
    anomalies = detect_anomalies(data)
    if not anomalies.empty:
        st.warning(f"{len(anomalies)} low-power anomalies found:")
        st.dataframe(anomalies[['timestamp', 'power_output_w']])
    else:
        st.success("✅ No significant anomalies detected.")

    # 🤖 AI Tips for Optimization
    st.subheader("🤖 AI Recommendations")
    tips = generate_tips(data)
    for tip in tips:
        st.info(tip)

else:
    st.info("👈 Please upload a CSV file to begin.")
