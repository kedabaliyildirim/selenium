from bot import Bot
from search import Search
from get_data import GetData
from preprocess import Preprocess
from analyze import Analyze
from sentiment_analysis import TwitterSentimentAnalsis
import pandas as pd
import time
def main():
    start_time = time.time()
    # Initialize the bot and login
    bot = Bot()
    bot.login()

    # Perform advanced search
    search = Search(bot)
    search.search_selection()

    # initilazie data getter class with bot object
    get_data = GetData(bot)
    
    #get tweet data without user data
    tweet_df = get_data.aggregate_tweet_data()

    # Preprocess data
    preprocess = Preprocess()
    cleaned_df = preprocess.tweet_preprocess(tweet_df)

    #get user data
    user_data_df = get_data.get_all_users_data(username_list=cleaned_df['username'].unique())

    # Close the bot
    bot.close()

    # Preprocess user data to process suffixes such as K, M
    cleaned_user_data = preprocess.user_preprocess(df=user_data_df)
    
    # Save data to csv
    cleaned_df.to_csv("cleaned_data.csv", index=False)
    cleaned_user_data.to_csv("user_data.csv", index=False)
    
    #merge user data with tweet data
    merged_df = cleaned_df.merge(cleaned_user_data, on='username')


    # Sentiment analysis
    sentiment_analysis = TwitterSentimentAnalsis()
    
    sentiment_df = sentiment_analysis.sentiment_analysis(df=merged_df)
    sentiment_df.to_csv("sentiment_data.csv", index=False)
    print("Data saved to cleaned_data.csv = preprocessed data, user_data.csv = user statistics, \
           merged_data.csv = user statistics + preprocessed data, sentiment_data.csv sentiment analysis data and")
    # Merge sentiment data with tweet data
    merged_sentiment_df = merged_df.merge(sentiment_df, on='tweet_text')
    merged_sentiment_df.to_csv("merged_data.csv", index=False)    
    
    # Analyze data
    analyze = Analyze()
    analyze.create_all_plots(df=merged_sentiment_df)


    print("Analysis complete")
    end_time = time.time()
    print(f"Time taken (including input duration): {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
