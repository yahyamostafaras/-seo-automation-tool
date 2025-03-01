import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io

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
def get_headings(soup):
    headings = []
    for i in range(1, 7):  # Loop through h1 to h6
        for tag in soup.find_all(f'h{i}'):
            headings.append(f"H{i}: {tag.get_text(strip=True)}")
    return headings if headings else ["No headings found."]

# Function to Extract Meta Data
def get_meta_data(soup):
    title = soup.title.string if soup.title else "No Title Found"
    description = soup.find("meta", attrs={"name": "description"})
    keywords = soup.find("meta", attrs={"name": "keywords"})

    meta_description = description["content"] if description else "No Meta Description Found"
    meta_keywords = keywords["content"] if keywords else "No Meta Keywords Found"

    return {
        "title": title,
        "description": meta_description,
        "keywords": meta_keywords
    }

# Function to Fetch and Parse Page
def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        headings = get_headings(soup)
        meta_data = get_meta_data(soup)

        return headings, meta_data
    
    except requests.exceptions.RequestException as e:
        return [f"❌ Error fetching the page: {e}"], {}

# Function to Create Excel File
def create_excel(meta_data, headings):
    output = io.BytesIO()
    
    # Create DataFrame
    data = {
        "Meta Title": [meta_data["title"]],
        "Meta Description": [meta_data["description"]],
        "Meta Keywords": [meta_data["keywords"]],
        "Headings": [", ".join(headings)]  # Store headings as comma-separated
    }
    
    df = pd.DataFrame(data)
    
    # Save to Excel
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="SEO Data")
    
    return output.getvalue()

# Initialize Streamlit App
st.set_page_config(page_title="SEO Analyzer", layout="wide")

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
st.markdown("<h2 style='text-align: center; color: #007bff;'>SEO Analyzer</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Developed by <b>Yahya</b> | Extract H1-H6, Title, Meta Description & Keywords</p>", unsafe_allow_html=True)

st.write("🔗 **Enter a webpage URL below:**")

# Input URL
url = st.text_input("Enter URL here", " ")

# Extract Data Button
if st.button("🔍 Analyze Page"):
    with st.spinner("Fetching SEO Data..."):
        headings, meta_data = fetch_page(url)

    st.success("✅ SEO Data extracted successfully!")
    
    # Display Meta Title
    st.markdown("### 🏷️ Meta Title:")
    st.markdown(f"<div style='padding:10px; background-color:#222; color:white; border-radius:5px;'>{meta_data['title']}</div>", unsafe_allow_html=True)

    # Display Meta Description
    st.markdown("### 📝 Meta Description:")
    st.markdown(f"<div style='padding:10px; background-color:#222; color:white; border-radius:5px;'>{meta_data['description']}</div>", unsafe_allow_html=True)

    # Display Meta Keywords
    st.markdown("### 🔑 Meta Keywords:")
    st.markdown(f"<div style='padding:10px; background-color:#222; color:white; border-radius:5px;'>{meta_data['keywords']}</div>", unsafe_allow_html=True)

    # Display Extracted Headings
    st.markdown("### 📑 Extracted Headings:")
    for heading in headings:
        st.markdown(f"<div style='padding:10px; background-color:#222; color:white; border-radius:5px; margin-bottom:5px;'>{heading}</div>", unsafe_allow_html=True)

    # Create Downloadable Excel File
    excel_data = create_excel(meta_data, headings)
    st.download_button(
        label="📥 Download SEO Data as Excel",
        data=excel_data,
        file_name="seo_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
