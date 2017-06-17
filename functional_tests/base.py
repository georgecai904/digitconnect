from selenium import webdriver
from django.test import TestCase


class FunctionalTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(FunctionalTest, cls).setUpClass()
        cls.browser = webdriver.Chrome(executable_path="/driver/chromedriver")
        cls.live_server_url = "http://localhost:8000"

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(FunctionalTest, cls).tearDownClass()
