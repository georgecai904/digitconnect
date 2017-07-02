from django.contrib.auth.models import User

from functional_tests.base import FunctionalTest
from unittest import skip
import time

from clients.models import Purchaser


class ProductFunctionalTest(FunctionalTest):

    def test_post_new_product(self):
        # 山姆登陆到了首页，看到了"产品发布"，便点了进去
        self.browser.get(self.live_server_url)
        post_product_link = self.browser.find_element_by_css_selector("nav .post-product")
        self.assertIn("产品发布", post_product_link.text)
        post_product_link.click()

        # 山姆因为还没有登陆过，所以网页跳转到了登陆页面
        # 山姆将自己的登陆信息进去
        self._create_purchaser()

        self.assertRegex(self.browser.current_url, "/auth/login")
        form = self.browser.find_element_by_tag_name('form')
        form.find_element_by_id("id_username").send_keys("purchaser1")
        form.find_element_by_id("id_password").send_keys("testpassword")
        form.find_element_by_id("id_sign-in").click()

        # 山姆将之前的账号输入进去，页面跳转到了空列表中，右边有一个"发布"按钮
        self.assertRegex(self.browser.current_url, "/products/list")
        # table = self.browser.find_element_by_id("product-table")
        # self.assertEqual(table.find_elements_by_css_selector('tbody tr'), [])
        self.browser.find_element_by_css_selector("a.post").click()

        # 点击发布后，页面跳转到了商品发布界面
        self.assertEqual(self.browser.current_url, self.live_server_url + "/products/new")
        form = self.browser.find_element_by_tag_name('form')

        # 山姆将他想要发布的商品以此都填写进去
        form.find_element_by_id('id_name').send_keys('B&O音响')
        form.find_element_by_id('id_image').send_keys('/images/product.jpg')
        form.find_element_by_id('id_category').send_keys('高档音响')
        form.find_element_by_id('id_location').send_keys('江浙沪')

        # 山姆填写并成功提交了
        form.find_element_by_id('id_submit').click()

        # 提交后，网页跳到了一个产品页面，在这个页面里显示了刚刚发布的商品
        self.assertRegex(self.browser.current_url, "/products/list")
        table = self.browser.find_element_by_id("product-table")
        self.assertEqual(table.find_element_by_css_selector('tbody tr:first-child .product-name').text, "B&O音响")

        # 在表格的最右边，山姆看到了修改按钮便点进去
        table.find_element_by_css_selector('tr:first-child .edit').click()

        # 页面跳转到了修改页面, 里面显示了该商品的所有信息
        self.assertRegex(self.browser.current_url, self.live_server_url + "/products/edit")
        form = self.browser.find_element_by_tag_name('form')

        self.assertEqual(form.find_element_by_id('id_name').get_attribute('value'), 'B&O音响')
        self.assertEqual(form.find_element_by_id('id_image').get_attribute('value'), '/images/product.jpg')
        self.assertEqual(form.find_element_by_id('id_category').get_attribute('value'), '高档音响')
        self.assertEqual(form.find_element_by_id('id_location').get_attribute('value'), '江浙沪')

        # 山姆发现商品的名称有些问题，于是更改了商品名称并保存
        form.find_element_by_id('id_name').clear()
        form.find_element_by_id('id_name').send_keys('B&O 降噪系列音响')
        form.find_element_by_id('id_submit').click()

        # 提交后，页面回到了原来的商品列表内，并发现商品名称已经更改成功
        self.assertRegex(self.browser.current_url, self.live_server_url + "/products/list")
        table = self.browser.find_element_by_id("product-table")
        self.assertEqual(table.find_element_by_css_selector('tbody tr:first-child .product-name').text, "B&O 降噪系列音响")

        # 山姆点击回到首页的商品列表里面看到了他刚刚发布的产品
        self.browser.find_element_by_css_selector("nav .homepage").click()
        self.assertEqual(self.browser.current_url, self.live_server_url + "/")
        container = self.browser.find_element_by_css_selector(".product-container:first-child")
        self.assertEqual(container.find_element_by_css_selector(".product-name .value").text, 'B&O 降噪系列音响')

        # 山姆觉得这个商品已经过时，想删掉，于是他点回到产品发布
        self.browser.find_element_by_css_selector("nav .post-product").click()
        table = self.browser.find_element_by_id("product-table")
        table.find_element_by_css_selector('tbody tr:first-child .delete').click()

        # 点击后，商品便自动消失了
        self.assertEqual(self.browser.find_elements_by_id("product-table"), [])

        # 再回到首页时，山姆发现产品列表中该产品不存在了
        self.browser.find_element_by_css_selector("nav .homepage").click()
        self.assertRegex(self.browser.current_url, "/")
        # container = self.browser.find_element_by_css_selector(".product-container:first-child")
        self.assertEqual(self.browser.find_elements_by_css_selector(".product-container"), [])
