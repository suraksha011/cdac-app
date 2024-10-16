import streamlit as st
import pandas as pd
from textblob import TextBlob
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk import pos_tag
from collections import Counter
from bs4 import BeautifulSoup
import requests
import nltk
import os
import matplotlib.pyplot as plt
import seaborn as sns


# Explicitly set the NLTK data path to where the downloaded resources are located
nltk_data_path = os.path.expanduser('~') + '/nltk_data'
nltk.data.path.append(nltk_data_path)

print("nltk_data_path is : ", nltk_data_path)

# Ensure necessary packages are downloaded
nltk.download('tagsets_json')
nltk.download('averaged_perceptron_tagger_eng') 
nltk.download('punkt_tab')
nltk.download('punkt', download_dir=nltk_data_path)
nltk.download('wordnet', download_dir=nltk_data_path)
nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_path)
nltk.download('stopwords', download_dir=nltk_data_path)

# Page Configuration
st.set_page_config(page_title="AI Text Mining & Web Scraping", layout="centered")

# Function to process text from .txt file or .csv file
def load_file(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".csv"):
        df = pd.read_csv(file)
        # Combine all text columns into one for processing
        text = df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
        return ' '.join(text)
    else:
        st.error("Unsupported file format!")
        return None

# Page 1 - File Upload
def upload_file_page():
    st.title("AI Text Mining & Web Scraping")
    
    st.markdown("""<style>
    .title {font-size: 36px; font-weight: bold; color: #4CAF50; text-align: center;}
    .upload-box {display: flex; justify-content: center; align-items: center; padding: 20px; border: 2px dashed #4CAF50; background-color: #f9f9f9; border-radius: 10px; cursor: pointer;}
    .buttons {display: flex; justify-content: center; gap: 10px;}
    .button {padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; text-align: center;}
    </style>""", unsafe_allow_html=True)

    st.markdown("<h1 class='title'>Upload Your Text or CSV File</h1>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a text (.txt) or CSV (.csv) file", type=["txt", "csv"])

    if uploaded_file is not None:
        # Process the file and save the content
        file_content = load_file(uploaded_file)
        if file_content:
            st.session_state["file_content"] = file_content
            st.success("File uploaded successfully! Click 'Proceed' to go to the next page.")
        
        # Proceed to the next page
        if st.button("Proceed"):
            st.session_state["page"] = "process"

# Page 2 - Text Mining & Web Scraping Options
def process_file_page():
    st.title("AI-Based Text Mining & Web Scraping")

    st.markdown("""<style>
    .page-title {font-size: 32px; font-weight: bold; text-align: center; color: #FF5722;}
    .buttons {display: flex; justify-content: center; gap: 10px; margin-top: 20px;}
    .button {padding: 10px 20px; background-color: #FF5722; color: white; border: none; border-radius: 5px; cursor: pointer;}
    </style>""", unsafe_allow_html=True)

    st.markdown("<h1 class='page-title'>Choose a Task</h1>", unsafe_allow_html=True)

    if "file_content" not in st.session_state:
        st.error("No file uploaded. Please go back and upload a file.")
        return

    # Define button actions in correct sequence
    if st.button("Tokenization"):
        perform_tokenization(st.session_state["file_content"])

    if st.button("POS Tagging"):
        perform_pos_tagging(st.session_state["file_content"])

    if st.button("Lemmatization"):
        perform_lemmatization(st.session_state["file_content"])

    if st.button("Word Frequency"):
        perform_word_frequency(st.session_state["file_content"])

    if st.button("Stopword Removal"):
        perform_stopword_removal(st.session_state["file_content"])

    if st.button("Stemming"):
        perform_stemming(st.session_state["file_content"])

    if st.button("Sentiment Analysis"):
       perform_sentiment_analysis(st.session_state["file_content"])
 
    if st.button("Web Scraping"):
        perform_web_scraping()

# Tokenization Function
def perform_tokenization(text):
    st.subheader("Tokenization Result")
    tokens = word_tokenize(text)
    st.write("Tokens:")
    st.write(tokens)

# POS Tagging Function
def perform_pos_tagging(text):
    st.subheader("POS Tagging Result")
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    st.write("POS Tags:")
    st.write(pos_tags)

# Lemmatization Function
def perform_lemmatization(text):
    st.subheader("Lemmatization Result")
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    st.write("Lemmatized Tokens:")
    st.write(lemmatized_tokens)

# Stopword Removal Function
def perform_stopword_removal(text):
    st.subheader("Stopword Removal Result")
    stop_words = set(nltk.corpus.stopwords.words("english"))
    tokens = word_tokenize(text)
    filtered_tokens = [w for w in tokens if w.lower() not in stop_words]
    st.write("Filtered Tokens:")
    st.write(filtered_tokens)

# Stemming Function
def perform_stemming(text):
    st.subheader("Stemming Result")
    ps = PorterStemmer()
    tokens = word_tokenize(text)
    stemmed_words = [ps.stem(w) for w in tokens]
    st.write("Stemmed Words:")
    st.write(stemmed_words)

# Word Frequency Function
def perform_word_frequency(text):
    st.subheader("Word Frequency Result")
    tokens = word_tokenize(text)
    word_freq = Counter(tokens)
    st.write("Word Frequency:")
    st.write(word_freq)

# Sentiment Analysis Function with Pie Chart and Countplot
def perform_sentiment_analysis(text):
    st.subheader("Sentiment Analysis Result")
    
    # Ensure the text is a string and tokenize into sentences
    if isinstance(text, bytes):
        text = text.decode("utf-8")  # If file was read as bytes, decode it to string
    
    sentences = sent_tokenize(text)  # Use NLTK's sent_tokenize to split into sentences
    
    # Sentiment counters
    positive = 0
    negative = 0
    neutral = 0
    
    sentiment_labels = []
    
    # Analyze sentiment for each sentence
    for sentence in sentences:
        blob = TextBlob(sentence)  # Process each sentence individually
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            positive += 1
            sentiment_labels.append("Positive")
        elif sentiment < 0:
            negative += 1
            sentiment_labels.append("Negative")
        else:
            neutral += 1
            sentiment_labels.append("Neutral")
    
    # Display sentiment counts
    st.write(f"Positive Sentences: {positive}")
    st.write(f"Negative Sentences: {negative}")
    st.write(f"Neutral Sentences: {neutral}")
    
    # Pie chart for sentiment distribution
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive, negative, neutral]
    colors = ['#4CAF50', '#F44336', '#FFC107']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.
    st.pyplot(fig)
    
    # Countplot for sentiment categories
    fig, ax = plt.subplots()
    sns.countplot(x=sentiment_labels, palette=colors, ax=ax)
    ax.set_title('Count of Sentiment Categories')
    st.pyplot(fig)
    
    # Word Count Plot
    # tokens = word_tokenize(text)
    # word_count = len(tokens)
    
    # Display word count
    # st.write(f"Total Word Count: {word_count}")
    
    # Barplot of word count
    # fig, ax = plt.subplots()
    # sns.barplot(x=['Word Count'], y=[word_count], ax=ax)
    # ax.set_title('Word Count')
    # st.pyplot(fig)
    
# Web Scraping Function 

def perform_web_scraping():
    st.subheader("Web Scraping")

    # URL input from the user
    url = st.text_input("Enter a URL to scrape", "https://en.wikipedia.org/wiki/Web_scraping")

    # Button to trigger scraping
    if st.button("Scrape"):
        if url:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    st.write("Web page content scraped successfully!")
                    
                    # Extract and display the title and all paragraphs
                    page_title = soup.title.string if soup.title else "No title found"
                    st.write(f"### Page Title: {page_title}")
                    
                    # Extract paragraphs
                    paragraphs = soup.find_all('p')
                    for p in paragraphs:
                        st.write(p.get_text())
                        
                else:
                    st.error("Failed to retrieve the web page.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a valid URL.")

# Page 3 - Web Scraping Results
def web_scraping_page():
    st.title("Web Scraping Results")
    perform_web_scraping()

# Main logic to determine which page to show
if "page" not in st.session_state:
    st.session_state["page"] = "upload"

if st.session_state["page"] == "upload":
    upload_file_page()
elif st.session_state["page"] == "process":
    process_file_page()
elif st.session_state["page"] == "web_scraping":
    web_scraping_page()