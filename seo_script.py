import streamlit as st
import requests
from bs4 import BeautifulSoup

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
        return headings if headings else ["No headings found."]
    except requests.exceptions.RequestException as e:
        return [f"Error fetching the page: {e}"]

# Streamlit Page Configuration
st.set_page_config(page_title="SEO Heading Extractor", layout="wide")

# Custom CSS for Light/Dark Mode
dark_mode_css = """
    <style>
        body { background-color: #121212; color: white; }
        .stTextInput>div>div>input { background-color: #333; color: white; }
        .stButton>button { background-color: #1e88e5; color: white; }
        .stAlert { background-color: #333; color: white; }
        .stMarkdown { background-color: #222; padding: 10px; border-radius: 5px; }
    </style>
"""
light_mode_css = """
    <style>
        body { background-color: #f5f5f5; color: black; }
        .stTextInput>div>div>input { background-color: white; color: black; }
        .stButton>button { background-color: #007bff; color: white; }
        .stAlert { background-color: #dff0d8; color: black; }
        .stMarkdown { background-color: #ffffff; padding: 10px; border-radius: 5px; }
    </style>
"""

# Sidebar Theme Toggle
st.sidebar.header("🌗 Theme Mode")
theme_mode = st.sidebar.radio("", ["Light Mode", "Dark Mode"], index=0)

# Apply the selected theme
if theme_mode == "Dark Mode":
    st.markdown(dark_mode_css, unsafe_allow_html=True)
else:
    st.markdown(light_mode_css, unsafe_allow_html=True)

# App Title & Input Section
st.markdown("### [SEO Heading Extractor](#) ", unsafe_allow_html=True)
st.write("Developed by Yahya | Extract H1-H6 from any webpage")
st.markdown("---")
url = st.text_input("🔗 Enter a webpage URL below:")
if st.button("🔍 Extract Headings"):
    if url:
        headings = get_headings(url)
        st.success("✅ Headings extracted successfully!")
        st.markdown("### 📝 Extracted Headings:")
        for heading in headings:
            st.markdown(f"<div class='stMarkdown'>{heading}</div>", unsafe_allow_html=True)
    else:
        st.error("❌ Please enter a valid URL.")
