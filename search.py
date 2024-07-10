import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
class Search:
    def __init__(self, bot):
        self.bot = bot

    def search_advanced_param_getter(self):
        self.bot.driver.get("https://x.com/search-advanced")
        wait = WebDriverWait(self.bot.driver, 5)
        
        # Switch to iframe if present
        try:
            iframe = self.bot.driver.find_element(By.TAG_NAME, "iframe")
            self.bot.driver.switch_to.frame(iframe)
        except NoSuchElementException:
            print("No iframe found, continuing with main content.")
        
        # Locate all text and number input fields
        try:
            text_fields = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))
        except TimeoutException:
            print("Timeout waiting for text input fields to be present.")
            text_fields = []
        
        try:
            number_inputs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='number']")))
        except TimeoutException:
            print("Timeout waiting for number input fields to be present.")
            number_inputs = []
        
        # Retrieve labels and map them to input fields
        labels = self.bot.driver.find_elements(By.XPATH, "//label")
        input_list = []

        for label in labels:
            input_type = None
            element = None

            # Check if label corresponds to a text input
            if text_fields:
                try:
                    text_field = label.find_element(By.XPATH, ".//input[@type='text']")
                    input_type = "text"
                    element = text_fields.pop(0).get_property("name")
                except NoSuchElementException:
                    pass

            # Check if label corresponds to a number input
            if number_inputs and not input_type:
                try:
                    number_input = label.find_element(By.XPATH, ".//input[@type='number']")
                    input_type = "number"
                    element = number_inputs.pop(0).get_property("name")
                except NoSuchElementException:
                    pass

            if input_type and element:
                input_list.append([label.text, input_type, element])

        input_df = pd.DataFrame(input_list, columns=["label", "element_type", "element"])
        print(f"Found {len(text_fields)} text inputs, {len(number_inputs)} number inputs")
        
        # Switch back to default content
        self.bot.driver.switch_to.default_content()
        return input_df
    def search_adv(self, input_df):
        print("@search_adv")
        for index, row in input_df.iterrows():
            element_name = row["element"]
            inputs = row["inputs"]
            if inputs == "":
                continue
            search_input = WebDriverWait(self.bot.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//input[@name='{element_name}']"))
            )
            search_input.send_keys(inputs)
        search_button = self.bot.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Search']")))
        search_button.click()

    def search_param_initialization(self, input_df):
        input_list = []
        for index, row in input_df.iterrows():
            prompt = row["label"]
            element_name = row["element"]
            element_type = row["element_type"]

            try:
                user_input = input(f"Enter {'number' if element_type == 'number' else 'search term'} for {prompt}: ")
                if element_type == "number":
                    try:
                        user_input = int(user_input)
                        if user_input < 0:
                            raise ValueError("Number must be positive.")

                        elif user_input == "":
                            user_input = 0
                    except ValueError:
                        print("Invalid number entered, defaulting to 0.")
                        user_input = 0

                print(f"Entered {'number' if element_type == 'number' else 'search term'} for {prompt}: {user_input}")
                input_list.append(user_input)
            except Exception as e:
                print(f"An error occurred while processing {prompt}: {e}")

        input_df["inputs"] = input_list

        self.search_adv(input_df)

    def clear_inputs(self, input_df):
        for index, row in input_df.iterrows():
            element_name = row["element"]
            try:
                search_input = WebDriverWait(self.bot.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//input[@name='{element_name}']"))
                )
                search_input.clear()
            except Exception as e:
                print(f"An error occurred while clearing {element_name}: {e}")

    def search_advanced_initialization(self):
        start_time = time.time()
        input_df = self.search_advanced_param_getter()
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for search_advanced_initialziation: {execution_time} seconds")
        start_time = time.time()
        self.search_param_initialization(input_df)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for search_param_initialziation: {execution_time} seconds")

    def search_basic(self):
        search_input = self.bot.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
        user_input = input("Enter search term: ")
        search_input.send_keys(user_input)
        search_input.send_keys(Keys.ENTER)

    def search_selection(self):
        search_type = input("Enter search type (0 for basic/ 1 for advanced): ")
        if search_type == "0":
            self.search_basic()
        elif search_type == "1":
            self.search_advanced_initialization()
        else:
            print("Invalid selection, defaulting to basic search.")
            self.search_basic()