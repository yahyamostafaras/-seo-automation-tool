# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
import io

# Set page config
st.set_page_config(page_title="SEO Heading & Meta Extractor", page_icon="🔍", layout="wide")

# Custom CSS for light/dark mode
st.markdown("""
    <style>
        .css-18e3th9 {
            padding: 1rem;
        }
        .stButton>button {
            background-color: #007BFF !important;
            color: white !important;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
        }
        .stTextInput>div>div>input {
            border: 2px solid #007BFF !important;
            border-radius: 5px;
        }
        .dark-theme {
            background-color: #1e1e1e;
            color: white;
        }
        .light-theme {
            background-color: white;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

# Theme toggle
theme = st.radio("🌗 Theme Mode", ["Light Mode", "Dark Mode"], horizontal=True)
page_class = "dark-theme" if theme == "Dark Mode" else "light-theme"
st.markdown(f'<div class="{page_class}">', unsafe_allow_html=True)

# Title
st.title("🔍 SEO Heading & Meta Extractor")
st.markdown("**Developed by Yahya | Extract H1-H6 & Meta Data from any webpage**")

# User input
url = st.text_input("🌍 Enter a webpage URL below:")

# Function to fetch HTML with JavaScript support
def fetch_html(url):
    session = HTMLSession()
    response = session.get(url)
    response.html.render(timeout=20)  # Render JavaScript
    return response.html.html

# Function to extract headings
def get_headings(soup):
    headings = []
    for i in range(1, 7):  # Loop through H1-H6
        for tag in soup.find_all(f'h{i}'):
            headings.append(f"**H{i}:** {tag.get_text(strip=True)}")
    return headings if headings else ["No headings found."]

# Function to extract meta data
def get_meta_data(soup):
    data = {}

    # Extract title
    title_tag = soup.find("title")
    data["Title"] = title_tag.get_text(strip=True) if title_tag else "Title not found."

    # Extract meta description
    description = None
    for attr in ["name", "property"]:
        for value in ["description", "og:description", "twitter:description"]:
            meta_tag = soup.find("meta", attrs={attr: value})
            if meta_tag and "content" in meta_tag.attrs:
                description = meta_tag["content"]
                break
        if description:
            break

    # Extract from <noscript> if still missing
    if not description:
        noscript_tag = soup.find("noscript")
        if noscript_tag:
            nosoup = BeautifulSoup(noscript_tag.text, "html.parser")
            meta_in_noscript = nosoup.find("meta", attrs={"name": "description"})
            if meta_in_noscript and "content" in meta_in_noscript.attrs:
                description = meta_in_noscript["content"]

    data["Meta Description"] = description if description else "Meta description not found."

    # Extract meta keywords
    keywords_tag = soup.find("meta", attrs={"name": "keywords"})
    data["Meta Keywords"] = keywords_tag["content"] if keywords_tag and "content" in keywords_tag.attrs else "No keywords found."

    return data

# Function to create an Excel file
def create_excel(meta_data, headings):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Convert meta data to DataFrame
        meta_df = pd.DataFrame(list(meta_data.items()), columns=["Tag", "Value"])
        meta_df.to_excel(writer, sheet_name="Meta Data", index=False)

        # Convert headings to DataFrame
        headings_df = pd.DataFrame(headings, columns=["Headings"])
        headings_df.to_excel(writer, sheet_name="Headings", index=False)

        writer.close()
    return output.getvalue()

# Extract data on button click
if st.button("🔎 Extract Data"):
    if url:
        try:
            # Fetch & parse HTML
            html_content = fetch_html(url)
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract data
            meta_data = get_meta_data(soup)
            headings = get_headings(soup)

            # Display results
            st.success("✅ Data extracted successfully!")

            # Display Meta Data
            st.subheader("📌 Extracted Meta Data:")
            for key, value in meta_data.items():
                st.markdown(f"**{key}:** {value}")

            # Display Headings
            st.subheader("📌 Extracted Headings:")
            for heading in headings:
                st.markdown(f"- {heading}")

            # Generate Excel file for download
            excel_data = create_excel(meta_data, headings)
            st.download_button(label="📥 Download Data as Excel",
                               data=excel_data,
                               file_name="seo_data.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        except Exception as e:
            st.error(f"⚠️ Error fetching data: {e}")
    else:
        st.warning("⚠️ Please enter a valid URL.")
