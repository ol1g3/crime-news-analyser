import pandas as pd
import numpy as np

import string
import re
import spacy
import compound_splitter # custom library, Kompositazerlegung

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import pickle


np.random.seed(42)

stopwords = open('assets/stopwords-de.txt', 'r').readlines()
stopwords = [x[:-1] for x in stopwords] # erase \n
nlp = spacy.load('assets/de_core_news_sm')

automaton = compound_splitter.make_auto('assets/wordlist-german.txt')

def get_simple_words(s):
    """
    Returns a simplified version of the input string by splitting compound words.
    
    Args:
        s (str): The input string to be processed.
        
    Returns:
        str: The simplified version of the input string with compound words split.
    """
    
    ans = compound_splitter.solve(s.lower(), automaton)

    # return s if splitting was not successful, otherwise return words forming the compound
    return s if ans == [] else ' '.join(ans)

def modify_text(text: str):
    """
    Modifies the given text by removing numbers, punctuation, converting to lowercase,
    removing stopwords, lemmatizing and removing extra whitespaces.

    Args:
        text (str): The text to be modified.

    Returns:
        str: The modified text.
    """

    # Remove numbers and alphanumeric characters
    text = re.sub(r'\d+\w*', '', text)    
    
    # Remove punctuation
    text = ''.join(list(x for x in text if x not in string.punctuation+'–––'))
    
    # Convert to lowercase
    text = ''.join(list(x.lower() for x in text))

    # Splitting the compounds and filtering out the German stopwords
    text = ' '.join(list(get_simple_words(x) for x in text.split() if x not in stopwords))
    
    # Lemmatizing using Spacy German corpus
    text = ' '.join([x.lemma_ for x in nlp(text)])

    # Removing extra whitespaces 
    text = re.sub(r'\s+', ' ', text)

    return text

def model_train(path: str):
    """
    Trains a model using the data from the given file path.

    Args:
        path (str): The file path to the CSV file containing the training data.

    Returns:
        None (the model is being saved in file and later is being retrieved from it)
    """

    df_train = pd.read_csv(path)
    df_train.text = df_train.text.apply(modify_text)
    X_train, X_test, y_train, y_test = train_test_split(df_train.text, df_train.label, test_size=.2)

    # creating a pipeline for transformation and predicting via SGD model
    sgd_pipe = Pipeline([('tfidf_vec', TfidfVectorizer()), ('classifier', SGDClassifier(random_state=42))])

    # training the model
    sgd_pipe.fit(X_train, y_train)

    # saving the model
    with open('model.pkl', 'wb') as file:
        pickle.dump(sgd_pipe, file)
