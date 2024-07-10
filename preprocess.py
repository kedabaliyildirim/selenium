import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from langdetect import detect
class Preprocess:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
    @staticmethod
    def tweet_preprocess(df):
        # Drop non-English tweets
        lang_detect = df['tweet_text'].apply(lambda x: detect(x))
        # Remove duplicate text and missing values
        df.drop_duplicates(subset=['tweet_text'], keep='first', inplace=True)
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        #extract hashtags
        df['hashtags'] = df['tweet_text'].apply(lambda x: ' '.join([word for word in x.split() if word.startswith('#')]))

        #extract mentions
        df['mentions'] = df['tweet_text'].apply(lambda x: ' '.join([word for word in x.split() if word.startswith('@')]))

        #extract links
        df['links'] = df['tweet_text'].apply(lambda x: ' '.join([word for word in x.split() if word.startswith('http')]))

        #delete hashtags, mentions and links from tweet text
        df['tweet_text'] = df['tweet_text'].apply(lambda x: ' '.join([word for word in x.split() if not word.startswith('#') and not word.startswith('@') and not word.startswith('http')]))

        

        # Normalize dates
        df['creation_date'] = pd.to_datetime(df['created_at']).dt.date
        df['creation_time'] = pd.to_datetime(df['created_at']).dt.time
        
        # Convert text to lowercase
        df["tweet_text"] = df["tweet_text"].str.lower()
        

        

        # Remove non-alphanumeric characters
        df["tweet_text"] = df["tweet_text"].str.replace("[^a-zA-Z0-9]", " ", regex=True)
        
        # Strip leading and trailing spaces
        df["tweet_text"] = df["tweet_text"].str.strip()
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        df["tweet_text"] = df["tweet_text"].apply(lambda x: " ".join([word for word in x.split() if word not in stop_words]))
        
        # Lemmatize words
        lemmatizer = WordNetLemmatizer()
        df["tweet_text"] = df["tweet_text"].apply(lambda x: " ".join([lemmatizer.lemmatize(word) for word in word_tokenize(x)]))

        return df
    def user_preprocess(self, df):
        df.dropna(inplace=True)
        # replace seperators to . from , in numbers and  Convert follower and following counts
        df['followers'] = df['followers'].str.replace(',', '').str.replace('M', 'e6').str.replace('K', 'e3').astype(float)
        df['following'] = df['following'].str.replace(',', '').str.replace('M', 'e6').str.replace('K', 'e3').astype(float)
        df['posts'] = df['posts'].str.replace(',', '').str.replace('M', 'e6').str.replace('K', 'e3').astype(float)
        return df