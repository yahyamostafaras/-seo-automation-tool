import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
        return None

def extract_seo_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else "Title not found"
    
    meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
    meta_desc = meta_desc_tag['content'] if meta_desc_tag else "Meta description not found"
    
    h1_tag = soup.find('h1')
    h1 = h1_tag.text.strip() if h1_tag else "H1 not found"
    
    word_count = len(soup.get_text().split())
    images = soup.find_all('img')
    missing_alt = sum(1 for img in images if not img.get('alt'))
    
    return {
        "title": title,
        "meta_description": meta_desc,
        "h1": h1,
        "word_count": word_count,
        "missing_alt": missing_alt,
    }

def calculate_seo_score(seo_data):
    score = 0
    
    if 50 <= len(seo_data["title"]) <= 60:
        score += 10
    
    if 120 <= len(seo_data["meta_description"]) <= 160:
        score += 10
    
    if seo_data["h1"] != "H1 not found":
        score += 10
    
    if seo_data["word_count"] >= 300:
        score += 10
    
    if seo_data["missing_alt"] == 0:
        score += 10
    
    return score

def main():
    st.title("SEO Score Checker")
    url = st.text_input("Enter a webpage URL:")
    
    if st.button("Analyze SEO") or st.session_state.get("enter_pressed"):
        if url:
            html = fetch_html(url)
            if html:
                seo_data = extract_seo_data(html)
                seo_score = calculate_seo_score(seo_data)
                
                st.subheader("SEO Score: ")
                st.markdown(f"### {seo_score} / 100")
                
                st.write("**Title:**", seo_data["title"])
                st.write("**Meta Description:**", seo_data["meta_description"])
                st.write("**H1:**", seo_data["h1"])
                st.write(f"**Word Count:** {seo_data['word_count']}")
                st.write(f"**Images Missing ALT:** {seo_data['missing_alt']}")
    
    st.session_state["enter_pressed"] = st.text_input("Press ENTER to submit", key="enter_key")

if __name__ == "__main__":
    main()
