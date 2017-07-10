from functional_tests.base import FunctionalTest

class SupplyOfferTest(FunctionalTest):

    def test_create_supply_offer(self):
        purchaser = self._create_purchaser(username="purchaser1")
        product = self._create_product(purchaser=purchaser, name="USB 64GB")
        purchase_offer = self._create_purchase_order(initiator=purchaser, product=product, amount=1000)

        self.browser.get(self.live_server_url)

        # 华少今天登陆了网站，看到了山姆发布的USB的采购需求
        self.browser.find_element_by_css_selector(".product-container:first-child .make-offer").click()

        # 由于华少已经在网站上登记了供应商的信息，但还没有登陆，所以页面跳转到了登陆页面

        self.assertRegex(self.browser.current_url, "/auth/login")

        # 华少登陆后，页面跳回了报价页面
        supplier = self._create_supplier(username="supplier1", name="华少供应")
        self._login(username="supplier1", login_url=self.browser.current_url)
        self.assertRegex(self.browser.current_url, "/deals/supply_offers/new")

        # 页面左边是商品信息已经采购数量
        self.assertEqual(self.browser.find_element_by_css_selector(".product-container .product-name dd").text,
                         "USB 64GB")

        # 页面右边是一个表单，需要填写价格, 华少将自己的报价填写进去并提交
        form = self.browser.find_element_by_css_selector("form")
        form.find_element_by_id("id_price").send_keys("19.99")
        form.find_element_by_id("id_submit").click()

        # 页面跳转到了确认报价页面
        self.assertRegex(self.browser.current_url, "/deals/supply_offers/new/confirm")

        # 华少检查了自己的报价，并点击确认按钮
        self.assertEqual(self.browser.find_element_by_css_selector(".product-container .product-name dd").text,
                         "USB 64GB")
        self.assertEqual(self.browser.find_element_by_css_selector(".offer-price").text, '19.99')
        self.browser.find_element_by_id("id_submit").click()

        # 确认之后，页面跳转到了我的报价页面
        self.assertRegex(self.browser.current_url, "/deals/supply_offers/dashboard")

        self.browser.quit()

        # (TODO: 在我的报价页面上，华少看到了刚刚的报价商品以及自己报的价格)

        # 华少检查无误后关闭了网站，等待供应商的回复




