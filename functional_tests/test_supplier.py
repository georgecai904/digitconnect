from functional_tests.base import FunctionalTest
from unittest import skip

class SupplierFunctionalTest(FunctionalTest):

    def test_supplier_post_price(self):
        purchaser = self._create_purchaser()
        p = self._create_product(purchaser)

        # 华少是一个高端音响制造公司的销售员，他从朋友那里了解到了该网站
        # 华少打开了这个网站
        self.browser.get(self.live_server_url)

        # 华少在网页上看到了山姆发布的采购需求
        product_container = self.browser.find_element_by_css_selector(".product-container:first-child")
        self.assertEqual(product_container.find_element_by_css_selector(".purchaser-name .value").text, "山姆采购商")

        # 华少对山姆的采购需求很感兴趣，便点击报价
        product_container.find_element_by_css_selector(".post-price").click()

        # 页面跳转到了一个登陆页面
        self.assertRegex(self.browser.current_url, "/auth/login")

        # 华少由于没有对应的账号，于是便注册
        self.browser.find_element_by_css_selector("form #id_sign-up").click()
        form = self.browser.find_element_by_tag_name("form")
        form.find_element_by_id("id_username").send_keys("supplier1")
        form.find_element_by_id("id_password").send_keys("testpassword")
        form.find_element_by_id("id_email").send_keys("supplier1@dc.com")
        form.find_element_by_id("id_submit").click()

        # 注册完了之后，页面跳转到了登陆页面
        self.assertRegex(self.browser.current_url, '/auth/login')
        form = self.browser.find_element_by_tag_name("form")
        form.find_element_by_id("id_username").send_keys("supplier1")
        form.find_element_by_id("id_password").send_keys("testpassword")
        form.find_element_by_id("id_submit").click()

        # 华少登陆之后进入身份创建页面，华少选择了供应商
        self.browser.find_element_by_css_selector(".client-supplier").click()

        # 华少对应的填写好了自己所有的信息
        self.assertRegex(self.browser.current_url, "/suppliers/new")
        form = self.browser.find_element_by_css_selector("form")
        form.find_element_by_id('id_name').send_keys("华少供应")
        form.find_element_by_id('id_phone').send_keys("12839991231")
        form.find_element_by_id('id_address').send_keys("上海自贸区11号")
        form.find_element_by_id('id_location').send_keys("江浙沪")
        form.find_element_by_id('id_license').send_keys("H182119821")
        form.find_element_by_id('id_area').send_keys('IT行业')
        form.find_element_by_id('id_submit').click()

        # 页面跳转到了首页，华少找到刚刚山姆发布报价按钮，点击进去
        self.assertRegex(self.browser.current_url, "/")
        self.browser.find_element_by_css_selector(".product-container:first-child .post-price").click()

        # 页面跳转到了刚刚的报价页面，页面左边显示了商品信息，右边是一个报价表格，里面需要填写最大供应数量及价格
        self.assertRegex(self.browser.current_url, "/suppliers/post-price")
        self.assertEqual(
            self.browser.find_element_by_css_selector(".product-container .product-name .value").text, "B&O音响")

        # 华少填写好了这些信息并提交
        # self._stop()
        form = self.browser.find_element_by_css_selector("form")
        form.find_element_by_id("id_price").send_keys("100")
        form.find_element_by_id("id_amount").send_keys("10000")
        form.find_element_by_id('id_submit').click()

        # 华少提交后，页面显示了他刚刚填写的信息以及山姆的采购需求
        # 页面提示华少，他的报价已经提交，并提示华少，若采购商感兴趣，会进一步与您联系
        self.assertRegex(self.browser.current_url, "/suppliers/post-price")
        self.assertEqual(
            self.browser.find_element_by_css_selector(".product-container .product-name .value").text, "B&O音响")
        self.assertEqual(
            self.browser.find_element_by_css_selector(".post-price-container .post-price .value").text, "100"
        )
        self.assertEqual(
            self.browser.find_element_by_css_selector(".alert.alert-success").text, "您的报价已提交，若采购商感兴趣，会进一步与您联系"
        )

        # 华少点击返回主页，页面跳回到了首页
        self.browser.find_element_by_css_selector(".back").click()
        self.assertRegex(self.browser.current_url, "/")

