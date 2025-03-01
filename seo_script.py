# -*- coding: utf-8 -*-

import streamlit as st
import requests
from bs4 import BeautifulSoup

# Set Streamlit page configuration
st.set_page_config(
    page_title="SEO Heading Extractor | Yahya",
    page_icon="🔍",
    layout="wide"
)

# Theme toggle switch
theme = st.sidebar.radio("🌗 Theme Mode", ["Light Mode", "Dark Mode"])

# Define CSS for Light & Dark modes
light_mode = """
    <style>
        body { background-color: #f4f7fc; color: #333; font-family: 'Arial', sans-serif; }
        .main-container { background: #ffffff; padding: 40px; border-radius: 15px; box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.1); }
        .big-title { font-size: 40px; font-weight: bold; color: #007bff; text-align: center; }
        .small-text { font-size: 18px; text-align: center; color: #666; font-weight: 500; }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea { font-size: 18px; padding: 12px; border-radius: 10px; border: 1px solid #ccc; background: #fff; }
        .stButton>button { background: linear-gradient(45deg, #007bff, #0056b3); color: white; font-size: 20px; border-radius: 12px; padding: 12px 20px; border: none; transition: 0.3s; font-weight: bold; box-shadow: 3px 3px 15px rgba(0, 0, 0, 0.2); }
        .stButton>button:hover { background: linear-gradient(45deg, #0056b3, #004494); transform: scale(1.05); }
        .results-container { background: #eef5ff; padding: 20px; border-radius: 12px; box-shadow: 3px 3px 15px rgba(0, 0, 0, 0.1); margin-top: 20px; }
        .heading-item { font-size: 18px; font-weight: bold; background: #ffffff; padding: 10px; border-radius: 8px; margin-bottom: 5px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); }
    </style>
"""

dark_mode = """
    <style>
        body { background-color: #121212; color: #ffffff; font-family: 'Arial', sans-serif; }
        .main-container { background: #1e1e1e; padding: 40px; border-radius: 15px; box-shadow: 5px 5px 20px rgba(255, 255, 255, 0.1); }
        .big-title { font-size: 40px; font-weight: bold; color: #00aaff; text-align: center; }
        .small-text { font-size: 18px; text-align: center; color: #bbbbbb; font-weight: 500; }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea { font-size: 18px; padding: 12px; border-radius: 10px; border: 1px solid #444; background: #222; color: white; }
        .stButton>button { background: linear-gradient(45deg, #00aaff, #0088cc); color: white; font-size: 20px; border-radius: 12px; padding: 12px 20px; border: none; transition: 0.3s; font-weight: bold; box-shadow: 3px 3px 15px rgba(255, 255, 255, 0.2); }
        .stButton>button:hover { background: linear-gradient(45deg, #0088cc, #0077bb); transform: scale(1.05); }
        .results-container { background: #222; padding: 20px; border-radius: 12px; box-shadow: 3px 3px 15px rgba(255, 255, 255, 0.1); margin-top: 20px; }
        .heading-item { font-size: 18px; font-weight: bold; background: #333; padding: 10px; border-radius: 8px; margin-bottom: 5px; box-shadow: 2px 2px 5px rgba(255, 255, 255, 0.1); }
    </style>
"""

# Apply selected theme
st.markdown(light_mode if theme == "Light Mode" else dark_mode, unsafe_allow_html=True)

# Professional header
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<p class="big-title">SEO Heading Extractor</p>', unsafe_allow_html=True)
st.markdown('<p class="small-text">Developed by <strong>Yahya</strong> | Extract H1-H6 from any webpage</p>', unsafe_allow_html=True)

# User input section
st.write("🔗 **Enter a webpage URL below:**")
url = st.text_input("", placeholder="https://example.com")

# Function to fetch and parse HTML headings
def get_headings(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        headings = []
        for i in range(1, 7):  # Loop through h1 to h6
            for tag in soup.find_all(f'h{i}'):
                headings.append(f"**H{i}:** {tag.get_text(strip=True)}")

        return headings if headings else ["⚠ No headings found on this page."]

    except requests.exceptions.RequestException as e:
        return [f"❌ Error fetching the page: {e}"]

# Centered layout for the button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔍 Extract Headings"):
        if url:
            st.success("✅ Headings extracted successfully!")

            # Display extracted headings in a styled card
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            st.subheader("📝 Extracted Headings:")
            headings = get_headings(url)
            for heading in headings:
                st.markdown(f'<div class="heading-item">{heading}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠ Please enter a valid URL.")

st.markdown('</div>', unsafe_allow_html=True)
