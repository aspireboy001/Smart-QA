import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import string
import contractions
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

model = joblib.load('model2New.pkl')
vectorizer = joblib.load('vectorizer2New.pkl')


def get_tag(text):
    
    preprocessed_question = preprocess_text(text)
    q_text = ""
    for word in preprocessed_question:
        q_text += word + " "

    text_tfidf = vectorizer.transform([q_text]).toarray()

    # making a prediction 
    prediction = model.predict(text_tfidf)
    
    if prediction is not None:
        return prediction[0] 
    else:
        return 0 
    

def preprocess_text(text):
    
    # nltk.download('stopwords')
    
    # Expanding contractions
    text = contractions.fix(text)

    # Tokenizing the text
    words = word_tokenize(text.lower())


    stop_words = set(stopwords.words('english'))
    stop_words.update(string.punctuation)
    
    filtered_words = []

    for word in words:
        if word not in stop_words:
            filtered_words.append(word)

    # Tagging parts of speech of the filtered words
    tagged_words = pos_tag(filtered_words)

    # taking only nouns, verbs, and adjectives as keywords
    keywords = []
    for word, tag in tagged_words:
        if tag.startswith('N') or tag.startswith('J') or tag.startswith('V'):
            if word.endswith("'s"):
                keywords.append(word[:-2])
            else:
                keywords.append(word)

    # Lemmatizing the keywords
    lemmatizer = WordNetLemmatizer()

    lemma_keywords = []
    
    for word in keywords:
        lemma_keywords.append(lemmatizer.lemmatize(word))

    return lemma_keywords 




def extract_keywords(text, num_keywords):
    
    lemma_keywords = preprocess_text(text)

    # Frequency distribution of the keywords
    fdist = nltk.FreqDist(lemma_keywords)
    sorted_pairs = sorted(fdist.items(), key=lambda x: x[1], reverse=True)

    # returning top n words
    top_keywords = []
    for word,freq in sorted_pairs:
        # print(word)
        if num_keywords <= 0 : 
            break
        num_keywords -= 1;
        top_keywords.append(word)

    return top_keywords
