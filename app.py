import streamlit as st
import pandas as pd
import datetime
from google import genai
from google.genai import types
from google.oauth2 import service_account
import os

# --- 1. CONFIGURATION & PROFESSIONAL DESIGN ---
st.set_page_config(
    page_title="EcoTrack AI | Personal Carbon Advisor",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .metric-container { display: flex; gap: 15px; margin-bottom: 25px; }
    .metric-card {
        background-color: #1e293b;
        padding: 22px;
        border-radius: 12px;
        border-top: 4px solid #3b82f6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        flex: 1;
        text-align: center;
    }
    .metric-card h3 { color: #94a3b8; font-size: 0.95rem; margin-bottom: 6px; }
    .metric-card h1 { color: #38bdf8; font-size: 2rem; margin: 0; }
    .stButton>button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        font-weight: bold;
        transition: 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(37,99,235,0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURE AUTHENTICATION MATRIX ---
@st.cache_resource
def get_ai_client():
    if os.path.exists("key.json"):
        try:
            creds = service_account.Credentials.from_service_account_file("key.json")
            return genai.Client()
        except Exception as e:
            st.sidebar.error(f"Credentials Parsing Error: {e}")
            
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if api_key:
        return genai.Client(api_key=api_key)
        
    return None

ai_client = get_ai_client()

if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. APPLICATION HEADER ---
st.title("🌱 EcoTrack AI: Personal Carbon Footprint Advisor")
st.caption("Track, understand, and mitigate your climate overhead using context-aware automation.")

# --- 4. SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("👤 Profile Context")
    user_region = st.selectbox("Operational Region", ["India", "North America", "Europe", "Other"])
    monthly_budget = st.slider("Target Carbon Budget (kg CO2/month)", 100, 2000, 500)
    st.markdown("---")
    if ai_client:
        st.success("⚡ System Status: Connected to Gemini")
    else:
        st.error("⚠️ System Status: Offline (Check Credentials)")

# --- 5. INTERACTIVE DASHBOARD STRUCTURE ---
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

    # Corrected coefficients matrix dictionary formatting
    fuel_multipliers = {"Petrol": 0.24, "Diesel": 0.27, "Electric": 0.05, "CNG": 0.18}
    diet_multipliers = {"Meat-heavy": 300.0, "Balanced/Mixed": 200.0, "Vegetarian": 120.0, "Vegan": 80.0}
    
    transport_emissions = (km_driven * 52 * fuel_multipliers[fuel_type]) / 12
    transit_emissions = (public_transit * 52 * 0.1) / 12
    energy_emissions = electricity_kwh * 0.82 * (1 - clean_energy_pct/100)
    food_emissions = diet_multipliers[diet_type] + (15 if food_waste == "High" else 0)
    
    total_monthly_emissions = transport_emissions + transit_emissions + energy_emissions + food_emissions

    st.markdown("---")
    
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <h3>Calculated Monthly Footprint</h3>
            <h1>{total_monthly_emissions:.2f} kg CO2</h1>
        </div>
        <div class="metric-card">
            <h3>Target Variance</h3>
            <h1 style="color: {'#ef4444' if total_monthly_emissions > monthly_budget else '#10b981'};">
                {total_monthly_emissions - monthly_budget:+.2f} kg
            </h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📝 Log This Assessment Entry"):
        entry = {
            "Date": datetime.date.today().strftime("%Y-%m-%d"),
            "Total Emissions (kg)": round(total_monthly_emissions, 2),
            "Transport": round(transport_emissions, 2),
            "Energy": round(energy_emissions, 2),
            "Diet": round(food_emissions, 2)
        }
        st.session_state.history.append(entry)
        st.success("Assessment parameters securely added to the local history logs!")
        st.balloons()

with tab2:
    st.header("💡 Contextual Insights & Mitigation Strategy")
    
    if total_monthly_emissions > monthly_budget:
        st.warning("⚠️ High Footprint Alert: Your current lifestyle metrics exceed your configured target ceiling.")
    else:
        st.success("✅ Sustainable Footprint: Your profile falls within safe operational limits.")
        
    st.subheader("🤖 Gemini 2.5 Intelligence Engine")
    
    if st.button("✨ Generate Personalized AI Recommendations"):
        if not ai_client:
            st.error("AI service client context is completely uninitialized. Verify project credentials.")
        else:
            with st.spinner("Analyzing cross-domain carbon vectors..."):
                try:
                    system_instruction = "You are an expert Environmental Sustainability Advisor specialized in low-impact lifestyle optimization architectures."
                    
                    user_prompt = f"""
                    Analyze this user's carbon profile:
                    - Country/Region: {user_region}
                    - Allocated Budget Target: {monthly_budget} kg CO2
                    - Actual Generated Footprint: {total_monthly_emissions:.2f} kg CO2
                    
                    Breakdowns:
                    - Commutes & Transport: {transport_emissions:.2f} kg CO2
                    - Grid Utility Energy: {energy_emissions:.2f} kg CO2
                    - Dietary Vectors: {food_emissions:.2f} kg CO2
                    
                    Compile a professional overview in clean markdown specifying the primary bottleneck, and 3 localized reduction tactics for {user_region}. Avoid fluff.
                    """
                    
                    response = ai_client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.3
                        )
                    )
                    
                    st.markdown("### 📋 Your Tailored Advisor Matrix")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"Execution Error during prompt inference: {e}")

with tab3:
    st.header("📋 Historic Metrics Logger")
    if len(st.session_state.history) == 0:
        st.info("No logs present yet. Log a calculation matrix first to construct trend analysis components.")
    else:
        df_history = pd.DataFrame(st.session_state.history)
        st.dataframe(df_history, use_container_width=True)
        st.line_chart(df_history.set_index("Date")["Total Emissions (kg)"])
