from functional_tests.base import FunctionalTest
from unittest import skip
import time


class UserDetailsTest(FunctionalTest):

    def setUp(self):
        purchaser = self._create_purchaser()
        self._create_product(purchaser)

    def test_user_update_information(self):
        # 山姆打开了网页，点击登陆按钮进入登陆界面
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_css_selector("nav .login").click()

        self.assertRegex(self.browser.current_url, '/auth/login')
        self.browser.find_element_by_css_selector("form #id_username").send_keys("purchaser1")
        self.browser.find_element_by_css_selector("form #id_password").send_keys("testpassword")
        self.browser.find_element_by_css_selector("form #id_sign-in").click()

        # 山姆登陆网站后想更新一下自己的邮箱信息，便点击了右上角的用户信息
        self.assertRegex(self.browser.current_url, '/')

        self.browser.find_element_by_css_selector("nav .user-details").click()

        # 页面跳转到了用户信息界面，山姆在邮箱的邮编看到了修改按钮
        self.assertRegex(self.browser.current_url, "/auth/details")
        email_container = self.browser.find_element_by_css_selector(".user-details .email")
        self.assertEqual(email_container.find_element_by_css_selector(".value").text, "purchaser1@dc.com")
        email_container.find_element_by_css_selector(".edit").click()

        # 于是山姆点了进去，便进行修改，山姆便把自己新的邮箱放了上去，并保存
        self.assertRegex(self.browser.current_url, "/auth/details/email")
        email_input = self.browser.find_element_by_css_selector("form #id_email")
        self.assertEqual(email_input.get_attribute("value"), "purchaser1@dc.com")
        email_input.clear()
        email_input.send_keys("purchaser2@dc.com")
        self.browser.find_element_by_css_selector("form #id_submit").click()

        # 页面跳回到了用户信息界面，山姆看见自己的邮箱已经更新成功
        self.assertRegex(self.browser.current_url, "/auth/details")

        self.assertEqual(
            self.browser.find_element_by_css_selector(".user-details .email .value").text,
            "purchaser2@dc.com"
        )

        # 山姆看到密码栏只显示了一个更改按钮, 于是点了进去进行修改，修改完成后
        self.browser.find_element_by_css_selector(".user-details .password .edit").click()
        self.assertRegex(self.browser.current_url, "/auth/details/password")
        self.browser.find_element_by_css_selector("form #id_old_password").send_keys("testpassword")
        self.browser.find_element_by_css_selector("form #id_password").send_keys("newpassword")
        self.browser.find_element_by_css_selector("form #id_repeated_password").send_keys("newpassword")
        self.browser.find_element_by_css_selector("form #id_submit").click()

        # 网站自动登出了, 山姆想尝试一下密码是否已经更改成功，于是便登出再登陆
        self.assertRegex(self.browser.current_url, "/auth/login")
        self.browser.find_element_by_css_selector("nav .login").click()

        # 山姆发现密码已经成功修改，原先的密码不能登陆
        self.assertRegex(self.browser.current_url, "/auth/login")
        self.browser.find_element_by_css_selector("form #id_username").send_keys("purchaser1")
        self.browser.find_element_by_css_selector("form #id_password").send_keys("newpassword")
        self.browser.find_element_by_css_selector("form #id_sign-in").click()

        # 山姆很开心，于是又回到了用户信息界面
        self.assertRegex(self.browser.current_url, "/")
        self.browser.find_element_by_css_selector("nav .user-details").click()

        # 山姆发现在用户信息界面的下方有一个表格显示采购商信息表格
        purchaser_container = self.browser.find_element_by_css_selector(".purchasers")
        self.assertEqual(purchaser_container.find_element_by_tag_name("h1").text, "采购商信息表")
        # time.sleep(10)
        # 这个表格显示了在自己名下的所有采购商信息
        self.assertEqual(
            purchaser_container.find_element_by_css_selector("tbody tr:first-child .purchaser-name").text,
            "山姆采购商")

        # 在每个表格的右边有产品按钮，修改按钮和删除按钮
        self.assertEqual(purchaser_container.find_element_by_css_selector("tbody tr:first-child .products").text,
                         "产品")
        self.assertEqual(purchaser_container.find_element_by_css_selector("tbody tr:first-child .edit").text,
                         "修改")
        # self.assertEqual(purchaser_container.find_element_by_css_selector("tbody tr:first-child .delete").text,
        #                  "删除")

        # 山姆发现他的采购商信息种类错了，便点击修改按钮
        purchaser_container.find_element_by_css_selector("tbody tr:first-child .edit").click()

        # 页面跳转到了采购商信息修改页面，山姆将自己的信息更新并保存
        self.assertRegex(self.browser.current_url, "/purchasers/edit")

        purchaser_name_input = self.browser.find_element_by_css_selector("form #id_name")
        self.assertEqual(purchaser_name_input.get_attribute("value"), "山姆采购商")
        purchaser_name_input.clear()
        purchaser_name_input.send_keys("新山姆采购商")
        self.browser.find_element_by_css_selector("form #id_submit").click()

        # 保存后页面跳回到了用户信息界面，确认刚刚更新成功
        self.assertRegex(self.browser.current_url, "/auth/details")
        purchaser_container = self.browser.find_element_by_css_selector(".purchasers")
        self.assertEqual(
            purchaser_container.find_element_by_css_selector("tbody tr:first-child .purchaser-name").text,
            "新山姆采购商")

        # 山姆想查看一下采购商里的产品信息情况，便点击了产品按钮
        purchaser_container.find_element_by_css_selector("tbody tr:first-child .products").click()

        # 页面跳转到了之前的产品列表，里面信息和之前的一致
        self.assertRegex(self.browser.current_url, "/products/list")
        self.assertEqual(
            self.browser.find_element_by_css_selector("tbody .product-name").text,
            "B&O音响"
        )

        # 山姆看一些信息都稳妥了，便退出了
        self.browser.find_element_by_css_selector("nav .logout").click()
        self.browser.get(self.live_server_url+"/auth/details")
        self.assertRegex(self.browser.current_url, "/auth/login")