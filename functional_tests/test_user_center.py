from functional_tests.base import FunctionalTest
from unittest import skip

class UserCenterTest(FunctionalTest):

    def test_user_center_for_supplier(self):
        self.browser.get(self.live_server_url)

        # 山姆发布了USB的10万个采购需求，采购需求的状态为待确认
        sam = self._create_purchaser(username="sam", name="sam")
        usb_product = self._create_product(purchaser=sam, name="USB")
        purchase_order = self._create_purchase_order(initiator=sam, product=usb_product)
        purchase_order.add_purchaser(purchaser=sam, amount=100000)

        self.assertEqual(purchase_order.status, "待确认")

        # 山姆今天登陆了网站，网站的右上角有一个我的中心，他点击进入
        # self._stop()
        self._login(username="sam")
        user_center = self.browser.find_element_by_css_selector("nav .user-center")
        self.assertEqual(user_center.text, "我的中心")
        user_center.click()

        # 进入网站后，山姆看到了个人信息，我的订单，我的发布三个按钮
        self.assertRegex(self.browser.current_url, "/auth/center")
        # print(self.browser.current_url)
        # self._stop(30)
        self.assertEqual(self.browser.find_element_by_css_selector(".personal-info").text, "个人信息")
        self.assertRegex(self.browser.find_element_by_css_selector(".personal-info").get_attribute("href"),
                         "/auth/account")

        self.assertEqual(self.browser.find_element_by_css_selector(".my-orders").text, "我的订单")
        self.assertRegex(self.browser.find_element_by_css_selector(".my-orders").get_attribute("href"),
                         "/auth/my-orders")

        self.assertEqual(self.browser.find_element_by_css_selector(".orders-dashboard").text, "我的发布")
        self.assertRegex(self.browser.find_element_by_css_selector(".orders-dashboard").get_attribute("href"),
                         "/deals/purchase_orders/dashboard")

        # 山姆点击了我的发布`
        self.browser.find_element_by_css_selector(".orders-dashboard").click()

        # 网页转到了一个三栏的页面，分别是已完成，待收货，待确认
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/dashboard")
        self.assertEqual(self.browser.find_element_by_css_selector(".completed .title").text, "已完成")
        self.assertEqual(self.browser.find_element_by_css_selector(".on-road .title").text, "待收货")
        self.assertEqual(self.browser.find_element_by_css_selector(".on-check .title").text, "待确认")

        # 在待确认里面，山姆看到了之前USB采购需求，且这个需求显示为0/3个报价，目前任何的报价
        on_check_table = self.browser.find_element_by_css_selector(".on-check table")
        first_row = on_check_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(first_row.find_element_by_css_selector(".product-name").text, "USB")
        self.assertEqual(first_row.find_element_by_css_selector(".product-amount").text, "100000")
        self.assertEqual(first_row.find_element_by_css_selector(".offer-amount").text, "0/3")

        # 山姆点击这个USB采购需求
        first_row.find_element_by_css_selector(".product-name a").click()

        # 页面跳转到了采购细节页面, 页面同样的显示了三栏，分别是报价／加入采购／在线交流
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/manage")
        self.assertEqual(self.browser.find_element_by_css_selector(".purchase-offer .title").text, "供应商报价")
        self.assertEqual(self.browser.find_element_by_css_selector(".join-purchase .title").text, "采购商拼购")
        self.assertEqual(self.browser.find_element_by_css_selector(".online-chat .title").text, "在线交流")


        # 在报价这栏，里面显示了三个个供应商的报价，供应商的名称，联系方式，以及他们的报价，已经他们报价时的采购数目
        supplier1 = self._create_supplier(username="supplier1", name="工厂1")
        supplier2 = self._create_supplier(username="supplier2", name="工厂2")
        supplier3 = self._create_supplier(username="supplier3", name="工厂3")
        purchase_order.add_supplier(supplier=supplier1, price=19.99)
        purchase_order.add_supplier(supplier=supplier2, price=17.95)
        purchase_order.add_supplier(supplier=supplier3, price=20.00)
        # self._stop(30)
        self.browser.refresh()
        purchase_offer_table = self.browser.find_element_by_css_selector(".purchase-offer table")
        row = purchase_offer_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".supplier-name").text, "工厂1")
        self.assertEqual(row.find_element_by_css_selector(".offer-price").text, "19.99")
        self.assertEqual(row.find_element_by_css_selector(".offer-amount").text, "100000")
        row = purchase_offer_table.find_element_by_css_selector("tbody tr:nth-child(2)")
        self.assertEqual(row.find_element_by_css_selector(".supplier-name").text, "工厂2")
        self.assertEqual(row.find_element_by_css_selector(".offer-price").text, "17.95")
        self.assertEqual(row.find_element_by_css_selector(".offer-amount").text, "100000")
        row = purchase_offer_table.find_element_by_css_selector("tbody tr:nth-child(3)")
        self.assertEqual(row.find_element_by_css_selector(".supplier-name").text, "工厂3")
        self.assertEqual(row.find_element_by_css_selector(".offer-price").text, "20.00")
        self.assertEqual(row.find_element_by_css_selector(".offer-amount").text, "100000")

        # 点击缩略地图里面的我的发布，山姆回到了我的发布界面
        self.browser.find_element_by_css_selector(".breadcrumb li:first-child a").click()
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/dashboard")

        # 山姆发现在刚刚的USB的报价数量变成了3/3
        on_check_table = self.browser.find_element_by_css_selector(".on-check table")
        first_row = on_check_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(first_row.find_element_by_css_selector(".product-name").text, "USB")
        self.assertEqual(first_row.find_element_by_css_selector(".product-amount").text, "100000")
        self.assertEqual(first_row.find_element_by_css_selector(".offer-amount").text, "3/3")

        # 就在同时，有两个采购商登陆到了服务器，拼购了这款产品
        purchaser1 = self._create_purchaser(username="purchaser1", name="采购商A")
        purchaser2 = self._create_purchaser(username="purchaser2", name="采购商B")
        purchase_order.add_purchaser(purchaser=purchaser1, amount=50000)
        purchase_order.add_purchaser(purchaser=purchaser2, amount=100000)

        # 此时山姆又点击了USB采购需求
        first_row = on_check_table.find_element_by_css_selector("tbody tr:first-child")
        first_row.find_element_by_css_selector(".product-name a").click()
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/manage")

        # 在加入采购这栏里面，他发现有两个采购商加入了采购
        join_purchase_table = self.browser.find_element_by_css_selector(".join-purchase table")
        row = join_purchase_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".purchaser-name").text, "采购商A")
        self.assertEqual(row.find_element_by_css_selector(".purchase-amount").text, "50000")
        row = join_purchase_table.find_element_by_css_selector("tbody tr:nth-child(2)")
        self.assertEqual(row.find_element_by_css_selector(".purchaser-name").text, "采购商B")
        self.assertEqual(row.find_element_by_css_selector(".purchase-amount").text, "100000")

        # USB的采购需求目前更新为25万个，其中山姆为10万个，采购商A为5万个，采购商B为10万个
        self.assertEqual(purchase_order.total_amount, 250000)
        self.assertEqual(purchase_order.get_amount_by_purchaser(purchaser=sam), 100000)
        self.assertEqual(purchase_order.get_amount_by_purchaser(purchaser=purchaser1), 50000)
        self.assertEqual(purchase_order.get_amount_by_purchaser(purchaser=purchaser2), 100000)

        # 工厂1和工厂2都已经根据目前最新的采购需求将价格已经更新，工厂3目前的报价仍然为当时10万个数量的报价
        purchase_order.supplier_update_price(supplier=supplier1, price=16.95)
        purchase_order.supplier_update_price(supplier=supplier2, price=16.99)
        self.browser.refresh()
        post_price_table = self.browser.find_element_by_css_selector(".purchase-offer table")
        row = post_price_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".supplier-name").text, "工厂1")
        self.assertEqual(row.find_element_by_css_selector(".offer-price").text, "16.95")
        self.assertEqual(row.find_element_by_css_selector(".offer-amount").text, "250000")
        row = post_price_table.find_element_by_css_selector("tbody tr:nth-child(2)")
        self.assertEqual(row.find_element_by_css_selector(".supplier-name").text, "工厂2")
        self.assertEqual(row.find_element_by_css_selector(".offer-price").text, "16.99")
        self.assertEqual(row.find_element_by_css_selector(".offer-amount").text, "250000")
        row = post_price_table.find_element_by_css_selector("tbody tr:nth-child(3)")
        self.assertEqual(row.find_element_by_css_selector(".supplier-name").text, "工厂3")
        self.assertEqual(row.find_element_by_css_selector(".offer-price").text, "20.00")
        self.assertEqual(row.find_element_by_css_selector(".offer-amount").text, "100000")

        # 山姆点击了通知工厂3按钮，按钮从"点击通知"变为"已通知"工厂3收到了通知 （TODO: 需要更改为在线交流）
        row = post_price_table.find_element_by_css_selector("tbody tr:nth-child(3)")
        notice_btn = row.find_element_by_css_selector(".notice")
        self.assertEqual(notice_btn.text, "通知工厂")
        notice_btn.click()

        self.browser.refresh()
        purchase_offer_table = self.browser.find_element_by_css_selector(".purchase-offer table")
        self.assertEqual(purchase_offer_table.find_element_by_css_selector("tbody tr:nth-child(3) .notice").text, "已通知")

        # 工厂3及时更改了价格
        purchase_order.supplier_update_price(supplier=supplier3, price=15.99)

        self.browser.refresh()
        # 由于工厂3的价格最低，山姆查看了工厂3的具体信息（TODO: 需要添加确认环节）
        purchase_offer_table = self.browser.find_element_by_css_selector(".purchase-offer table")
        purchase_offer_table.find_element_by_css_selector("tbody tr:nth-child(3) .supplier-name a").click()
        self.assertRegex(self.browser.current_url, "/clients/suppliers/details")
        self.assertEqual(self.browser.find_element_by_css_selector(".supplier-name").text, "工厂3")

        # (TODO: 需要修改为投票环节）
        # 山姆确认了工厂报价信息属实，点击返回按钮
        self.browser.find_element_by_css_selector(".back").click()
        self.browser.refresh()

        # 返回当刚刚页面后，点击确定生成订单，订单状态为采购成立 (TODO: 考虑是否需要加入机制确保所有的工厂都已更新价格后才能生成订单）
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/manage")
        self.browser.find_element_by_css_selector(".confirm-order").click()

        # 页面跳回到了刚刚的我的发布页面，刚刚的采购需求从原来的待确认进入到了待收货
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/dashboard")

        self.assertEqual(len(self.browser.find_elements_by_css_selector(".on-check tbody tr")), 0)
        self.assertEqual(len(self.browser.find_elements_by_css_selector(".on-road tbody tr")), 1)
        self.assertEqual(
            self.browser.find_element_by_css_selector(".on-road tbody tr:first-child .product-name").text, "USB")
        self.assertEqual(
            self.browser.find_element_by_css_selector(".on-road tbody tr:first-child .product-amount").text, "100000")
        self.assertEqual(
            self.browser.find_element_by_css_selector(".on-road tbody tr:first-child .offer-price").text, "15.99")

        # 山姆看到后确认一切无误并关闭了网页

























        # 山姆返回到刚才的页面，点击进入创建投票流程（TODO: 需要更改为在线交流）
        # 创建投票流程后，页面跳转到了投票页面，山姆，采购商A和采购商B三者同时收到了投票通知，采购需求状态为等待投票
        # 山姆，采购商A，采购商B都各自投好票
        # 投票流程状态为已完成，最后投票一致决定为工厂3，采购需求状态为采购成立（TODO: 需要考虑如果没有达成一致，或者势均力敌的情况）
        # 山姆回到我的发布，刚刚的采购需求从原来的待确认进入到了待收货
        # 同时采购商A和采购商B也看到对应的信息
