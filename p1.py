import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_scraped_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            page_title = soup.title.string if soup.title else "No title found"
            paragraphs = [p.get_text() for p in soup.find_all('p')]
            return page_title, paragraphs
        else:
            return "Failed to retrieve the web page.", []
    except Exception as e:
        return f"An error occurred: {e}", []

def perform_web_scraping():
    st.subheader("Web Scraping")
    url = st.text_input("Enter a URL to scrape", "https://en.wikipedia.org/wiki/Web_scraping")
    if url:
        page_title, paragraphs = get_scraped_content(url)
        st.write(f"### Page Title: {page_title}")
        for paragraph in paragraphs:
            st.write(paragraph)
