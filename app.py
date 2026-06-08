import streamlit as st
import pandas as pd
import datetime
import google.generativeai as genai

# --- CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="EcoTrack AI - Carbon Footprint Platform",
    page_icon="🌱",
    layout="wide"
)

# Securely fetch API key from Streamlit secrets or environment variables
# For local testing, add this to your .env or streamlit secrets
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    st.sidebar.warning("⚠️ API Key missing. Running in hybrid/deterministic fallback mode.")

# Initialize Session State for historical tracking
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🌱 EcoTrack AI: Personal Carbon Footprint Advisor")
st.caption("Track, understand, and reduce your climate impact with personalized automated insights.")

# --- SIDEBAR: USER CONTEXT ---
st.sidebar.header("👤 Your Profile Context")
user_region = st.sidebar.selectbox("Region/Country", ["India", "North America", "Europe", "Other"])
monthly_budget = st.sidebar.slider("Target Carbon Budget (kg CO2/month)", 100, 2000, 500)

# --- TRACKING CONTEXT LOGIC ---
tab1, tab2, tab3 = st.tabs(["📊 Footprint Calculator", "💡 Personalized AI Insights", "📈 Tracking History"])

with tab1:
    st.header("Calculate Your Daily/Monthly Footprint")
    st.write("Provide your baseline consumption metrics below to generate your context score.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🚗 Transportation")
        km_driven = st.number_input("Distance driven by car per week (KM)", min_value=0.0, value=50.0)
        fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric", "CNG"])
        public_transit = st.number_input("Public transit usage per week (Hours)", min_value=0.0, value=2.0)
        
    with col2:
        st.subheader("⚡ Home Energy")
        electricity_kwh = st.number_input("Monthly electricity consumption (kWh)", min_value=0.0, value=150.0)
        clean_energy_pct = st.slider("Percentage of renewable energy source (%)", 0, 100, 0)
        
    with col3:
        st.subheader("🍽️ Dietary Habits")
        diet_type = st.selectbox("Primary Diet Plan", ["Meat-heavy", "Balanced/Mixed", "Vegetarian", "Vegan"])
        food_waste = st.select_slider("Weekly food waste level", options=["Low", "Medium", "High"])

    # Environmental conversion calculations
    fuel_multipliers = {"Petrol": 0.24, "Diesel": 0.27, "Electric": 0.05, "CNG": 0.18}
    diet_multipliers = {"Meat-heavy": 300.0, "Balanced/Mixed": 200.0, "Vegetarian": 120.0, "Vegan": 80.0}
    
    transport_emissions = (km_driven * 52 * fuel_multipliers[fuel_type]) / 12
    transit_emissions = (public_transit * 52 * 0.1) / 12
    energy_emissions = electricity_kwh * 0.82 * (1 - clean_energy_pct/100)
    food_emissions = diet_multipliers[diet_type] + (15 if food_waste == "High" else 0)
    
    total_monthly_emissions = transport_emissions + transit_emissions + energy_emissions + food_emissions

    st.markdown("---")
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric("Your Monthly Carbon Footprint", f"{total_monthly_emissions:.2f} kg CO2", 
                  delta=f"{total_monthly_emissions - monthly_budget:.2f} vs Budget", delta_color="inverse")
    with metric_col2:
        if st.button("📝 Log This Assessment Entry"):
            entry = {
                "Date": datetime.date.today().strftime("%Y-%m-%d"),
                "Total Emissions (kg)": round(total_monthly_emissions, 2),
                "Transport": round(transport_emissions, 2),
                "Energy": round(energy_emissions, 2),
                "Diet": round(food_emissions, 2)
            }
            st.session_state.history.append(entry)
            st.success("Assessment parameters captured securely!")

with tab2:
    st.header("💡 Contextual Insights & Mitigation Strategy")
    
    if total_monthly_emissions > monthly_budget:
        st.warning("⚠️ High Footprint Alert: Your current lifestyle metrics exceed your stated budget target.")
    else:
        st.success("✅ Sustainable Operations: Your usage patterns match baseline environmental targets.")
        
    st.subheader("🤖 Generative AI Action Plan")
    
    if st.button("✨ Generate Personalized AI Recommendations"):
        if not GEMINI_API_KEY:
            st.error("Please configure your GEMINI_API_KEY to unlock generative analysis features.")
        else:
            with st.spinner("AI Engine is analyzing your carbon footprint vectors..."):
                try:
                    # Formulate structured prompt using the user's calculated metrics
                    prompt = f"""
                    You are an expert Environmental Sustainability Advisor. Analyze this user's carbon footprint context:
                    - Region: {user_region}
                    - Monthly Carbon Target Budget: {monthly_budget} kg CO2
                    - Actual Calculated Footprint: {total_monthly_emissions:.2f} kg CO2
                    
                    Breakdown:
                    - Transportation: {transport_emissions:.2f} kg CO2
                    - Household Energy: {energy_emissions:.2f} kg CO2
                    - Diet & Food Waste: {food_emissions:.2f} kg CO2
                    
                    Provide a concise, professional analysis including:
                    1. A assessment of their biggest emission bottleneck.
                    2. 3 highly practical, specific actions customized to their region ({user_region}) to help them drop below their goal.
                    Keep the tone encouraging, technical, and actionable. Do not use generic filler text.
                    """
                    
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    
                    st.markdown("### 📋 Your Tailored Advisor Matrix")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"AI generation pipeline error: {e}")

with tab3:
    st.header("📋 Historic Metrics Logger")
    if len(st.session_state.history) == 0:
        st.info("No logs present yet. Complete an entry in the calculator window to render progress lines.")
    else:
        df_history = pd.DataFrame(st.session_state.history)
        st.dataframe(df_history, use_container_width=True)
        st.line_chart(df_history.set_index("Date")["Total Emissions (kg)"])
  
