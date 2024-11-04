# main.py - Full Implementation Styled According to Design Document
import streamlit as st
import random  # Import random module for displaying random facts
from p1 import get_scraped_content  # Import web scraping function
from p2 import (  # Import text mining functions
    load_file, perform_tokenization, perform_pos_tagging, perform_lemmatization, 
    perform_word_frequency, perform_stopword_removal, perform_stemming, 
    perform_sentiment_analysis
)

# Set page configuration
# st.set_page_config(page_title="AI-Based Text Mining & Web Scraping", layout="wide")

# Page Content
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>AI-Based Text Mining and Web Scraping</h1>", unsafe_allow_html=True)

# Custom CSS Styling
st.markdown("""
    <style>
    /* Global Title */
    .title {
        font-size: 36px;
        color: #4CAF50;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    /* Section Titles */
    .section-title {
        font-size: 30px;
        color: #FF5722;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    /* Upload and URL input boxes */
    .upload-box, .url-input-box {
        display: flex;
        justify-content: center;
        padding: 20px;
        border: 2px dashed #4CAF50;
        background-color: #f9f9f9;
        border-radius: 10px;
        cursor: pointer;
        text-align: center;
    }
    /* Button Row */
    .button-row {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 20px;
        flex-wrap: wrap;
    }
    /* Task Buttons */
    .task-button {
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        text-align: center;
        width: 180px;
        margin-bottom: 10px;
    }
    /* Results Area */
    .results {
        margin-top: 20px;
        padding-top: 10px;
        border-top: 2px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# Random Facts about AI-based Text Mining and Web Scraping
random_facts = [
    "Text mining is a process of deriving high-quality information from text.",
    "Web scraping can be used to extract data from websites for various purposes, including price comparison and data analysis.",
    "AI-driven text mining can automate the extraction of insights from large volumes of text data.",
    "Natural Language Processing (NLP) is a key component of text mining that helps computers understand human language.",
    "Web scraping is often used in market research to gather data on competitors and market trends.",
    "Text mining techniques can be used in sentiment analysis to gauge public opinion from social media data.",
    "Web scraping can help researchers gather data for academic studies or reports without manual data entry.",
    "With proper tools, web scraping can extract information from various formats, including HTML, XML, and JSON."
]

# Sidebar Navigation
st.sidebar.header("Navigation")
if "page" not in st.session_state:
    st.session_state["page"] = "home"  # Default to Home

# Navigation Buttons
if st.sidebar.button("Text Mining"):
    st.session_state["page"] = "text_mining"
if st.sidebar.button("Web Scraping"):
    st.session_state["page"] = "web_scraping"

# Homepage Section with Random Facts
if st.session_state["page"] == "home":
    st.markdown("<h2 class='title'>Welcome to AI-Based Text Mining and Web Scraping</h2>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>Did You Know?</h3>", unsafe_allow_html=True)
    # Display a random fact
    st.write(random.choice(random_facts))

# Text Mining Section
if st.session_state["page"] == "text_mining":
    st.markdown("<h2 class='title'>TEXT MINING</h2>", unsafe_allow_html=True)
    
    # File Upload Section
    st.markdown("<div class='upload-box'>Upload Your File (Supported Formats: .csv, .txt)</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv", "txt"])

    if uploaded_file is not None:
        file_content = load_file(uploaded_file)
        if file_content:
            st.session_state["file_content"] = file_content
            st.success("File uploaded successfully!")

            # "Proceed" button to navigate to the next page
            if st.button("Proceed"):
                st.session_state["show_processing_options"] = True
                st.session_state["page"] = "processing_options"  # Navigate to processing options

# Processing Options Section
elif st.session_state.get("page") == "processing_options":
    st.markdown("<h2 class='title'>PROCESSING OPTIONS</h2>", unsafe_allow_html=True)

    # Check if the file content exists
    if "file_content" in st.session_state:
        st.markdown("<h3 class='section-title'>Choose a Processing Task</h3>", unsafe_allow_html=True)
        
        # Display processing task buttons in a structured row format
        col1, col2, col3 = st.columns(3)

        # Task Buttons
        with col1:
            if st.button("Tokenization", key="tokenize"):
                st.markdown("<div class='results'><b>Result:</b></div>", unsafe_allow_html=True)
                perform_tokenization(st.session_state["file_content"])
            if st.button("Stopword Removal", key="stopwords"):
                st.markdown("<div class='results'><b>Result:</b></div>", unsafe_allow_html=True)
                perform_stopword_removal(st.session_state["file_content"])
        
        with col2:
            if st.button("POS Tagging", key="pos"):
                st.markdown("<div class='results'><b>Result:</b></div>", unsafe_allow_html=True)
                perform_pos_tagging(st.session_state["file_content"])
            if st.button("Word Frequency", key="frequency"):
                st.markdown("<div class='results'><b>Result:</b></div>", unsafe_allow_html=True)
                perform_word_frequency(st.session_state["file_content"])

        with col3:
            if st.button("Lemmatization", key="lemma"):
                st.markdown("<div class='results'><b>Result:</b></div>", unsafe_allow_html=True)
                perform_lemmatization(st.session_state["file_content"])
            if st.button("Sentiment Analysis", key="sentiment"):
                st.markdown("<div class='results'><b>Result:</b></div>", unsafe_allow_html=True)
                perform_sentiment_analysis(st.session_state["file_content"])
        
        if st.button("Stemming", key="stem"):
            st.markdown("<div class='results'><b>Result:</b></div>", unsafe_allow_html=True)
            perform_stemming(st.session_state["file_content"])
    else:
        st.error("Please upload a file in the Text Mining section first.")

# Web Scraping Section
elif st.session_state["page"] == "web_scraping":
    st.markdown("<h2 class='title'>WEB SCRAPING</h2>", unsafe_allow_html=True)

    # URL Input for Web Scraping
    st.markdown("<div class='url-input-box'>Enter the URL</div>", unsafe_allow_html=True)
    url = st.text_input("", placeholder="https://example.com")

    # Scrape Button
    if st.button("Scrape"):
        if url:
            page_title, paragraphs = get_scraped_content(url)
            st.markdown("<div class='results'><b>Topic:</b></div>", unsafe_allow_html=True)
            st.write(page_title)
            st.markdown("<div class='results'><b>First 200 Words:</b></div>", unsafe_allow_html=True)
            st.write(" ".join(paragraphs[:200]))  # Display first 200 words
        else:
            st.error("Please enter a valid URL.")
