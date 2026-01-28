import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CommuteTracker", layout="wide")

# --- 1. CONSTANTS (The Science) ---
# Emission factors based on average commute (kg CO2 per trip)
EMISSION_FACTORS = {
    "Car": 2.3,    # High emissions
    "Bus": 12.0,   # High total, but efficient if full
    "Bike": 0.0    # Zero emissions
}

# --- 2. DATA SIMULATION (The Inputs) ---
@st.cache_data
def generate_data():
    """Simulates 12 hours of traffic at the campus gate."""
    data = []
    
    # Hours from 7 AM to 7 PM
    for hour in range(7, 19):
        
        # SCENARIO A: The "Solo Driver" Problem (9 AM)
        if hour == 9:
            # 50 cars arrive with only 1 person (Inefficient)
            data.append({"Hour": hour, "Type": "Car", "Passengers": 1, "Count": 50})
            data.append({"Hour": hour, "Type": "Bus", "Passengers": 45, "Count": 2}) # Full bus
            
        # SCENARIO B: The "Ghost Bus" Problem (11 AM)
        elif hour == 11:
            # A large bus runs with only 2 people (Waste)
            data.append({"Hour": hour, "Type": "Bus", "Passengers": 2, "Count": 1}) 
            data.append({"Hour": hour, "Type": "Car", "Passengers": 1, "Count": 8})

        # Normal Traffic Flow
        else:
            data.append({"Hour": hour, "Type": "Car", "Passengers": 2, "Count": np.random.randint(5, 12)})
            data.append({"Hour": hour, "Type": "Bike", "Passengers": 1, "Count": np.random.randint(10, 25)})

    # Expand into a detailed list for analysis
    rows = []
    for entry in data:
        for _ in range(entry["Count"]):
            rows.append({
                "Hour": entry["Hour"],
                "Vehicle": entry["Type"],
                "Passengers": entry["Passengers"],
                "Emission_kg": EMISSION_FACTORS[entry["Type"]]
            })
    
    return pd.DataFrame(rows)

# --- 3. ANALYSIS ENGINE (The Logic) ---
def analyze_impact(df):
    # Metric: Emissions Per Person (Lower is better)
    df['Efficiency_Score'] = df['Emission_kg'] / df['Passengers']
    
    # Waste Detection Logic
    def detect_problem(row):
        if row['Vehicle'] == 'Bus' and row['Passengers'] < 5:
            return "CRITICAL WASTE (Ghost Bus)"
        elif row['Vehicle'] == 'Car' and row['Passengers'] == 1:
            return "INEFFICIENT (Solo Driver)"
        else:
            return "OPTIMAL"
            
    df['Status'] = df.apply(detect_problem, axis=1)
    return df

# --- 4. DASHBOARD UI (The Visuals) ---
st.title("🚌 CommuteTracker: Transport Impact Monitor")
st.markdown("**Theme:** Climate Action | **Scope:** Transportation Efficiency")

# Load and process data
df = generate_data()
df = analyze_impact(df)

# Top KPIs
total_co2 = df['Emission_kg'].sum()
avg_efficiency = df['Efficiency_Score'].mean()
total_students = df['Passengers'].sum()

k1, k2, k3 = st.columns(3)
k1.metric("🌍 Total CO2 Today", f"{total_co2:.1f} kg")
k2.metric("👥 Total Commuters", f"{total_students}")
k3.metric("📉 Avg CO2 Per Person", f"{avg_efficiency:.2f} kg", delta_color="inverse")

st.divider()

# Charts
c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 Transport Mode Mix")
    # Pie chart showing too many cars
    fig_pie = px.pie(df, names='Vehicle', title='Vehicle Types Entering Campus')
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.subheader("⚠️ Efficiency Analysis (Hourly)")
    # Bar chart highlighting the waste events in RED
    fig_bar = px.bar(df, x='Hour', y='Emission_kg', color='Status',
                     color_discrete_map={
                         "CRITICAL WASTE (Ghost Bus)": "#FF4B4B",  # Red
                         "INEFFICIENT (Solo Driver)": "#FFA15A",   # Orange
                         "OPTIMAL": "#00CC96"                      # Green
                     },
                     title="CO2 Emissions by Hour (Red = Waste)")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- 5. ACTION CENTER (The Solution) ---
st.subheader("📢 Smart Recommendations")

# Filter for today's specific problems
ghost_buses = df[df['Status'] == "CRITICAL WASTE (Ghost Bus)"]
solo_drivers = df[df['Status'] == "INEFFICIENT (Solo Driver)"]

col_a, col_b = st.columns(2)

with col_a:
    if not ghost_buses.empty:
        st.error(f"🚨 **ALERT:** Empty Bus detected at 11:00 AM!")
        st.info("**ACTION:** Cancel fixed schedule for 11 AM. Replace with 'On-Demand' van service.\n\n*Potential Savings: 12kg CO2/day*")
    else:
        st.success("✅ Bus fleet is optimized.")

with col_b:
    if not solo_drivers.empty:
        st.warning(f"⚠️ **TRAFFIC:** High volume of Solo Drivers at 9:00 AM.")
        st.info("**ACTION:** Open 'Carpool Priority Lane' at main gate to incentivize sharing.")
    else:
        st.success("✅ Carpooling rates are healthy.")