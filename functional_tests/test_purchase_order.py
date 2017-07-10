from unittest import skip

from functional_tests.base import FunctionalTest


class PurchaseOrderTest(FunctionalTest):

    def test_create_purchase_order(self):

        # 山姆需要采购5000个USB 32GB
        # 山姆登陆到网站
        purchaser1 = self._create_purchaser(username="purchaser1", name="山姆采购商")
        self._login(username="purchaser1")
        self.browser.get(self.live_server_url)

        # 山姆点击发布订单
        self.browser.find_element_by_css_selector("nav .release-order").click()

        # 山姆之前已经登记了这款USB的产品信息，所以山姆只需要点击这款产品右边的发布订单按钮就可以了 （TODO：可以改变成多选形式）
        USB_32GB = self._create_product(purchaser=purchaser1, name="USB 32GB")
        USB_64GB = self._create_product(purchaser=purchaser1, name="USB 64GB")
        self.browser.refresh()
        self.assertRegex(self.browser.current_url, "/stocks/products/dashboard")

        # 点击发布订单后，页面跳转到了表单页面
        table = self.browser.find_element_by_css_selector(".product-table")
        release_order = table.find_element_by_css_selector("tbody tr:nth-child(2) .release-order")
        self.assertEqual(release_order.text, "发布订单")
        release_order.click()
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/new")

        # 页面的左边是商品的信息
        self.assertEqual(self.browser.find_element_by_css_selector(".product-container .product-name dd").text, "USB 64GB")

        # 页面的右边需要山姆填写需要采购的数量（TODO：可以添加是否支持拼购）
        form = self.browser.find_element_by_css_selector("form")
        form.find_element_by_id("id_amount").send_keys(5000)

        # 山姆填写好对的数量后，点击发布按钮
        form.find_element_by_id("id_submit").click()

        # 页面跳转到确认页面，上面提示山姆商品信息是否正确
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/new/confirm")

        # 山姆查看了一下信息，发现他选错了USB的型号
        self.assertFalse(self.browser.find_element_by_css_selector(".product-container .product-name dd").text == "USB 32GB")

        # 于是他点击返回商品库
        self.browser.find_element_by_css_selector(".back").click()

        # 山姆重新选择了正确型号的USB，点击发布按钮
        self.assertRegex(self.browser.current_url, "/stocks/products/dashboard")
        self.browser.find_element_by_css_selector(".product-table tbody tr:nth-child(1) .release-order").click()

        # 页面再次跳转到了订单发布页面，山姆对应填写好了数量
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/new")
        form = self.browser.find_element_by_css_selector("form")
        form.find_element_by_id("id_amount").send_keys(5000)
        form.find_element_by_id("id_submit").click()

        # 页面再次来到确认页面，山姆这次确认信息都正确，山姆点击确认发布
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/new/confirm")
        self.assertEqual(self.browser.find_element_by_css_selector(".product-container .product-name dd").text, "USB 32GB")
        self.assertEqual(self.browser.find_element_by_css_selector(".order-amount").text, '5000')
        self.browser.find_element_by_id("id_submit").click()

        # 发布后，页面跳转到了用户中心的我的发布页面，山姆看到了刚刚发布的采购订单出现在了“待确认”这栏
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/dashboard")
        on_check_table = self.browser.find_element_by_css_selector(".on-check table")
        first_row = on_check_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(first_row.find_element_by_css_selector(".product-name").text, "USB 32GB")

        # 山姆查看了这个订单的数量与自己发布的一致
        self.assertEqual(first_row.find_element_by_css_selector(".product-amount").text, "5000")
        self.assertEqual(first_row.find_element_by_css_selector(".offer-amount").text, "0/3")

        # 山姆回到网站的首页，看到首页也显示了自己刚刚发布的订单, 并且确认所有显示的信息完全正确
        self.browser.find_element_by_css_selector("nav .homepage").click()
        container = self.browser.find_element_by_css_selector(".product-list .product-container:first-child")
        self.assertEqual(container.find_element_by_css_selector(".purchaser-name .value").text, "山姆采购商")
        self.assertEqual(container.find_element_by_css_selector(".product-name .value").text, "USB 32GB")

        # 山姆确认无误，并关闭了网站
        self.browser.quit()


    def test_join_purchase_order(self):
        pass