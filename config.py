import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        dotenv_path = './.env'
        load_dotenv(dotenv_path)
        self.handle = os.getenv("TWITTER_HANDLE")
        self.password = os.getenv("TWITTER_PASSWORD")
