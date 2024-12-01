from typing_extensions import Buffer
import nltk
import re
import io
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

def create_download_button(df, file_name, button_label):
    # Convert the DataFrame to an Excel buffer
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()
        
    buffer.seek(0)

    # Create a download button in Streamlit
    st.download_button(
        label=button_label,
        data=buffer,
        file_name=file_name,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# POS tag abbreviations and their full forms
pos_abbreviations = {
    'CC': 'Coordinating conjunction',
    'CD': 'Cardinal number',
    'DT': 'Determiner',
    'EX': 'Existential there',
    'FW': 'Foreign word',
    'IN': 'Preposition or subordinating conjunction',
    'JJ': 'Adjective',
    'JJR': 'Adjective, comparative',
    'JJS': 'Adjective, superlative',
    'LS': 'List item marker',
    'MD': 'Modal',
    'NN': 'Noun, singular or mass',
    'NNS': 'Noun, plural',
    'NNP': 'Proper noun, singular',
    'NNPS': 'Proper noun, plural',
    'PDT': 'Predeterminer',
    'POS': 'Possessive ending',
    'PRP': 'Personal pronoun',
    'PRP$': 'Possessive pronoun',
    'RB': 'Adverb',
    'RBR': 'Adverb, comparative',
    'RBS': 'Adverb, superlative',
    'RP': 'Particle',
    'SYM': 'Symbol',
    'TO': 'To',
    'UH': 'Interjection',
    'VB': 'Verb, base form',
    'VBD': 'Verb, past tense',
    'VBG': 'Verb, gerund or present participle',
    'VBN': 'Verb, past participle',
    'VBP': 'Verb, non-3rd person singular present',
    'VBZ': 'Verb, 3rd person singular present',
    'WDT': 'Wh-determiner',
    'WP': 'Wh-pronoun',
    'WP$': 'Possessive wh-pronoun',
    'WRB': 'Wh-adverb'
}

# Function for Tokenization
def perform_tokenization(text):
    # Tokenizes the input text into individual words
    tokens = word_tokenize(text)
    tokenized_df = pd.DataFrame(tokens, columns=["Tokens"])
    return tokenized_df
    create_download_button(tokenized_df, "tokenized_output.xlsx", "Download Tokenized Data as Excel")


# Function for POS Tagging
def perform_pos_tagging(text):
    # Tokenizes the input text and tags each word with its part of speech
    tokens = word_tokenize(text)
    tagged = nltk.pos_tag(tokens)

    
    # Convert to DataFrame for better visual presentation
    tagged_df = pd.DataFrame(tagged, columns=["Word", "POS"])
    
    # Display the full form of each POS tag abbreviation
    pos_info = "\n".join([f"{key}: {value}" for key, value in pos_abbreviations.items()])
    
    st.text_area("POS Tag Abbreviations (Full Forms)", pos_info, height=300)

    # Calculate POS tag distribution
    pos_counts = tagged_df['POS'].value_counts()

    # Limit to top 10 POS tags
    top_10_pos_counts = pos_counts.head(10)

    # Plot the distribution as a pie chart
    st.text_area("Pie Chart Distribution of Top 10 POS: ", height=30)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(top_10_pos_counts, labels=top_10_pos_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3", len(top_10_pos_counts)))
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
    st.pyplot(fig)

    return tagged_df
    create_download_button(tagged_df, "pos_tagged_output.xlsx", "Download POS-Tagged Data as Excel")


# Function for Lemmatization
def perform_lemmatization(text):
    # Lemmatizes the input text by reducing words to their root form
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = word_tokenize(text)
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens]
    lemmatized_df = pd.DataFrame({"Original Word": tokens, "Lemmatized Word": lemmatized})
    return lemmatized_df
    create_download_button(lemmatized_df, "lemmatized_output.xlsx", "Download Lemmatized Data as Excel")

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
    create_download_button(freq_df, "word_frequency_output.xlsx", "Download Word Frequency Data as Excel")

# Function for Stopword Removal
def perform_stopword_removal(text):
    # Removes common stopwords like "the", "a", etc. from the text
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text)
    filtered_words = [word for word in tokens if word.lower() not in stop_words]
    
    # Create a pandas DataFrame with original words and filtered words
    stopword_removal_df = pd.DataFrame({
        "Original Word": tokens,
        "Filtered Word": [word if word.lower() not in stop_words else "" for word in tokens] # Output as a space-separated string
    })
    return stopword_removal_df
    create_download_button(stopword_removal_df, "stopword_removal_output.xlsx", "Download Stopword Removal Data as Excel")

# Function for Stemming
def perform_stemming(text):
    # Reduces words to their stem (root) form using the Porter Stemmer
    ps = PorterStemmer()
    tokens = word_tokenize(text)
    stemmed = [ps.stem(word) for word in tokens]
    stemming_df = pd.DataFrame({
        "Original Word": tokens,
        "Stemmed Word": stemmed
    })
    return stemming_df
    create_download_button(stemming_df, "stemming_output.xlsx", "Download Stemming Data as Excel")

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
