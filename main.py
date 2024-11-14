# main.py

import streamlit as st
from p1 import get_scraped_content, create_excel_file
from p2 import (
    perform_tokenization, perform_pos_tagging, perform_lemmatization,
    perform_word_frequency, perform_stopword_removal, perform_stemming,
    perform_sentiment_analysis
)

# Page Configurations
# st.set_page_config(page_title="AI Text Mining & Web Scraping", layout="centered")

# Custom CSS for background color and styling
st.markdown("""
    <style>
        /* Apply background color */
        body {
            background-color: #f6e0b5;  /* Light Pastel Yellow */
            font-family: 'Roboto', sans-serif;
            color: #333;
            margin: 0;
            padding: 0;
        }

        .main-title {
            font-size: 48px;
            color: #4a4a4a;
            text-align: center;
            font-weight: 700;
            margin-top: 50px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }

        .section-title {
            font-size: 28px;
            color: #ff6f61;  /* Pastel Coral */
            text-align: center;
            font-weight: 600;
            margin-top: 30px;
        }

        .description {
            font-size: 18px;
            color: #6b6b6b;
            text-align: center;
            margin-top: 10px;
            padding: 0 20px;
        }

        .container {
            margin: 0 auto;
            width: 80%;
            max-width: 1200px;
        }

        /* Custom styles for buttons */
        .operation-button {
            display: inline-block;
            padding: 12px 24px;
            margin: 5px;
            background-color: #ff6f61;
            color: white;
            font-size: 16px;
            border: none;
            cursor: pointer;
            border-radius: 8px;
            transition: background-color 0.3s;
        }

        .operation-button:hover {
            background-color: #ff3b2d;
        }

        .button-container {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
        }
    </style>
""", unsafe_allow_html=True)

# Home Page Title
st.markdown("<h1 class='main-title'>AI Text Mining & Web Scraping</h1>", unsafe_allow_html=True)

# Description
st.markdown("<p class='description'>An AI-powered tool for efficient web scraping and advanced text mining tasks.</p>", unsafe_allow_html=True)

# Sidebar for Navigation
option = st.sidebar.selectbox(
    'Choose a Module:',
    ['Home', 'Web Scraping', 'Text Mining']
)

# Show Home Page if the 'Home' option is selected
if option == 'Home':
    st.markdown("<h2 class='section-title'>Welcome to AI Text Mining & Web Scraping</h2>", unsafe_allow_html=True)
    st.markdown("<p class='description'>This platform offers advanced tools for text mining and web scraping. Please choose a module from the sidebar to get started.</p>", unsafe_allow_html=True)

# Show Web Scraping Page
elif option == 'Web Scraping':
    st.markdown("<h2 class='section-title'>Web Scraping Module</h2>", unsafe_allow_html=True)
    
    # URL input for scraping
    url = st.text_input("Enter a URL to scrape", "https://example.com")
    if st.button("Scrape"):
        if url:
            title, paragraphs = get_scraped_content(url)
            if title and paragraphs:
                st.write(f"### Page Title: {title}")
                for para in paragraphs:
                    st.write(para)
                
                # Option to download scraped data as Excel
                excel_data = create_excel_file(title, paragraphs)
                st.download_button(
                    label="Download as Excel",
                    data=excel_data,
                    file_name="scraped_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("Failed to retrieve content from the URL.")
        else:
            st.error("Please enter a valid URL.")

# Show Text Mining Page
elif option == 'Text Mining':
    st.markdown("<h2 class='section-title'>Text Mining Module</h2>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a text (.txt) or CSV (.csv) file", type=["txt", "csv"])
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        st.session_state["file_content"] = file_content
        st.success("File uploaded successfully!")

        # Buttons to trigger text mining operations
        st.markdown("<div class='button-container'>", unsafe_allow_html=True)

        if st.button("Tokenization"):
            result = perform_tokenization(file_content)
            st.subheader("Tokenized Text:")
            st.write(result)

        if st.button("POS Tagging"):
            result = perform_pos_tagging(file_content)
            st.subheader("POS Tagged Text:")
            st.write(result)

        if st.button("Lemmatization"):
            result = perform_lemmatization(file_content)
            st.subheader("Lemmatized Text:")
            st.write(result)

        if st.button("Word Frequency"):
            result = perform_word_frequency(file_content)
            st.subheader("Word Frequency Analysis:")
            st.write(result)

        if st.button("Stopword Removal"):
            result = perform_stopword_removal(file_content)
            st.subheader("Text After Stopword Removal:")
            st.write(result)

        if st.button("Stemming"):
            result = perform_stemming(file_content)
            st.subheader("Stemmed Text:")
            st.write(result)

        if st.button("Sentiment Analysis"):
            result = perform_sentiment_analysis(file_content)
            st.subheader("Sentiment Analysis Results:")
            st.write(result)
        
        st.markdown("</div>", unsafe_allow_html=True)
