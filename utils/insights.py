import pandas as pd

def detect_anomalies(data):
    threshold = data['power_output_w'].mean() * 0.5
    anomalies = data[data['power_output_w'] < threshold]
    return anomalies

def generate_tips(data):
    tips = []
    if data['ambient_temperature_c'].mean() > 35:
        tips.append("🌡️ High ambient temp detected. Consider cooling panels for efficiency.")
    if data['power_output_w'].mean() < 100:
        tips.append("⚠️ Low average power output. Inspect panel cleanliness and orientation.")
    if data['battery_charge_level_%'].mean() < 30:
        tips.append("🔋 Battery level often low. Consider higher capacity or optimized charging.")
    
    if not tips:
        tips.append("✅ All systems operating efficiently!")
    return tips
