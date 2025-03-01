import requests
from bs4 import BeautifulSoup
import streamlit as st

# Streamlit UI
st.title("SEO Heading Extractor")
st.write("Enter a URL to extract H1-H6 headings.")

# User input
url = st.text_input("Enter URL:")

def get_headings(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        headings = [tag.get_text(strip=True) for i in range(1, 7) for tag in soup.find_all(f'h{i}')]
        return headings if headings else ["No headings found."]
    
    except requests.exceptions.RequestException as e:
        return [f"Error: {e}"]

# Display results
if url:
    headings = get_headings(url)
    st.write("### Extracted Headings:")
    for heading in headings:
        st.write(f"- {heading}")
