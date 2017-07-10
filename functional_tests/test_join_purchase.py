from functional_tests.base import FunctionalTest

class JoinPurchaseTest(FunctionalTest):

    def test_join_purchase(self):

        # 黛安娜登陆到了网页
        diana = self._create_purchaser(username="diana", name="黛安娜采购商")
        self.browser.get(self.live_server_url)

        # 黛安娜看到山姆的USB 10万个的采购需求
        sam = self._create_purchaser(username="sam", name="山姆采购商")
        usb_32 = self._create_product(purchaser=sam, name="USB 32GB")
        purchase_order = self._create_purchase_order(initiator=sam, product=usb_32, amount=100000)

        # 并且这个订单已经有两个供应商报价了
        supplier1 = self._create_supplier(username="s1", name="s1")
        supplier2 = self._create_supplier(username="s2", name="s2")
        purchase_order.add_supplier(supplier=supplier1, price=19.99)
        purchase_order.add_supplier(supplier=supplier2, price=18.99)

        self.browser.refresh()

        product_container = self.browser.find_element_by_css_selector(".product-container:first-child")
        self.assertEqual(product_container.find_element_by_css_selector(".purchaser-name .value").text, "山姆采购商")
        self.assertEqual(product_container.find_element_by_css_selector(".product-name .value").text, "USB 32GB")

        # 黛安娜也刚好需要采购这款产品, 黛安娜点击了产品下方的参加拼购
        product_container.find_element_by_css_selector(".join-purchase").click()

        # 点击之后，因为黛安娜还没有登陆，所以页面跳转到了登陆页面
        self.assertRegex(self.browser.current_url, "/auth/login")

        # 黛安娜登陆后，页面跳转到了拼购页面
        self._login(username="diana", login_url=self.browser.current_url)
        self.assertRegex(self.browser.current_url, "/deals/join_purchases/new")

        # 页面的左边显示了商品的信息
        product_container = self.browser.find_element_by_css_selector(".product-container")
        self.assertEqual(product_container.find_element_by_css_selector(".product-name dd").text, "USB 32GB")

        # 页面中间是拼购详情
        join_purchase = self.browser.find_element_by_css_selector(".join-purchase-container table")
        row = join_purchase.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".purchaser-name").text, "山姆采购商")
        self.assertEqual(row.find_element_by_css_selector(".purchase-amount").text, "100000")

        # 页面的右边是一个表单，需要黛安娜输入她需要采购的数量
        form = self.browser.find_element_by_css_selector("form")

        # 黛安娜输入了20万，并点击“拼购”
        form.find_element_by_id("id_amount").send_keys("200000")
        # self._stop()
        form.find_element_by_id("id_submit").click()

        # 页面跳转到了确认拼购页面，黛安娜确认了商品信息以及采购数量是否正确
        self.assertRegex(self.browser.current_url, "/deals/join_purchases/confirm")
        self.assertEqual(self.browser.find_element_by_css_selector(".join-purchase-container .amount").text, "200000")

        # 黛安娜点击确定按钮
        self.browser.find_element_by_id("id_submit").click()

        # 页面跳转到了我的发布页面
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/dashboard")

        # 刚刚参加的采购单出现在了待确认页面，数量为她刚刚输入的20万个
        on_check_table = self.browser.find_element_by_css_selector(".on-check table")
        row = on_check_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".product-name").text, "USB 32GB")
        self.assertEqual(row.find_element_by_css_selector(".product-amount").text, "200000")
        self.assertEqual(row.find_element_by_css_selector(".offer-amount").text, "2/3")

        # 黛安娜想看看这个参加过拼购的商品是否会出现在自己商品库中，于是点击了我的中心
        self.browser.find_element_by_css_selector("nav .user-center").click()

        # 页面跳转到我的中心后，黛安娜点击了我的产品
        self.assertRegex(self.browser.current_url, "/auth/center")
        self.browser.find_element_by_css_selector(".products-dashboard").click()

        # 页面跳转到了产品库
        self.assertRegex(self.browser.current_url, "/stocks/products/dashboard")

        # 黛安娜发现刚刚参加过拼购的商品的确在自己的产品库中了
        product_table = self.browser.find_element_by_css_selector(".product-table")
        row = product_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".product-name").text, "USB 32GB")

        # 黛安娜确认信息后退出了网站
        self._logout()

        # 与此同时山姆登陆到了网页，点击了我的中心
        self.browser.get(self.live_server_url)
        self._login(username="sam")
        self.browser.find_element_by_css_selector("nav .user-center").click()

        # 然后山姆点击了我的发布
        self.browser.find_element_by_css_selector(".orders-dashboard").click()

        # 山姆看见他的采购单里面的总采购数由原先的10万变为30万个
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/dashboard")
        on_check_table = self.browser.find_element_by_css_selector(".on-check table")
        row = on_check_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".product-name").text, "USB 32GB")
        self.assertEqual(row.find_element_by_css_selector(".product-amount").text, "100000")
        self.assertEqual(row.find_element_by_css_selector(".offer-amount").text, "2/3")

        # 山姆点击了这个订单
        row.find_element_by_css_selector(".product-name a").click()
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/details")

        # 山姆看见所有的工厂都还没有更新价格，并出现通知工厂的按钮
        supply_offer_table = self.browser.find_element_by_css_selector(".supply-offer table")
        row1 = supply_offer_table.find_element_by_css_selector("tbody tr:nth-child(1)")
        self.assertEqual(row1.find_element_by_css_selector(".supplier-name").text, "s1")
        self.assertEqual(row1.find_element_by_css_selector(".offer-price").text, "19.99")
        self.assertEqual(row1.find_element_by_css_selector(".offer-amount").text, "100000")

        row2 = supply_offer_table.find_element_by_css_selector("tbody tr:nth-child(2)")
        self.assertEqual(row2.find_element_by_css_selector(".supplier-name").text, "s2")
        self.assertEqual(row2.find_element_by_css_selector(".offer-price").text, "18.99")
        self.assertEqual(row2.find_element_by_css_selector(".offer-amount").text, "100000")

        row1.find_element_by_css_selector(".notice").click()

        self.assertRegex(self.browser.current_url, "deals/purchase_orders/manage")
        supply_offer_table = self.browser.find_element_by_css_selector(".supply-offer table")
        row1 = supply_offer_table.find_element_by_css_selector("tbody tr:nth-child(1)")
        self.assertEqual(row1.find_element_by_css_selector(".notice").text, "已通知")

        # 并且在拼购那个表格里面看到了黛安娜的拼购信息
        join_purchase_table = self.browser.find_element_by_css_selector(".join-purchase table")
        row = join_purchase_table.find_element_by_css_selector("tbody tr:nth-child(1)")
        self.assertEqual(row.find_element_by_css_selector(".purchaser-name").text, "黛安娜采购商")
        self.assertEqual(row.find_element_by_css_selector(".purchase-amount").text, "200000")

        # 山姆确认一切正常，便退出了网站
        self.browser.quit()