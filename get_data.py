from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd

class GetData:
    def __init__(self, bot):
        self.bot = bot

    def get_user_data(self, url):
        temp_driver = self.bot.driver
        print(f"Getting data for {url}")

        # Initialize variables to None
        following_count = None
        followers_count = None
        posts_count = None

        try:
            temp_driver.get(f"https://twitter.com/{url}")
            following_element = self.bot.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@href, "/following")]/span/span')
            ))
            following_count = following_element.text.strip()

            followers_element = self.bot.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@href, "/verified_followers")]/span/span')
            ))
            followers_count = followers_element.text.strip()

            posts_element = self.bot.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[contains(text(), "posts")]')
            ))
            posts_count = posts_element.text.strip().split()[0].replace(',', '')
            print(f"Following: {following_count}, Followers: {followers_count}, Posts: {posts_count}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            return following_count, followers_count, posts_count

    def get_tweets(self, max_scrolls=2, page_scroll_multiplier=3):
        tweet_list_and_stats = []
        wait = WebDriverWait(self.bot.driver, 10)

        def scroll_down():
            scroll_height = self.bot.driver.execute_script("return window.innerHeight;")
            scroll_amount = page_scroll_multiplier * scroll_height
            self.bot.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")

        def get_tweet_data():
            attempts = 0
            max_attempts = 3
            tweets_data = []

            while attempts < max_attempts:
                try:
                    articles = WebDriverWait(self.bot.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))
                    for article in articles:
                        try:
                            tweet_date = article.find_element(By.XPATH, ".//time[@datetime]")
                            tweet_text = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']")
                            twitter_stats = article.find_element(By.XPATH, ".//div[@role='group']")
                            twitter_username_elem = article.find_element(By.XPATH, ".//div//span[contains(text(),'@')]")
                            
                            print("Processing tweet for ", twitter_username_elem.text, "... ")
                            text_strings = twitter_stats.text
                            time.sleep(1)
                            twitter_username = twitter_username_elem.text.replace("@", "")

                            text_list = text_strings.split("\n")

                            if len(text_list) >= 3:
                                tweet_replies, tweet_retweets, tweet_likes = text_list[0], text_list[1], text_list[2]
                                tweets_data.append({
                                    'tweet_text': tweet_text.text,
                                    'replies': tweet_replies,
                                    'retweets': tweet_retweets,
                                    'likes': tweet_likes,
                                    'created_at': tweet_date.get_attribute('datetime'),
                                    'username': twitter_username,
                                })
                        except StaleElementReferenceException:
                            print("StaleElementReferenceException encountered. Skipping this article.")
                        except Exception as e:
                            print("Error processing article:", e)
                    break
                except StaleElementReferenceException:
                    attempts += 1
                    print(f"StaleElementReferenceException encountered. Retrying... {attempts}/{max_attempts}")
                    time.sleep(2)
                except TimeoutException:
                    print("TimeoutException encountered. Skipping.")
                    break
                except Exception as e:
                    print("Error locating elements:", e)
                    break

            return tweets_data

        for _ in range(max_scrolls):
            tweets_data = get_tweet_data()
            tweet_list_and_stats.extend(tweets_data)
            scroll_down()

        tweet_df = pd.DataFrame(tweet_list_and_stats, columns=["tweet_text", "replies", "retweets", "likes", "created_at", "username"])
        return tweet_df

    def get_all_users_data(self, username_list):
        user_list = []
        for user in username_list:
            following, followers, posts = self.get_user_data(user)
            user_list.append([user, following, followers, posts])
        user_frame = pd.DataFrame(user_list, columns=["username", "following", "followers", "posts"])
        return user_frame
    
    def aggregate_tweet_data(self):
        try:
            page_scroll_multiplier = int(input("Enter the page scroll multiplier (the bigger number means less \
                                               duplicates but more data loss): "))
        except ValueError:
            print("Invalid input. Defaulting to 3. ")
            page_scroll_multiplier = 3
        try:
            max_scrolls = int(input("Enter the number of scrolls to perform (more scrolls more data and more time): "))
        except ValueError:
            print("Invalid input. Defaulting to 2.")
            max_scrolls = 2
        tweet_df = self.get_tweets(max_scrolls=max_scrolls,
                                    page_scroll_multiplier=page_scroll_multiplier)
        return tweet_df
