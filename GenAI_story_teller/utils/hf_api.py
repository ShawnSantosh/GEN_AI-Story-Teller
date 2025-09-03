# utils/api_calls.py

import streamlit as st
import requests
import google.generativeai as genai
import io
from PIL import Image
import base64 # Needed for Stability AI if you switch later

# --- ⚙️ API Configuration ---
try:
    # Configure Gemini API
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Configure Hugging Face API
    HF_TOKEN = st.secrets["HF_TOKEN"]
    HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # --- 💡 UPDATED MODEL URL ---
    # Switched from v1-5 to the newer Stable Diffusion XL 1.0
    SD_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

except (KeyError, AttributeError):
    st.error("API keys not found. Please add GEMINI_API_KEY and HF_TOKEN to your Streamlit secrets.")
    st.stop()


# --- 📝 Text Generation ---
def query_gemini(prompt: str) -> str:
    """Sends a prompt to the Gemini API and returns the text response."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred with the Gemini API: {e}")
        return ""

# --- 🖼️ Image Generation ---
def query_sd(prompt: str) -> Image.Image:
    """Sends a prompt to Hugging Face's Stable Diffusion API."""
    payload = {"inputs": prompt}
    response = requests.post(SD_URL, headers=HF_HEADERS, json=payload)
    response.raise_for_status()
    return Image.open(io.BytesIO(response.content))