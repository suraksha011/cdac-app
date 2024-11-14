import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
# Make sure to download necessary NLTK datasets (first-time usage)
nltk.download('punkt')
nltk.download('stopwords')

# Function for Tokenization
def perform_tokenization(text):
    # Tokenizes the input text into individual words
    tokens = word_tokenize(text)
    return ', '.join(tokens)  # Output as a comma-separated list

# Function for POS Tagging
def perform_pos_tagging(text):
    # Tokenizes the input text and tags each word with its part of speech
    tokens = word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    # Convert to DataFrame for better visual presentation
    tagged_df = pd.DataFrame(tagged, columns=["Word", "POS"])
    return tagged_df

# Function for Lemmatization
def perform_lemmatization(text):
    # Lemmatizes the input text by reducing words to their root form
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = word_tokenize(text)
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens]
    return ', '.join(lemmatized)  # Output as a comma-separated list

# Function for Word Frequency
def perform_word_frequency(text):
    # Tokenizes the input text and calculates the frequency distribution of words
    tokens = word_tokenize(text)
    frequency = nltk.FreqDist(tokens)
    # Convert frequency distribution to a DataFrame for plotting
    freq_df = pd.DataFrame(frequency.items(), columns=["Word", "Frequency"])
    # Plotting the word frequency as a bar chart
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Word", y="Frequency", data=freq_df.sort_values(by="Frequency", ascending=False).head(10))
    plt.title("Top 10 Word Frequency")
    plt.xticks(rotation=45)
    plt.show()
    return freq_df

# Function for Stopword Removal
def perform_stopword_removal(text):
    # Removes common stopwords like "the", "a", etc. from the text
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text)
    filtered_text = [word for word in tokens if word.lower() not in stop_words]
    return ' '.join(filtered_text)  # Output as a space-separated string

# Function for Stemming
def perform_stemming(text):
    # Reduces words to their stem (root) form using the Porter Stemmer
    ps = PorterStemmer()
    tokens = word_tokenize(text)
    stemmed = [ps.stem(word) for word in tokens]
    return ', '.join(stemmed)  # Output as a comma-separated list

# Function for Sentiment Analysis
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

# Function for Word Cloud Generation (Optional extra)
def generate_word_cloud(text):
    from wordcloud import WordCloud
    # Generates a word cloud from the text
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    return wordcloud
