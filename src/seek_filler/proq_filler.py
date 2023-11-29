from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


import json
import os
from web_fillers import Filler
from .proq_to_json import proq_to_json
from .utils import md2html

class ProqFiller(Filler):

    def from_cookie(self,url,cookies):
        self.driver.get(url)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.get(url)
        
        
    def load_data(self,proq_file):
        self.unit_name, self.proqs = proq_to_json(proq_file)
        for i, proq in enumerate(self.proqs):
            self.proqs[i]["statement"] = md2html(proq["statement"])
        
    def open_dashboard():
        ...
    def check_value(self,name, state=True):
        try:
            checkbox = self.driver.find_element(By.NAME, name)
            checkbox_sibling = checkbox.find_element(By.XPATH,"./preceding-sibling::input[@type='checkbox']")
            if ((checkbox.get_dom_attribute("value")=="true") != state):
                checkbox_sibling.click()
        except Exception as e:
            print(f"Error checking value for {name}: {e}")

    def set_date_time(self,date_time= "09/17/2023,14:30"):
        date , time = date_time.split(",")
        js_code = f"""
        document.querySelector('input[name="workflow:submission_due_date[0]"]').value = '{date}';
        document.querySelector('select[name="workflow:submission_due_date[1][0]"]').value = '{time.split(":")[0]}';
        document.querySelector('select[name="workflow:submission_due_date[1][1]"]').value = '{time.split(":")[1]}';
        """
        self.driver.execute_script(js_code)

    def set_testcase_content(self,testcase_no, content_type, is_public, content):
            if is_public:
                name_attribute = f"content:public_testcase[{testcase_no}]{content_type}"
            else:
                name_attribute = f"content:private_testcase[{testcase_no}]{content_type}"
            self.fill_text_area(name_attribute,content)

    def set_testcases(self,testcases):
        self.click_link("Add Public Test Case", len(testcases["public_testcases"]))  
        self.click_link("Add Private Test Case", len(testcases["public_testcases"]))  

        for i,t in enumerate(testcases["public_testcases"]):
            self.set_testcase_content(i,"input",True,t["input"])
            self.set_testcase_content(i,"output",True,t["output"])

        for i,t in enumerate(testcases["private_testcases"]):
            self.set_testcase_content(i,"input",False,t["input"])
            self.set_testcase_content(i,"output",False,t["output"])

    def set_code_content(self,template):
        
        textarea_mapping = {
            "prefix": "content:allowed_languages[0]prefixed_code",
            "template": "content:allowed_languages[0]code_template",
            "suffix": "content:allowed_languages[0]uneditable_code",
            "suffixInvisible": "content:allowed_languages[0]suffixed_invisible_code",
            "solution": "content:allowed_languages[0]sample_solution"
        }
        for k in template.keys():
            self.fill_text_area(textarea_mapping[k],template[k])

    def set_problem_statement(self,statement):
        html_button = self.driver.find_element(By.XPATH,"//button[text()='code']")
        html_button.click()
        self.fill_code_mirror(statement)

    def wait_till_outline_loaded(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="add_unit"]/button'))
        )

    def add_unit(self,unit_name):
        add_unit_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="add_unit"]/button'))
        )
        add_unit_btn.click()
        WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Save"))
        )
        self.fill_input_by_name("title",unit_name)
        self.click_link("Save",wait=True)
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="gcb-butterbar-message"]'), 'Saved.')
        )
        self.driver.back()
        self.driver.refresh()

        
    def get_proq_urls(self,unit_name, proqs):
        xpath = f"//a[contains(text(), '{unit_name}')]/parent::*/parent::*/following-sibling::ol"
        unit = self.driver.find_element(By.XPATH, xpath)
        urls = [
            unit.find_element(By.XPATH,f".//a[contains(text(), '{proq}')]").get_attribute("href") 
            for proq in proqs
        ]
        return urls 

    def get_all_proq_urls(self,unit_name):
        xpath = f"//a[contains(text(), '{unit_name}')]/parent::*/parent::*/following-sibling::ol"
        unit = self.driver.find_element(By.XPATH, xpath)
        urls = [unit.find_elements(By.XPATH,f".//a").get_attribute("href")]
        return urls 


    def wait_till_proq_loaded(self,timeout):
        # wait till the save buttion is available
        WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Save"))
            )

    def save_proq(self):
        self.click_link("Save")
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="gcb-butterbar-message"]'), 'Saved.')
        )

    def fill_data(self,data):
        while True:
            try:
                self.wait_till_proq_loaded(1)
                break
            except:
                try:
                    # for non secure sites.
                    self.click_by_xpath_text("button","Continue to site", 1)
                except:
                    pass
            
        self.fill_input_by_name("title", data["title"])
        self.set_problem_statement(data["statement"])
        
        # defaults
        self.select_value("content:evaluator", "nsjail")
        self.select_value("workflow:evaluation_type", "Test cases")
        self.check_value("html_check_answers", True)
        self.check_value("content:ignore_presentation_errors", True)
        self.check_value("content:show_sample_solution", True)
        
        self.select_value("content:allowed_languages[0]language",data["lang"])
        self.set_date_time(data["deadline"])
        self.set_testcases(data["testcases"])
        self.set_code_content(data["code"])
        
        self.save_proq()
        

    def create_open_proqs(self):
        # wait till loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ol[@class="course ui-sortable"]'))
        )
        last_unit = self.driver.find_element(By.XPATH,'//ol[@class="course ui-sortable"]/li[last()]')
        button = last_unit.find_element(By.XPATH,'.//form[@id="add_custom_unit_com.google.coursebuilder.programming_assignment"]/button')
        for i in range(len(self.proqs)):
            ActionChains(self.driver) \
                .key_down(Keys.CONTROL) \
                .click(button) \
                .key_up(Keys.CONTROL) \
                .perform()
        

    def create_proqs(self,create_unit=True):
        if create_unit:
            self.add_unit(self.unit_name)
        self.create_open_proqs()
        for i,proq in enumerate(self.proqs,1):
            self.driver.switch_to.window(self.driver.window_handles[i])
            try:
                self.fill_data(proq)
            except:
                print(f"problem in {proq['title']}")
                

if __name__ == "__main__":

    # Procedure
    url = "https://backend.seek.onlinedegree.iitm.ac.in/22python_mock/dashboard"
    # cookies = [{
    #     'name': 'id_token',
    #     'value': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImFhMDhlN2M3ODNkYjhjOGFjNGNhNzJhZjdmOWRkN2JiMzk4ZjE2ZGMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTGl2aW4gTmVjdG9yIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FBY0hUdGMwZE9pbjJ2YWd3Q1pnSjE1VEo2Y1FwS3YwMVVSU0NtOUEwWElXdzFRPXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3NlZWstb2RlLXByb2QtYXV0aCIsImF1ZCI6InNlZWstb2RlLXByb2QtYXV0aCIsImF1dGhfdGltZSI6MTY5NDk0MDgxNCwidXNlcl9pZCI6Ikg0cnNZdzE2TWRTU1cwckRUWjZjajQ0ZXJXYTIiLCJzdWIiOiJINHJzWXcxNk1kU1NXMHJEVFo2Y2o0NGVyV2EyIiwiaWF0IjoxNjk0OTU0ODQxLCJleHAiOjE2OTQ5NTg0NDEsImVtYWlsIjoibGl2aW5Ac3R1ZHkuaWl0bS5hYy5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTEzMTEzNzQ1MzczNDY4MzY1NTMxIl0sImVtYWlsIjpbImxpdmluQHN0dWR5LmlpdG0uYWMuaW4iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.ldPRBPM2yfXN43hFGusRRZ6zBGZ2WyTSBY3ped4FVIRpa0s2In-hX3cT9k7xaMb2FR1MZx9j1MUwcopFwmha4GV35sRCLuLJFX4qRmSRjsZSprLRKLC8mOXRh5D12qVl4NYJIQF5O_BndH_NBsNslNyJCgRiPp0eejrc1f75nbt4DofVkjALTuOrS_zY-dyOfNpUlUjZagw5tPwv6s8imTFtv6mEBqBY9n2jas0boUj26H0aVTu2gtgL8g8aOc6gINZx2X0Kc54pbXBMZjzXpmrYCBAWHUNXVSIJKMdT6peLr3qnB_3YqGNsXysPSEgmoWlQvo0qQHp449Mm_ywGfQ',
    #     'domain': 'backend.seek.onlinedegree.iitm.ac.in', 
    #     'path': '/'
    # }]

    # filler = ProgAssignFiller("data.json",url,cookies)
    # print("enter exit to exit.")
    # while True:
    #     a = input(">")
    #     if a == "fill":
    #         filler.fill_data()
    #     elif a =="exit":
    #         filler.driver.close()
    #         break

