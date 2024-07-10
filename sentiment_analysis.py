from textblob import TextBlob
import pandas as pd
class TwitterSentimentAnalsis:
    def __init__(self):
        pass
    def sentiment_analysis(self,df):
        
        sentiment_df = pd.DataFrame()
        sentiment_df['tweet_text'] = df['tweet_text']
        sentiment_df["sentiment"] = sentiment_df["tweet_text"].apply(lambda x: TextBlob(x).sentiment.polarity)
        sentiment_df["sentiment_category"] = sentiment_df["sentiment"].apply(lambda x: "positive" if x > 0 else "negative" if x < 0 else "neutral")
        return sentiment_df