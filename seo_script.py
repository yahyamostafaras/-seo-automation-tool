# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup

# Streamlit UI
st.title("SEO Heading Scraper")
st.write("Enter a URL to extract headings (H1 - H6):")

# Input field
url = st.text_input("Enter the URL:")

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

# Display results
if url:
    st.subheader("Extracted Headings:")
    headings = get_headings(url)
    for heading in headings:
        st.write(heading)
