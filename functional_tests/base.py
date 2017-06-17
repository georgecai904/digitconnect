from selenium import webdriver
from django.test import LiveServerTestCase, TestCase
import time


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

    # def test_django_server_is_working(self):
    #     self.browser.get(self.live_server_url)
    #     self.assertIn("Django", self.browser.title)
