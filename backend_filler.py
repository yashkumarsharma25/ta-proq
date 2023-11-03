from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time 
import os
from utils import md2html

class Filler:
    def __init__(self,user_data_dir=None,profile_directory="Default") -> None:
        options = webdriver.ChromeOptions()
        if not user_data_dir:
            user_data_dir = f"/home/{os.getlogin()}/.config/google-chrome/"
        # Path To Custom Profile
        options.add_argument(f"user-data-dir={user_data_dir}")
        options.add_argument(f"profile-directory={profile_directory}")
        self.driver = webdriver.Chrome(options=options)

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

    def fill_input(self,name, content):
        try:
            input_field = self.driver.find_element(By.NAME, name)
            input_field.clear()
            input_field.send_keys(content)
        except Exception as e:
            print(f"Error filling input for {name}: {e}")

    def click_link(self,link_text, n=1,wait=False):
        if wait:
            link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, link_text))
            )
        else:
            link = self.driver.find_element(By.LINK_TEXT, link_text)
        for _ in range(n):
            link.click()

    def fill_text_area(self,name,content):
        textarea = self.driver.find_element(By.NAME,name)
        textarea.clear()
        textarea.send_keys(content)

    def fill_code_mirror(self,text):
        codeMirror = self.driver.find_element(By.CLASS_NAME,"CodeMirror")
        codeLine = codeMirror.find_elements(By.CLASS_NAME,"CodeMirror-lines")[0]
        codeLine.click()
        txtbx = codeMirror.find_element(By.CSS_SELECTOR,"textarea")
        txtbx.send_keys(md2html(text))

class ProgAssignFiller(Filler):

    def from_cookie(self,url,cookies):
        self.driver.get(url)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.get(url)
        
        
    def load_data_file(self,data_file):
        with open(data_file,"r") as f:
            return json.load(f)
        
    def load_data(self, data_path):
        if os.path.isfile(data_path):
            self.proqs = [self.load_data(data_path)]
        if os.path.isdir(data_path):
            self.proqs = [
                self.load_data_file(os.path.join(data_path,data_file)) 
                for data_file in os.listdir(data_path)
            ]
        
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
        n_public = len(list(filter(lambda x: x.get("isPublic"), testcases)))
        n_private =len(testcases) - n_public
        self.click_link("Add Public Test Case", n_public)  
        self.click_link("Add Private Test Case", n_private)  

        for i,t in enumerate(filter(lambda x: x["isPublic"], testcases)):
            self.set_testcase_content(i,"input",t["isPublic"],t["input"])
            self.set_testcase_content(i,"output",t["isPublic"],t["output"])

        for i,t in enumerate(filter(lambda x: not x["isPublic"], testcases)):
            self.set_testcase_content(i,"input",t["isPublic"],t["input"])
            self.set_testcase_content(i,"output",t["isPublic"],t["output"])

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

    def add_unit(self):
        add_unit_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="add_unit"]/button'))
        )
        add_unit_btn.click()
        self.click_link("Save",wait=True)
        self.driver.back()
        self.driver.refresh()

    def wait_till_proq_loaded(self):
        # wait till the save buttion is available
        WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Save"))
            )
    
    def create_open_proq(self):
        # wait till loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ol[@class="course ui-sortable"]'))
        )

        last_unit = self.driver.find_element(By.XPATH,'//ol[@class="course ui-sortable"]/li[last()]')
        add_proq_form = last_unit.find_element(By.XPATH,'.//form[@id="add_custom_unit_com.google.coursebuilder.programming_assignment"]')
        add_proq_form.submit()
        
        self.wait_till_proq_loaded()
        

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
        urls = [
            unit.find_elements(By.XPATH,f".//a[contains(text(), '{proq}')]").get_attribute("href") 
            for proq in proqs
        ]
        return urls 

    def save_proq(self):
        self.click_link("Save")
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="gcb-butterbar-message"]'), 'Saved.')
        )

    def fill_data(self,data):
        self.fill_input("title", data["title"])
        self.set_problem_statement(data["statement"])
        
        # defaults
        self.select_value("content:evaluator", "nsjail")
        self.select_value("workflow:evaluation_type", "Test Cases")
        self.check_value("html_check_answers", True)
        self.check_value("content:ignore_presentation_errors", True)
        self.check_value("content:show_sample_solution", True)

        self.set_date_time(data["deadline"])
        self.set_testcases(data["testcases"])
        self.set_code_content(data["code"])
        
        self.save_proq()
        

    def create_proqs(self):
        self.add_unit()
        for proq in self.proqs:
            self.create_open_proq()
            try:
                self.fill_data(proq)
                self.driver.back()
                self.driver.refresh()
            except:
                print(f"problem in {proq['title']}")
                input("Press enter to continue")
                

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

