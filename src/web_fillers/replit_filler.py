from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .filler import Filler

class ReplitFiller(Filler):
    def select_replit_dropdown(self,value):
        elem = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'.dropdown-container'))
            )
        elem.click()
        elem = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'//li/a[contains(text(),"{value}")]'))
            )
        elem.click()
    
    def fill_testcases(self,testcases):
        self.click_by_xpath_text("button","Tests")
        self.click_by_xpath_text("h4",'Input output tests')
        for i,testcase in enumerate(testcases,1):
            self.click_by_xpath_text("button","Create test")
            self.fill_input_by_placeholder("The name of the test",f"Test case {i}")
            self.fill_input_by_placeholder("The input for the test",testcase["input"])
            self.fill_input_by_placeholder("The expected output for the test",testcase["output"])
            self.select_replit_dropdown("exact")
            self.click_by_xpath_text("button","Save")

    