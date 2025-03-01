import streamlit as st
import requests
from bs4 import BeautifulSoup

# Load Custom CSS with Light/Dark Mode Support
def load_custom_css():
    css = """
    <style>
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            background-color: var(--btn-color);
            color: white;
            border-radius: 8px;
            padding: 10px;
            font-size: 16px;
            border: none;
        }
        .stTextInput>div>div>input {
            background-color: var(--input-bg);
            color: var(--text-color);
            border-radius: 5px;
            padding: 8px;
            border: 1px solid var(--border-color);
        }
        .stMarkdown {
            font-size: 18px;
            font-weight: bold;
        }
        /* Light Mode */
        .light-mode {
            --bg-color: #f5f5f5;
            --text-color: #333;
            --btn-color: #007bff;
            --input-bg: #fff;
            --border-color: #ccc;
        }
        /* Dark Mode */
        .dark-mode {
            --bg-color: #121212;
            --text-color: #f5f5f5;
            --btn-color: #1e88e5;
            --input-bg: #333;
            --border-color: #555;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Function to Extract Headings
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
        return [f"❌ Error fetching the page: {e}"]

# Initialize Streamlit App
st.set_page_config(page_title="SEO Heading Extractor", layout="wide")

# Load CSS
load_custom_css()

# Sidebar Theme Toggle
theme = st.sidebar.radio("🌗 Theme Mode", ["Light Mode", "Dark Mode"])

# Apply Theme Class
if theme == "Dark Mode":
    st.markdown('<div class="dark-mode">', unsafe_allow_html=True)
else:
    st.markdown('<div class="light-mode">', unsafe_allow_html=True)

# Title and Subtitle
st.markdown("<h2 style='text-align: center; color: #007bff;'>SEO Heading Extractor</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Developed by <b>Yahya</b> | Extract H1-H6 from any webpage</p>", unsafe_allow_html=True)

st.write("🔗 **Enter a webpage URL below:**")

# Input URL
url = st.text_input("Enter URL here", "https://www.replicaairguns.ca/")

# Extract Headings Button
if st.button("🔍 Extract Headings"):
    with st.spinner("Fetching headings..."):
        headings = get_headings(url)

    st.success("✅ Headings extracted successfully!")
    
    # Display Extracted Headings
    st.markdown("### 📑 Extracted Headings:")
    for heading in headings:
        st.markdown(f"<div style='padding:10px; background-color:#222; color:white; border-radius:5px; margin-bottom:5px;'>{heading}</div>", unsafe_allow_html=True)
