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
st.markdown(
    """
    <style>
        /* General Styling */
        .stApp {
            background-color: #F9F9F9;  /* Very Light Gray Background */
            font-family: 'Roboto', sans-serif;
            color: #333333;  /* Dark Text Color */
            padding: 0;
            margin: 0;
        }

        /* Title Styling */
        .stTitle {
            font-size: 48px;
            color: #FFB6B9;  /* Light Coral */
            text-align: center;
            font-weight: 700;
            margin-top: 50px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }

        /* Subheader Styling */
        .stSubheader {
            font-size: 28px;
            color: #D4E6F1;  /* Soft Light Blue */
            text-align: center;
            font-weight: 600;
            margin-top: 30px;
        }

        /* Markdown/Text Styling */
        .stMarkdown {
            font-size: 18px;
            color: #6b6b6b;
            text-align: center;
            margin-top: 10px;
            padding: 0 20px;
        }

        /* Container Styling */
        .stContainer {
            margin: 0 auto;
            width: 80%;
            max-width: 1200px;
        }

        /* Button Styling */
        .stButton > button {
            padding: 12px 24px;
            margin: 5px;
            background-color: #FFB6B9;  /* Light Coral */
            color: white;
            font-size: 16px;
            border: none;
            cursor: pointer;
            border-radius: 8px;
            transition: background-color 0.3s;
            width: 250px;
            height: 40px;
        }

        /* Button Hover Styling */
        .stButton > button:hover {
            background-color: #F7E1C3;  /* Soft Peach */
        }

        # /* Button Container Styling */
        # .stButton > div {
        #     display: flex;
        #     justify-content: center;
        #     gap: 10px;
        #     # flex-wrap: wrap;
        # }

        /* Section Styling */
        .section-background {
            background-color: #FFFFFF;  /* White */
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }

        /* Alternate Section Styling */
        .alternate-background {
            background-color: #D4E6F1;  /* Soft Light Blue */
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }

        /* Content Card Styling */
        .card {
            background-color: #FFFFFF;  /* White */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }

        /* Description Box */
        .description-box {
            background-color: #FFB6B9;  /* Light Coral */
            border: 1px solid #F7E1C3;  /* Soft Peach */
            padding: 15px;
            border-radius: 8px;
            color: #333333;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Home Page Title
st.markdown("<h1 class='main-title'>AI Text Mining & Web Scraping</h1>", unsafe_allow_html=True)

# Description
st.markdown("<p class='description'>An AI-powered tool for efficient web scraping and advanced text mining tasks.</p>", unsafe_allow_html=True)

# Sidebar for Navigation
option = st.sidebar.radio(
    'Choose a Module:',
    ['HomePage', 'Web Scraping', 'Text Mining']
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
                # Option to download scraped data as Excel
                excel_data = create_excel_file(title, paragraphs)
                st.download_button(
                    label="Download as Excel",
                    data=excel_data,
                    file_name="scraped_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                #Scrpaed data
                st.write(f"### Page Title: {title}")
                for para in paragraphs:
                    st.write(para)
                
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

    # Display buttons after the file is uploaded
    buttons = ["Tokenization", "POS Tagging", "Lemmatization", "Word Frequency", "Stopword Removal", "Stemming", "Sentiment Analysis"]

    if 'file_content' in st.session_state:
        # Display buttons only after file is uploaded
        button_col = st.columns(len(buttons))

        for i, button in enumerate(buttons):
            with button_col[i]:
                # When a button is clicked, update the selected action
                if st.button(button, key=f"button_{i}", help=f"Perform {button} on the uploaded text"):
                    st.session_state.selected_action = button

    # Create an empty placeholder for dynamic output
    output_placeholder = st.empty()

    # Perform the selected action and update the placeholder dynamically
    if 'selected_action' in st.session_state:
        action = st.session_state.selected_action
        st.session_state.selected_action = action  # Ensure the action stays in session state

        with output_placeholder.container():  # Use the container to update dynamically
            if action == "Tokenization":
                result = perform_tokenization(file_content)
                st.subheader("Tokenized Text:")
                st.write(result)

            elif action == "POS Tagging":
                result = perform_pos_tagging(file_content)
                st.subheader("POS Tagged Text:")
                st.write(result)

            elif action == "Lemmatization":
                result = perform_lemmatization(file_content)
                st.subheader("Lemmatized Text:")
                st.write(result)

            elif action == "Word Frequency":
                result = perform_word_frequency(file_content)
                st.subheader("Word Frequency Analysis:")
                st.write(result)

            elif action == "Stopword Removal":
                result = perform_stopword_removal(file_content)
                st.subheader("Text After Stopword Removal:")
                st.write(result)

            elif action == "Stemming":
                result = perform_stemming(file_content)
                st.subheader("Stemmed Text:")
                st.write(result)

            elif action == "Sentiment Analysis":
                result = perform_sentiment_analysis(file_content)
                # st.subheader("Sentiment Analysis Results:")
                st.write(result)
