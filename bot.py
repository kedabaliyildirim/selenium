from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from config import Config

class Bot:
    def __init__(self):
        self.config = Config()
        self.driver = self.init_driver()
        self.wait = WebDriverWait(self.driver, 10)

    def init_driver(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(1.5)
        return driver

    def login(self):
        self.driver.get("https://x.com/login")
        wait = WebDriverWait(self.driver, 10.5)
        twitter_handle = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']")))
        twitter_handle.send_keys(self.config.handle)
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        next_button.click()
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='current-password']")))
        password_field.send_keys(self.config.password)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']")))
        login_button.click()
        time.sleep(2)

    def close(self):
        self.driver.quit()
