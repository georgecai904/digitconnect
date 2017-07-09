from functional_tests.base import FunctionalTest

class OffersDashBoardTest(FunctionalTest):

    def test_offers_dashboard(self):
        # python manage.py test functional_tests.test_user_center.UserCenterTest.test_offers_dashboard
        # 前提条件设立
        sam = self._create_purchaser(username="purchaser1", name="山姆采购商")
        usb_32 = self._create_product(purchaser=sam, name="USB 32GB")
        usb_32_order = self._create_purchase_order(initiator=sam, product=usb_32, amount=100000)

        george = self._create_purchaser(username="purchaser2", name="乔治采购商")
        usb_64 = self._create_product(purchaser=george, name="USB 64GB")
        usb_64_order = self._create_purchase_order(initiator=george, product=usb_64, amount=100000)

        wason = self._create_supplier(username="supplier1", name="华少供应")
        usb_32_order.add_supplier(supplier=wason, price=16.99)
        usb_32_order.make_deal(supplier=wason)
        usb_64_order.add_supplier(supplier=wason, price=19.99)

        # 干扰因素
        other_supplier = self._create_supplier(username="supplier2", name="其他供应")
        usb_32_order.add_supplier(supplier=other_supplier, price=17.99)
        usb_64_order.add_supplier(supplier=other_supplier, price=21.99)

        # 华少登陆网页
        # 华少昨天分别给山姆的USB 32GB和乔治的USB 64GB报过价格，华少想看这两个报价的进度
        self.browser.get(self.live_server_url)
        self._login(username="supplier1")

        # 华少点击我的中心
        self.browser.find_element_by_css_selector("nav .user-center").click()

        # 页面跳转到了我的中心，华少继续点击我的报价
        self.browser.find_element_by_css_selector(".offers-dashboard").click()

        # 页面跳转到了我的报价页面
        self.assertRegex(self.browser.current_url, "/deals/supply_offers/dashboard")

        # 里面有两栏：被采纳的报价和正在报价中
        self.assertEqual(self.browser.find_element_by_css_selector(".adopted-offers h3").text, "被采纳报价")
        self.assertEqual(self.browser.find_element_by_css_selector(".ongoing-offers h3").text, "正在报价中")

        # 其中给山姆的报价在被采纳的报价这栏里
        adopted_offers = self.browser.find_element_by_css_selector(".adopted-offers table")
        row = adopted_offers.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".order-initiator").text, "山姆采购商")
        self.assertEqual(row.find_element_by_css_selector(".product-name").text, "USB 32GB")
        self.assertEqual(row.find_element_by_css_selector(".order-amount").text, "100000")
        self.assertEqual(row.find_element_by_css_selector(".offer-price").text, "16.99")

        # 给乔治的报价仍然在正在报价中这栏，正在报价这栏显示了华少的报价，他报价时的数量，最新采购数量
        ongoing_offers = self.browser.find_element_by_css_selector(".ongoing-offers table")
        row = ongoing_offers.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".order-initiator").text, "乔治采购商")
        self.assertEqual(row.find_element_by_css_selector(".product-name").text, "USB 64GB")
        self.assertEqual(row.find_element_by_css_selector(".order-amount").text, "100000")
        self.assertEqual(row.find_element_by_css_selector(".offer-amount").text, "100000")
        self.assertEqual(row.find_element_by_css_selector(".offer-price").text, "19.99")

        # 华少点击了给乔治的报价，页面进入到了报价详情页面
        row.find_element_by_css_selector(".order-initiator a").click()
        self.assertRegex(self.browser.current_url, "/deals/supply_offers/details")

        # 左边页面显示采购商品的信息
        self.assertEqual(self.browser.find_element_by_css_selector(".product-container .product-name dd").text,
                         "USB 64GB")

        # 中间是采购商的具体信息以及他们的采购数量和总数
        purchase_order_container = self.browser.find_element_by_css_selector(".purchase-order-container")
        row = purchase_order_container.find_element_by_css_selector("table tbody tr:first-child")
        self.assertEqual(
            row.find_element_by_css_selector(".purchaser-name").text, "乔治采购商")
        self.assertEqual(row.find_element_by_css_selector(".order-amount").text, "100000")
        self.assertEqual(purchase_order_container.find_element_by_css_selector("table tfoot tr .total-amount").text,
                         "100000")

        # 右边页面是个表单，里面显示了华少之前的报价，华少可以更改价格，华少想尝试一下功能
        form = self.browser.find_element_by_css_selector(".supply-offer-container form")
        price_field = form.find_element_by_id("id_price")
        self.assertEqual(price_field.get_attribute("value"), "19.99")
        price_field.clear()
        price_field.send_keys("18.99")
        form.find_element_by_id("id_submit").click()

        # 页面跳转到了确认页面，华少点击了取消，页面回到了刚刚的报价详情页面
        self.assertRegex(self.browser.current_url, "/deals/supply_offers/edit/confirm")
        self.browser.find_element_by_css_selector(".back").click()
        self.assertRegex(self.browser.current_url, "deals/supply_offers/details")

        # 与此同时，大卫和法兰基拼购了乔治的采购订单，他们分别需要10万个和5万个产品，所以数量已经上升到了25万个
        purchaser3 = self._create_purchaser(username="purchaser3", name="大卫采购商")
        purchaser4 = self._create_purchaser(username="purchaser4", name="法兰基采购商")
        usb_64_order.add_purchaser(purchaser=purchaser3, amount=100000)
        usb_64_order.add_purchaser(purchaser=purchaser4, amount=50000)

        # 华少都到了通知, 回到了刚刚的我的报价页面(TODO： 增加在线功能或提醒）
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_css_selector("nav .user-center").click()
        self.browser.find_element_by_css_selector(".offers-dashboard").click()

        # 华少观察到乔治发起的采购单数量又原先的10万变为25万个，自己的报价数量还是的10万个
        ongoing_offers = self.browser.find_element_by_css_selector(".ongoing-offers table")
        row = ongoing_offers.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".order-amount").text, "250000")
        self.assertEqual(row.find_element_by_css_selector(".offer-amount").text, "100000")

        # 华少点进去查看详情，看到一共有三个采购商，以及他们所需要的数量
        row.find_element_by_css_selector(".order-initiator a").click()
        self.assertRegex(self.browser.current_url, "/deals/supply_offers/details")
        purchase_order_table = self.browser.find_element_by_css_selector(".purchase-order-container table")
        self.assertEqual(len(purchase_order_table.find_elements_by_css_selector("tbody tr")), 3)
        self.assertEqual(purchase_order_table.find_element_by_css_selector("tfoot tr .total-amount").text,
                         "250000")

        # 华少为了拿到这个订单，决定将价格由原先的19.99改为15.99，并提交
        form = self.browser.find_element_by_css_selector(".supply-offer-container form")
        price_field = form.find_element_by_id("id_price")
        self.assertEqual(price_field.get_attribute("value"), "19.99")
        price_field.clear()
        price_field.send_keys("15.99")
        form.find_element_by_id("id_submit").click()

        # 页面再次跳转到确认页面，华少确认了价格，并提交
        self.assertRegex(self.browser.current_url, "/deals/supply_offers/edit/confirm")
        self.browser.find_element_by_id("id_submit").click()

        # 页面跳回了刚刚的我的报价页面，华少给乔治的价格也更新了过来
        self.assertRegex(self.browser.current_url, "/deals/supply_offers/dashboard")

        ongoing_offers = self.browser.find_element_by_css_selector(".ongoing-offers table")
        row = ongoing_offers.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".order-initiator").text, "乔治采购商")
        self.assertEqual(row.find_element_by_css_selector(".product-name").text, "USB 64GB")
        self.assertEqual(row.find_element_by_css_selector(".order-amount").text, "250000")
        self.assertEqual(row.find_element_by_css_selector(".offer-amount").text, "250000")
        self.assertEqual(row.find_element_by_css_selector(".offer-price").text, "15.99")

        # 与此同时，乔治收到了华少的价格更新的提示并确认了华少的报价
        usb_64_order.make_deal(supplier=wason)

        # 华少刷新了页面，刚刚乔治的订单从正在报价中转移到了被采纳的报价中
        self.browser.refresh()
        ongoing_offers = self.browser.find_element_by_css_selector(".ongoing-offers table")
        self.assertEqual(len(ongoing_offers.find_elements_by_css_selector("tbody tr")), 0)
        adopted_offers = self.browser.find_element_by_css_selector(".adopted-offers table")
        self.assertEqual(len(adopted_offers.find_elements_by_css_selector("tbody tr")), 2)

        # 华少点进乔治的订单，页面跳转到了确认订单页面
        adopted_offers = self.browser.find_element_by_css_selector(".adopted-offers table")
        row = adopted_offers.find_element_by_css_selector("tbody tr:nth-child(1)")
        row.find_element_by_css_selector(".order-initiator a").click()

        self.assertRegex(self.browser.current_url, "/deals/supply_offers/adopt")

        # 华少点击确认订单，页面跳转到了工厂账号创建页面
        self.browser.find_element_by_id("id_submit").click()
        self.assertRegex(self.browser.current_url, "/clients/manufacturers/new")
