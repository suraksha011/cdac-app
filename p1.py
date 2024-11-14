from turtle import st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO
import os

# Function to load the CSS file
def load_css():
    css_file_path = os.path.join(os.getcwd(), 'css', 'style.css')
    if os.path.exists(css_file_path):
        with open(css_file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.error("CSS file not found!")
    
def get_scraped_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No title"
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        return title, paragraphs
    else:
        return None, None

def create_excel_file(title, content):
    df = pd.DataFrame(content, columns=["Content"])
    df["Title"] = title
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output.getvalue()
