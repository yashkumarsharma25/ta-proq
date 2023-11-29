from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


import os

class Filler:
    def __init__(self,user_data_dir=None,profile_directory="Default") -> None:
        options = webdriver.ChromeOptions()
        if not user_data_dir:
            if os.name == "posix": # linux
                user_data_dir = f"/home/{os.getlogin()}/.config/google-chrome/"
            elif os.name == "nt": # windows
                user_data_dir = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data"
        # Path To Custom Profile
        options.add_argument(f"user-data-dir={user_data_dir}")
        options.add_argument(f"profile-directory={profile_directory}")
        self.driver = webdriver.Chrome(options=options)

    def get_elem_by_xpath(self,xpath, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
        )
    
    def get_elem_by_name(self,name,timeout=10):
        return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.NAME, name))
        )

    def select_value(self,name, text):
        try:
            select_element = Select(self.driver.find_element(By.NAME, name))
            select_element.select_by_visible_text(text)
        except Exception as e:
            print(f"Error selecting value from {name}: {e}")

    def check_value(self,name, state=True):
        try:
            checkbox = self.driver.find_element(By.NAME, name)
            if (checkbox.is_selected() and not state) or (not checkbox.is_selected() and state):
                checkbox.click()
        except Exception as e:
            print(f"Error checking value for {name}: {e}")

    def fill_input_by_name(self,name, content):
        try:
            input_field = self.driver.find_element(By.XPATH, f"(//textarea|//input)[@name='{name}']")
            input_field.clear()
            input_field.send_keys(content)
        except Exception as e:
            print(f"Error filling input for {name}: {e}")
    
    def fill_input_by_placeholder(self,placeholder, content):
        try:
            input_field = self.driver.find_element(By.XPATH, f"(//textarea |//input)[@placeholder='{placeholder}']")
            input_field.send_keys(Keys.CONTROL+"a")
            input_field.send_keys(content)
        except Exception as e:
            print(f"Error filling input for {placeholder}: {e}")

    def click_link(self,link_text, n=1,wait=False):
        if wait:
            link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, link_text))
            )
        else:
            link = self.driver.find_element(By.LINK_TEXT, link_text)
        for _ in range(n):
            link.click()
    
    def click_by_xpath_text(self,element, text,timeout=10):
        elem = self.get_elem_by_xpath(f"//{element}[contains(.,'{text}')]",timeout=timeout)
        elem.click()

    def fill_text_area(self,name,content):
        textarea = self.driver.find_element(By.NAME,name)
        textarea.clear()
        textarea.send_keys(content)

    def fill_code_mirror(self,text):
        codeMirror = self.driver.find_element(By.CLASS_NAME,"CodeMirror")
        codeLine = codeMirror.find_elements(By.CLASS_NAME,"CodeMirror-lines")[0]
        codeLine.click()
        txtbx = codeMirror.find_element(By.CSS_SELECTOR,"textarea")
        txtbx.send_keys(text)