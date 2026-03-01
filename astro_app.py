import streamlit as st
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# --- COSMO PAGE CONFIGURATION ---
st.set_page_config(page_title="Astro-Vision Cosmo", layout="wide")

# --- ADVANCED CSS: STARFIELD & MINIMALIST TYPOGRAPHY ---
st.markdown("""
    <style>
    /* Fixed Starfield Background */
    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/stardust.png"), 
                          linear-gradient(to bottom, #000000, #020205);
        background-attachment: fixed;
        color: #e0e0e0;
    }

    /* Classical Serif Typography for Headlines */
    h1, h2, h3 {
        font-family: 'Georgia', serif;
        font-weight: 100;
        letter-spacing: 5px;
        color: #ffffff;
        text-align: center;
        text-transform: uppercase;
    }

    /* Clean Sans-Serif for Data and Labels */
    p, span, label {
        font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 300;
        letter-spacing: 1px;
        color: #b0b0b0;
    }

    /* Metric Glow Effect */
    div[data-testid="stMetricValue"] > div {
        color: #ffffff;
        font-family: 'Georgia', serif;
        text-shadow: 0 0 10px rgba(255,255,255,0.5);
    }

    /* Minimalist Ghost Button */
    .stButton>button {
        background-color: transparent;
        color: #ffffff;
        border: 1px solid #ffffff;
        border-radius: 0px;
        padding: 12px 50px;
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton>button:hover {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #ffffff;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 20, 0.8);
        border-right: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTEM LOGIC ---
load_dotenv("planet.env")
MY_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(api_key=MY_TOKEN)

def calculate_space_weight(weight, g_factor):
    return round(weight * g_factor, 2)

def calculate_space_age(age, o_factor):
    return round(age / o_factor, 1)

# --- INTERFACE LAYOUT ---
st.markdown("<h1>Astro-Vision Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>CELESTIAL DATA EXTRACTION SYSTEM</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Main container for inputs
with st.container():
    col_input, col_preview = st.columns([1, 1.5])
    
    with col_input:
        st.markdown("### DATA INPUT")
        u_weight = st.number_input("Earth Weight (kg)", min_value=1, value=75)
        u_age = st.number_input("Earth Age (years)", min_value=1, value=25)
        img_url = st.text_input("Celestial Body Image URL", "https://upload.wikimedia.org/wikipedia/commons/2/2b/Jupiter_and_its_shrunken_Great_Red_Spot.jpg")

    with col_preview:
        if img_url:
            st.image(img_url, use_container_width=True)

st.markdown("<br><hr><br>", unsafe_allow_html=True)

# Action Trigger
col_btn_left, col_btn_mid, col_btn_right = st.columns([1, 1, 1])
with col_btn_mid:
    execute = st.button("Initialize Analysis")

if execute:
    with st.spinner("Decoding cosmic signals..."):
        try:
            # Multi-modal request to Mistral
            prompt = (
                "Identify this celestial body. Return the following as raw data: "
                "Name, Gravity Factor (relative to Earth), Orbital Period (years), "
                "and a brief scientific survival analysis."
            )

            response = client.chat.completions.create(
                model="mistralai/Pixtral-12B-2409",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": img_url}}
                    ]
                }]
            )
            
            ai_data = response.choices[0].message.content
            
            # RESULTS DISPLAY
            res_col_left, res_col_right = st.columns(2)
            
            with res_col_left:
                st.markdown("### SCIENCE REPORT")
                st.write(ai_data)
                
            with res_col_right:
                st.markdown("### CALCULATIONS")
                # Using Jupiter reference values for the logic demonstration
                g_ref = 2.52 
                o_ref = 11.86
                
                st.metric("RELATIVE WEIGHT", f"{calculate_space_weight(u_weight, g_ref)} KG")
                st.metric("RELATIVE AGE", f"{calculate_space_age(u_age, o_ref)} YEARS")
        
        except Exception as e:
            st.error("Access Denied. Server Maintenance in progress.")
            st.info(f"System Log: {e}")

st.markdown("<br><br><p style='text-align: center; font-size: 10px;'>V 3.0 | MISTRAL AI INTEGRATION</p>", unsafe_allow_html=True)