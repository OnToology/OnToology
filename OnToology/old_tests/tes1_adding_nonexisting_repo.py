# # -*- coding: utf-8 -*-
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import NoAlertPresentException
# import unittest, time, re
# import os
#
#
# class Test1AddingNonexistingRepo(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Firefox()
#         self.driver.implicitly_wait(30)
#         self.base_url = "http://ontoology.linkeddata.es/"
#         self.verificationErrors = []
#         self.accept_next_alert = True
#
#     def test_1_adding_nonexisting_repo(self):
#         msg = "You don't have permission to add collaborators and create"
#         driver = self.driver
#         driver.get(self.base_url + "/")
#         driver.find_element_by_id("target_repo_select").click()
#         driver.find_element_by_id("target_repo_select").clear()
#         driver.find_element_by_id("target_repo_select").send_keys("ahmad88me/fake12")
#         driver.find_element_by_css_selector("input.form-control.btn").click()
#         driver.find_element_by_id("login_field").clear()
#         driver.find_element_by_id("login_field").send_keys(os.environ['test_github_username'])
#         driver.find_element_by_id("password").click()
#         driver.find_element_by_id("password").clear()
#         driver.find_element_by_id("password").send_keys(os.environ['test_github_password'])
#         driver.find_element_by_name("commit").click()
#         for t in driver.find_elements_by_tag_name("h2"):
#             if msg in t.text:
#                 return True
#         self.assertEqual('a', 'b')
#
#
#     def is_element_present(self, how, what):
#         try: self.driver.find_element(by=how, value=what)
#         except NoSuchElementException as e: return False
#         return True
#
#     def is_alert_present(self):
#         try: self.driver.switch_to_alert()
#         except NoAlertPresentException as e: return False
#         return True
#
#     def close_alert_and_get_its_text(self):
#         try:
#             alert = self.driver.switch_to_alert()
#             alert_text = alert.text
#             if self.accept_next_alert:
#                 alert.accept()
#             else:
#                 alert.dismiss()
#             return alert_text
#         finally: self.accept_next_alert = True
#
#     def tearDown(self):
#         self.driver.quit()
#         self.assertEqual([], self.verificationErrors)
#
# if __name__ == "__main__":
#     unittest.main()
