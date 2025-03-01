import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io

# Function to fetch HTML content
def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching page: {e}"

# Function to extract meta title & description
def extract_meta_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # Get Title
    title = soup.title.string.strip() if soup.title else "Title not found"
    title_length = len(title) if title != "Title not found" else 0

    # Get Meta Description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    og_desc = soup.find("meta", attrs={"property": "og:description"})
    
    if meta_desc and meta_desc.get("content"):
        description = meta_desc["content"].strip()
    elif og_desc and og_desc.get("content"):
        description = og_desc["content"].strip()
    else:
        description = "Meta description not found"
    
    desc_length = len(description) if description != "Meta description not found" else 0
    
    return title, title_length, description, desc_length

# Function to extract all headings (H1-H6) and their character counts
def extract_headings(html):
    soup = BeautifulSoup(html, "html.parser")
    headings = []
    for i in range(1, 7):  # H1 to H6
        for tag in soup.find_all(f'h{i}'):
            text = tag.get_text(strip=True)
            headings.append((f"H{i}", text, len(text)))
    return headings if headings else [("No headings found", "", 0)]

# Function to create an Excel file
def create_excel(meta_data, headings):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_meta = pd.DataFrame([meta_data], columns=["Title", "Title Length", "Meta Description", "Description Length"])
        df_headings = pd.DataFrame(headings, columns=["Heading Tag", "Text", "Character Count"])
        
        df_meta.to_excel(writer, sheet_name="Meta Data", index=False)
        df_headings.to_excel(writer, sheet_name="Headings", index=False)
    
    output.seek(0)
    return output

# Streamlit UI
st.set_page_config(page_title="SEO Extractor", layout="wide")

# Centered Name & Title
st.markdown("<h1 style='text-align: center; color: #0078FF;'>SEO Data Extractor</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: grey;'>Developed by Yahya</h3>", unsafe_allow_html=True)

# Sidebar Theme Toggle
st.sidebar.markdown("### Theme Mode")
theme = st.sidebar.radio("Select Theme", ["Light Mode", "Dark Mode"])

if theme == "Dark Mode":
    st.markdown(
        """
        <style>
        body { background-color: #0e1117; color: white; }
        .stTextInput>div>div>input { background-color: #333; color: white; }
        .stButton>button { background-color: #0078FF; color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )

# URL Input
url = st.text_input("🔗 Enter a webpage URL:", " ")

# Extract Button
extract_button = st.button("🔍 Extract SEO Data")

# **Trigger extraction when ENTER key is pressed OR button is clicked**
if url and (extract_button or url):  
    st.write("🔄 Fetching data, please wait...")

    html = fetch_html(url)

    if "Error fetching page" in html:
        st.error(html)
    else:
        title, title_length, description, desc_length = extract_meta_data(html)
        headings = extract_headings(html)

        st.success("✅ Data extracted successfully!")

        # Display Meta Title & Description
        st.markdown("### 📌 Meta Data")
        st.write(f"**Title:** {title}  _(Characters: {title_length})_")
        st.write(f"**Meta Description:** {description}  _(Characters: {desc_length})_")

        # Display Headings
        st.markdown("### 🏷️ Extracted Headings (with Lengths):")
        for tag, text, length in headings:
            st.markdown(f"- **{tag}:** {text} _(Characters: {length})_")

        # Download as Excel
        excel_data = create_excel((title, title_length, description, desc_length), headings)
        st.download_button(
            label="📥 Download SEO Data (Excel)",
            data=excel_data,
            file_name="seo_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
