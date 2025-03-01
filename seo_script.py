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
    title = soup.title.string.strip() if soup.title else "Title not found"
    meta_desc = soup.find("meta", attrs={"name": "description"})
    description = meta_desc["content"].strip() if meta_desc else "Meta description not found"
    return title, description

# Function to extract all headings (H1-H6)
def extract_headings(html):
    soup = BeautifulSoup(html, "html.parser")
    headings = []
    for i in range(1, 7):  # H1 to H6
        for tag in soup.find_all(f'h{i}'):
            headings.append(f"**H{i}:** {tag.get_text(strip=True)}")
    return headings if headings else ["No headings found"]

# Function to create an Excel file
def create_excel(meta_data, headings):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_meta = pd.DataFrame([meta_data], columns=["Title", "Meta Description"])
        df_headings = pd.DataFrame(headings, columns=["Headings"])
        
        df_meta.to_excel(writer, sheet_name="Meta Data", index=False)
        df_headings.to_excel(writer, sheet_name="Headings", index=False)
    
    output.seek(0)
    return output

# Streamlit UI
st.set_page_config(page_title="SEO Extractor", layout="wide")

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

# App Title
st.markdown("<h2 style='text-align: center; color: #0078FF;'>SEO Heading Extractor</h2>", unsafe_allow_html=True)
st.markdown("Developed by **Yahya** | Extract H1-H6 + Meta Tags")

# URL Input
url = st.text_input("🔗 Enter a webpage URL:", "https://www.example.com")

if st.button("🔍 Extract SEO Data"):
    st.write("🔄 Fetching data, please wait...")
    
    html = fetch_html(url)
    
    if "Error fetching page" in html:
        st.error(html)
    else:
        title, description = extract_meta_data(html)
        headings = extract_headings(html)

        st.success("✅ Data extracted successfully!")
        
        # Display Meta Title & Description
        st.markdown("### 📌 Meta Data")
        st.write(f"**Title:** {title}")
        st.write(f"**Meta Description:** {description}")

        # Display Headings
        st.markdown("### 🏷️ Extracted Headings:")
        for heading in headings:
            st.markdown(f"- {heading}")

        # Download as Excel
        excel_data = create_excel((title, description), headings)
        st.download_button(
            label="📥 Download Excel",
            data=excel_data,
            file_name="seo_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
