from functional_tests.base import FunctionalTest


class SupplierFunctionalTest(FunctionalTest):

    def test_supplier_post_price(self):
        p = self._create_product()

        # 华少是一个高端音响制造公司的销售员，他从朋友那里了解到了该网站
        # 华少打开了这个网站
        self.browser.get(self.live_server_url)

        # 华少在网页上看到了山姆发布的采购需求
        product_container = self.browser.find_element_by_css_selector(".product-container:first-child")
        self.assertEqual(product_container.find_element_by_css_selector(".purchaser-name .value").text, "山姆采购商")

        # 华少对山姆的采购需求很感兴趣，便点击报价
        product_container.find_element_by_css_selector(".post-price").click()

        # 页面跳转到了一个表单页面，里面需要填写一些个人信息，华少依次填写下自己的联系方式，报价
        self.assertRegex(self.browser.current_url, "/products/[0-9]+/post-price")

        self.assertEqual(
            self.browser.find_element_by_css_selector(".product-container .product-name .value").text, "B&O音响")
        form = self.browser.find_element_by_css_selector(".post-price form")
        # self._stop(20)
        form.find_element_by_id("id_name").send_keys("华少")
        form.find_element_by_id("id_phone").send_keys("12839991231")
        form.find_element_by_id("id_email").send_keys("junk@georgecai.com")
        form.find_element_by_id("id_price").send_keys("1000")
        form.find_element_by_id("id_submit").click()

        # 华少提交后，页面显示了他刚刚填写的信息以及山姆的采购需求
        # 页面提示华少，他的报价已经提交，并提示华少，若采购商感兴趣，会进一步与您联系
        # self.assertRegex(self.browser.current_url, "/products/post-price/success")
        self.assertEqual(
            self.browser.find_element_by_css_selector(".product-container .product-name .value").text, "B&O音响")
        self.assertEqual(
            self.browser.find_element_by_css_selector(".post-price-container .post-price .value").text, "1000"
        )
        self.assertEqual(
            self.browser.find_element_by_css_selector(".alert.alert-success").text, "您的报价已提交，若采购商感兴趣，会进一步与您联系"
        )

        # 华少点击返回主页，页面跳回到了首页
        self.browser.find_element_by_css_selector(".back").click()
        self.assertRegex(self.browser.current_url, "/")

