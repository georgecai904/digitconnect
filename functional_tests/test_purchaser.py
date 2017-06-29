from functional_tests.base import FunctionalTest
import unittest
import time


class PurchaserFunctionalTest(FunctionalTest):

    def test_purchaser_register_in(self):

        # 山姆是一个采购商，他登陆了网站
        self.browser.get(self.live_server_url)

        # 山姆看到导航栏上有"申请入驻"的标志
        # 山姆点击进去，导航栏上的"申请入驻高亮"
        self.browser.find_element_by_css_selector("nav .join-in a").click()

        # 因为山姆山姆还没有登陆，所以点进去之后是一个登陆界面
        self.assertRegex(self.browser.current_url, "/auth/login")

        # 山姆看到了页面上有用户名，密码的两个填写位置，还有忘记密码，注册，登陆按钮在他们的下方
        form = self.browser.find_element_by_tag_name("form")
        self.assertNotEqual(form.find_elements_by_id("id_username"), None)
        self.assertNotEqual(form.find_elements_by_id("id_password"), None)
        self.assertNotEqual(form.find_elements_by_id("id_forget-password"), None)
        self.assertNotEqual(form.find_elements_by_id("id_sign-in"), None)
        self.assertNotEqual(form.find_elements_by_id("id_sign-up"), None)

        # 所以他没有对应的账号登陆, 山姆点击了注册按钮
        form.find_element_by_id("id_sign-up").click()

        # 山姆进去之后看到了信息填写页面，山姆将信息依次填写并提交
        self.assertEqual(self.browser.current_url, self.live_server_url+"/auth/signup")
        form = self.browser.find_element_by_tag_name("form")
        form.find_element_by_id("id_username").send_keys("georgecai904")
        form.find_element_by_id("id_password").send_keys("testpassword")
        # form.find_element_by_id("id_password_repeat").send_keys("testpassword")
        form.find_element_by_id("id_email").send_keys("mail@georgecai.com")
        form.find_element_by_id("id_submit").click()

        # 山姆注册好了之后，页面跳转到了登陆界面
        self.assertRegex(self.browser.current_url, '/auth/login')
        form = self.browser.find_element_by_tag_name("form")
        form.find_element_by_id("id_username").send_keys("georgecai904")
        form.find_element_by_id("id_password").send_keys("testpassword")
        # self._stop()
        form.find_element_by_id("id_sign-in").click()

        # 这是山姆第一次登陆到这个网站，登陆后，页面跳转到了创建页面
        self.assertRegex(self.browser.current_url, "/clients/select")

        # 创建页面显示了两个选择，"创建采购商信息"和"创建供应商信息"
        self.assertEqual(self.browser.find_element_by_css_selector(".client-purchaser").text, "创建采购商信息")
        self.assertEqual(self.browser.find_element_by_css_selector(".client-supplier").text, "创建供应商信息")

        # 由于山姆是一个采购商，于是他点击了采购商按钮，页面跳转到创建采购商细节
        self.browser.find_element_by_css_selector(".client-purchaser").click()
        self.assertRegex(self.browser.current_url, '/purchasers/new')
        self.assertIn("active", self.browser.find_element_by_css_selector("nav .join-in").get_attribute("class"))

        # 进去之后，山姆发现页面呈现出一个表格，需要填写相关的信息
        forms = self.browser.find_elements_by_tag_name('form')
        self.assertEqual(len(forms), 1)

        # 山姆按照需要的信息填写进去并提交
        form = forms[0]
        # form.find_element_by_id("id_user").send_keys("georgecai904")
        form.find_element_by_id('id_name').send_keys("Sam")
        form.find_element_by_id('id_phone').send_keys("13868892809")
        form.find_element_by_id('id_address').send_keys("上海市浦东新区罗山路1502号10号楼502室")
        form.find_element_by_id('id_location').send_keys("江浙沪")
        form.find_element_by_id('id_license').send_keys("G92719234")
        form.find_element_by_id('id_area').send_keys('IT行业')
        form.find_element_by_id('id_submit').click()

        # 提交之后，网站回到首页，并在首页上方显示入驻成功
        self.assertEqual(self.browser.current_url, self.live_server_url+"/")

        # TODO
        # messages = self.browser.find_elements_by_css_selector('.alert-success.message')
        # self.assertIn("入驻成功", [message.text for message in messages])