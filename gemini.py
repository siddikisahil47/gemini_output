import os
import streamlit as st
import requests
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

st.markdown(
    """
    <style>
    .main {
        background-color: #F5F5F5;
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]


model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              safety_settings=safety_settings)

response = requests.get("https://fleastore.in/gem/img.png")
response.raise_for_status()

with open("image0.jpeg", "wb") as f:
    f.write(response.content)

if not (img := Path("image0.jpeg")).exists():
  raise FileNotFoundError(f"Could not find image: {img}")

image_parts = [
  {
    "mime_type": "image/jpeg",
    "data": Path("image0.jpeg").read_bytes()
  },
]

predefined_prompt = "read image and Detect all possible Dark pattern"
prompt_parts = [
  {
    "text": predefined_prompt,
  },
  image_parts[0],
]

response = model.generate_content(prompt_parts)

# st.title("Google's Gemini Pro - Vision")
# st.image("image0.jpeg")
st.write(response.text)
