import streamlit as st
import requests
from bs4 import BeautifulSoup

def perform_web_scraping():
    st.subheader("Web Scraping")
    
    url = st.text_input("Enter a URL to scrape", "https://en.wikipedia.org/wiki/Web_scraping")

    if st.button("Scrape"):
        if url:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    st.write("Web page content scraped successfully!")
                    
                    page_title = soup.title.string if soup.title else "No title found"
                    st.write(f"### Page Title: {page_title}")
                    
                    paragraphs = soup.find_all('p')
                    for p in paragraphs:
                        st.write(p.get_text())
                else:
                    st.error("Failed to retrieve the web page.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a valid URL.")

def web_scraping_page():
    st.title("Web Scraping Results")
    perform_web_scraping()

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "web_scraping"  # Set default to web scraping

if st.session_state["page"] == "web_scraping":
    web_scraping_page()
