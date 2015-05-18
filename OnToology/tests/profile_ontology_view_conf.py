# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os




from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


username = os.environ['user_github_username']
password = os.environ['user_github_password']

class ProfileOntologyConf(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()#PhantomJS()
        #self.driver.implicitly_wait(5)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_profile_ontology_conf(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        
        

        
        driver.find_element_by_link_text("Login through Github").click()

        
        driver.find_element_by_id("login_field").click()
        driver.find_element_by_id("login_field").clear()
        driver.find_element_by_id("login_field").send_keys(username)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_name("commit").click()
        driver.find_element_by_css_selector("span.curfont").click()
        driver.find_element_by_xpath("//tr[2]/td[3]").click()
        driver.find_element_by_css_selector("span.bootstrap-switch-label").click()
        driver.find_element_by_css_selector("span.bootstrap-switch-handle-off.bootstrap-switch-default").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
