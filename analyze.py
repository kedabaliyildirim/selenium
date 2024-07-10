import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class Analyze:
    def generate_wordcloud(self, df):
        """
        Generate a word cloud from tweet texts.

        :param df: DataFrame containing tweet data with a 'tweet_text' column
        """
        wordcloud = WordCloud(width=800, height=400, max_words=200, background_color='white').generate(" ".join(df["tweet_text"]))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title("Word Cloud of Tweets")
        plt.show()

    def generate_sentiment_plot(self, df):
        """
        Generate a bar plot of sentiment categories.

        :param df: DataFrame containing tweet data with a 'sentiment_category' column
        """
        plt.figure(figsize=(10, 5))
        df['sentiment_category'].value_counts().plot(kind='bar')
        plt.title("Sentiment Analysis")
        plt.xlabel("Sentiment")
        plt.ylabel("Count")
        plt.show()

    def generate_tweet_count_plot(self, df):
        """
        Generate a bar plot of tweet counts by creation date.

        :param df: DataFrame containing tweet data with a 'creation_date' column
        """
        plt.figure(figsize=(10, 5))
        df['creation_date'].value_counts().plot(kind='bar')
        plt.title("Tweet Count by Date")
        plt.xlabel("Date")
        plt.ylabel("Count")
        plt.show()

    def convert_to_int(self, value):
        """
        Convert follower, following, and post counts from float to integer.

        :param value: float value (e.g., 1.500, 2.300)
        :return: Integer value
        """
        try:
            return int(value)
        except ValueError:
            return int(float(value))

    def generate_user_data_plot(self, df):
        """
        Generate bar plots for followers, following, and posts counts.

        :param df: DataFrame containing user data with 'followers', 'following', and 'posts' columns
        """
        df['followers'] = df['followers'].apply(self.convert_to_int)
        df['following'] = df['following'].apply(self.convert_to_int)
        df['posts'] = df['posts'].apply(self.convert_to_int)

        plt.figure(figsize=(15, 5))
        
        plt.subplot(1, 3, 1)
        df['followers'].plot(kind='bar')
        plt.title("Followers Count")
        plt.xlabel("User")
        plt.ylabel("Count")
        
        plt.subplot(1, 3, 2)
        df['following'].plot(kind='bar')
        plt.title("Following Count")
        plt.xlabel("User")
        plt.ylabel("Count")

        plt.subplot(1, 3, 3)
        df['posts'].plot(kind='bar')
        plt.title("Posts Count")
        plt.xlabel("User")
        plt.ylabel("Count")

        plt.tight_layout()
        plt.show()

    def plot_data_with_sub_plots(self, df):
        """
        Generate subplots for sentiment analysis, tweet counts, followers, and following.

        :param df: DataFrame containing tweet and user data
        """
        fig, axs = plt.subplots(2, 2, figsize=(15, 10))

        df['sentiment_category'].value_counts().plot(kind='bar', ax=axs[0, 0])
        axs[0, 0].set_title("Sentiment Analysis")
        axs[0, 0].set_xlabel("Sentiment")
        axs[0, 0].set_ylabel("Count")

        df['creation_date'].value_counts().plot(kind='bar', ax=axs[0, 1])
        axs[0, 1].set_title("Tweet Count by Date")
        axs[0, 1].set_xlabel("Date")
        axs[0, 1].set_ylabel("Count")

        df['followers'] = df['followers'].apply(self.convert_to_int)
        df['following'] = df['following'].apply(self.convert_to_int)
        df['posts'] = df['posts'].apply(self.convert_to_int)
        
        df['followers'].plot(kind='bar', ax=axs[1, 0])
        axs[1, 0].set_title("Followers Count")
        axs[1, 0].set_xlabel("User")
        axs[1, 0].set_ylabel("Count")
        
        df['following'].plot(kind='bar', ax=axs[1, 1])
        axs[1, 1].set_title("Following Count")
        axs[1, 1].set_xlabel("User")
        axs[1, 1].set_ylabel("Count")

        plt.tight_layout()
        plt.show()


    def create_all_plots(self, df):
        """
        Generate all plots for sentiment analysis, tweet counts, followers, and following.

        :param df: DataFrame containing tweet and user data
        """
        plot_consent = input("all proceedings are completed, this will generate multiple plots. Proceed? (y/n): ")

        if plot_consent.lower() != 'y':
            print("Exiting...")
            return
        
        self.generate_wordcloud(df)
        self.generate_sentiment_plot(df)
        self.generate_tweet_count_plot(df)
        self.generate_user_data_plot(df)
        self.plot_data_with_sub_plots(df)