from functional_tests.base import FunctionalTest
from django.test.utils import override_settings
import datetime

class ProductionDashboardTest(FunctionalTest):

    # @override_settings(DEBUG=True)
    def test_production_dashboard(self):
        sam = self._create_purchaser(username="sam", name="sam")
        george = self._create_supplier(username="george", name="george")
        product = self._create_product(purchaser=sam, name="USB 32GB")
        po = self._create_purchase_order(initiator=sam, product=product, amount=1)
        po.add_supplier(supplier=george, price=1.99)
        po.make_deal(supplier=george)
        # po.confirm_by_supplier()

        # 乔治再一次登陆了网页
        self._login(username="george")

        today = str(datetime.date.today())

        # 乔治点击进入了我的中心->我的报价
        self.browser.find_element_by_css_selector("nav .user-center").click()
        self.assertRegex(self.browser.current_url, "/auth/center")
        self.browser.find_element_by_css_selector(".offers-dashboard").click()
        self.assertRegex(self.browser.current_url, "/deals/supply_offers/dashboard")

        # 乔治看到了之前给山姆的USB 32GB的报价被采纳
        adopted_offers_table = self.browser.find_element_by_css_selector(".adopted-offers table")
        row = adopted_offers_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".order-initiator").text, "sam")
        self.assertEqual(row.find_element_by_css_selector(".product-name").text, "USB 32GB")
        self.assertEqual(row.find_element_by_css_selector(".order-amount").text, "1")
        self.assertEqual(row.find_element_by_css_selector(".offer-price").text, "1.99")

        # 乔治点击进去，查看了商品信息和报价
        row.find_element_by_css_selector(".order-initiator a").click()
        self.assertRegex(self.browser.current_url, "/deals/supply_offers/adopt")

        # 乔治确认无误后点击了确认订单按钮
        self.browser.find_element_by_id("id_submit").click()

        # 由于乔治还没有登记过工厂信息，所以页面跳转到了创建工厂信息页面
        # 页面跳转到了表单页面，上面需要登记工厂的名称，地址，登录名，密码
        self.assertRegex(self.browser.current_url, "/clients/manufacturers/new")

        # 乔治依次输入了这些信息，点击创建后，页面跳转到了我的工厂页面
        form = self.browser.find_element_by_css_selector("form")
        form.find_element_by_id("id_name").send_keys("乔治的工厂")
        form.find_element_by_id("id_address").send_keys("上海浦东新区")
        form.find_element_by_id("id_username").send_keys("factory1")
        form.find_element_by_id("id_password").send_keys("testpassword")
        form.find_element_by_id("id_submit").click()

        # 注册好了之后，页面跳转到了生产管理页面
        self.assertRegex(self.browser.current_url, "/deals/production/details")

        # 页面上方显示了（TODO：订单号码），产品名称，数量，工厂名称
        self.assertEqual(self.browser.find_element_by_css_selector(".product-name").text, "USB 32GB")
        self.assertEqual(self.browser.find_element_by_css_selector(".order-amount").text, "1")
        self.assertEqual(self.browser.find_element_by_css_selector(".factory-name").text, "乔治的工厂")

        # 页面显示了生产环节进程表
        production_table = self.browser.find_element_by_css_selector(".production-records table")

        # 进程表里面包括了节点代码，节点名称，计划日期，期望日期，完成日期
        self.assertEqual(
            [header.text for header in production_table.find_elements_by_css_selector("thead th")],
            ["节点代码", "节点名称", "计划日期", "期望日期", "完成日期"]
        )

        # 表格内显示了第一条信息是：PO0001, 生产订单已确认，_, _, 2017年7月7号
        row = production_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".record-code").text, "PO0001")
        self.assertEqual(row.find_element_by_css_selector(".record-title").text, "生产订单已确认")

        self.assertEqual(row.find_element_by_css_selector(".date-intended").text, today)
        self.assertEqual(row.find_element_by_css_selector(".date-estimate").text, today)
        self.assertEqual(row.find_element_by_css_selector(".date-complete").text, today)

        # 乔治在右上角看见了工厂登陆的按钮，乔治点击
        self.browser.find_element_by_css_selector("nav .manufacturer-login").click()

        # 页面跳转到了登陆界面 ,乔治把刚刚填写的工厂登陆信息填写进去, 页面回到了首页
        self._login(username="factory1", login_url=self.browser.current_url)

        # 乔治点击了右上角的我的中心
        self.browser.find_element_by_css_selector("nav .user-center").click()

        # 我的中心里面只显示了账户信息以及生产管理
        self.assertRegex(self.browser.current_url, "/auth/center")

        self.assertEqual(
            [module.text for module in self.browser.find_elements_by_css_selector(".row a")],
            ["个人信息", "生产管理"]
        )

        # 乔治点击了生产订单列表，页面显示了一个表格，表格显示了产品名称，订单数量, 节点名称
        self.browser.find_element_by_css_selector(".production-dashboard").click()
        self.assertRegex(self.browser.current_url, "/deals/production/dashboard")

        table = self.browser.find_element_by_css_selector(".production table")
        self.assertEqual(
            [header.text for header in table.find_elements_by_css_selector("thead th")],
            ["产品名称", "订单数量", "节点名称"]
        )

        # 其中包括了刚刚乔治已经确认了报价的订单
        row = table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".product-name").text, "USB 32GB")
        self.assertEqual(row.find_element_by_css_selector(".order-amount").text, "1")
        self.assertEqual(row.find_element_by_css_selector(".record-title").text, "生产订单已确认")

        # 乔治点击了这个订单，页面跳转到了生产管理详情，和刚刚用供应商账户登陆时看到的大部分一致
        row.find_element_by_css_selector(".product-name a").click()

        self.assertRegex(self.browser.current_url, "/deals/production/details")

        record_table = self.browser.find_element_by_css_selector(".production-records table")

        # 表格内显示了第一条信息是：PO0001, 生产订单已确认，_, _, 2017年7月7号
        row = record_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".record-code").text, "PO0001")
        self.assertEqual(row.find_element_by_css_selector(".record-title").text, "生产订单已确认")
        self.assertEqual(row.find_element_by_css_selector(".date-intended").text, today)
        self.assertEqual(row.find_element_by_css_selector(".date-estimate").text, today)
        self.assertEqual(row.find_element_by_css_selector(".date-complete").text, today)

        # 页面右上角，乔治看到了发布生产状态按钮
        self.browser.find_element_by_css_selector(".add-record").click()

        # 页面跳转到了生产流程添加页面
        self.assertRegex(self.browser.current_url, "/deals/production/records/new")

        # 乔治模拟了工厂，填写了生产订单的新状态：”采购原材料“ 并发布
        form = self.browser.find_element_by_css_selector("form")
        form.find_element_by_id("id_code").send_keys("PO0002")
        form.find_element_by_id("id_title").send_keys("采购原材料")
        form.find_element_by_id("id_date_intended").send_keys(today)
        form.find_element_by_id("id_date_estimate").send_keys(today)
        form.find_element_by_id("id_date_complete").send_keys(today)
        form.find_element_by_id("id_submit").click()

        # 发布后，页面又跳回到了刚刚详情页面
        self.assertRegex(self.browser.current_url, "/deals/production/details")

        # 乔治发现刚刚的节点代号填写错了，点击了表格右边的修改那妞
        production_table = self.browser.find_element_by_css_selector(".production-records table")
        row = production_table.find_element_by_css_selector("tbody tr:nth-child(2)")
        self.assertEqual(row.find_element_by_css_selector(".record-code").text, "PO0002")
        row.find_element_by_css_selector(".edit").click()

        # 页面跳转到了修改生产订单页面，乔治把生产订单的节点代码更新后点击确认更新
        self.assertRegex(self.browser.current_url, "/deals/production/records/edit")
        form = self.browser.find_element_by_css_selector("form")
        form.find_element_by_id("id_code").clear()
        form.find_element_by_id("id_code").send_keys("PO0003")
        form.find_element_by_id("id_submit").click()

        # 页面再次回到详情页面, 看见刚刚的修改成功了
        self.assertRegex(self.browser.current_url, "/deals/production/details")
        production_table = self.browser.find_element_by_css_selector(".production-records table")
        row = production_table.find_element_by_css_selector("tbody tr:nth-child(2)")
        self.assertEqual(row.find_element_by_css_selector(".record-code").text, "PO0003")

        # 乔治觉得没有问题了并点击右上角的销售登陆, 乔治把自己把自己供应商登陆信息填写并登陆, 页面再次回到我的中心
        self.browser.find_element_by_css_selector("nav .sales-login").click()
        self._login(username="george", login_url=self.browser.current_url)

        # 然后乔治点击了生产订单列表，看到了刚才这个订单的最新名称为“采购原材料”
        self.browser.find_element_by_css_selector("nav .user-center").click()
        self.assertRegex(self.browser.current_url, "/auth/center")
        self.browser.find_element_by_css_selector(".production-dashboard").click()

        table = self.browser.find_element_by_css_selector(".production table")
        row = table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".record-title").text, "采购原材料")

        # 点击进去之后，确认了信息和工厂账户看到的完全一致，但是发现他自己不能添加或者修改里面的信息
        row.find_element_by_css_selector(".product-name a").click()
        self.assertRegex(self.browser.current_url, "/deals/production/details")
        production_table = self.browser.find_element_by_css_selector(".production-records table")
        row = production_table.find_element_by_css_selector("tbody tr:last-child")
        self.assertEqual(row.find_element_by_css_selector(".record-code").text, "PO0003")

            # 页面提示乔治，必须要用工厂账号才可以修改订单信息
        self.assertEqual(self.browser.find_element_by_css_selector(".warning-msg").text, "需要登陆工厂账号管理生产记录")
        # 乔治确认一切正常后退出了网站
        self._logout()

        # 正在此时，山姆登陆网页
        self._login(username="sam")

        # 山姆想去跟踪一下和乔治的订单进行的如何了
        # 山姆点击了我的订单，在待收货这栏里面看到了乔治的订单
        self.browser.find_element_by_css_selector("nav .user-center").click()
        self.browser.find_element_by_css_selector(".orders-dashboard").click()

        table = self.browser.find_element_by_css_selector(".on-road table")
        row = table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".product-name").text, "USB 32GB")
        self.assertEqual(row.find_element_by_css_selector(".product-amount").text, "1")
        self.assertEqual(row.find_element_by_css_selector(".offer-price").text, "1.99")
        row.find_element_by_css_selector(".product-name a").click()

        # 山姆点击进去，页面上方显示了商品信息，订单详情
        self.assertRegex(self.browser.current_url, "/deals/purchase_orders/on_road")
        self.assertEqual(self.browser.find_element_by_css_selector(".product-name").text, "USB 32GB")
        self.assertEqual(self.browser.find_element_by_css_selector(".order-amount").text, "1")
        self.assertEqual(self.browser.find_element_by_css_selector(".offer-price").text, "1.99")

        # 页面下方显示了生产环节表格，这个表格和乔治看的一致
        production_table = self.browser.find_element_by_css_selector(".production-records table")
        row = production_table.find_element_by_css_selector("tbody tr:first-child")
        self.assertEqual(row.find_element_by_css_selector(".record-code").text, "PO0001")
        self.assertEqual(row.find_element_by_css_selector(".record-title").text, "生产订单已确认")

        row = production_table.find_element_by_css_selector("tbody tr:nth-child(2)")
        self.assertEqual(row.find_element_by_css_selector(".record-code").text, "PO0003")
        self.assertEqual(row.find_element_by_css_selector(".record-title").text, "采购原材料")

        # 山姆也同样不能修改这个表格
        self.assertFalse(row.find_elements_by_css_selector(".edit"))

        # 山姆确认后也退出了网站
        self.browser.quit()