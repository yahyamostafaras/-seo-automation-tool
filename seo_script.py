# -*- coding: utf-8 -*-

import streamlit as st
import requests
from bs4 import BeautifulSoup

# Custom page config
st.set_page_config(
    page_title="SEO Heading Extractor | Yahya",
    page_icon="🔍",
    layout="centered"
)

# Custom CSS for professional look
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        .big-title {
            font-size: 36px;
            font-weight: bold;
            color: #F39C12;
            text-align: center;
        }
        .small-text {
            font-size: 16px;
            text-align: center;
            margin-top: -10px;
            color: #aaa;
        }
        .stButton>button {
            background-color: #F39C12;
            color: black;
            font-size: 18px;
            border-radius: 10px;
            padding: 8px 16px;
        }
        .stTextInput>div>div>input {
            font-size: 16px;
            padding: 10px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Professional header with Yahya's name
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

# Button section with professional layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔍 Extract Headings"):
        if url:
            st.success("✅ Headings extracted successfully!")
            st.subheader("📝 Extracted Headings:")
            headings = get_headings(url)
            for heading in headings:
                st.write(heading)
        else:
            st.warning("⚠ Please enter a valid URL.")
