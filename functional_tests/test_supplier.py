from functional_tests.base import FunctionalTest
from unittest import skip

class SupplierFunctionalTest(FunctionalTest):

    def test_supplier_register_in(self):
        purchaser = self._create_purchaser()
        purchaser = self._create_purchaser(username="purchaser2", name="山姆采购商")
        product = self._create_product(purchaser=purchaser, name="USB 64GB")
        purchase_offer = self._create_purchase_order(initiator=purchaser, product=product, amount=1000)

        # 华少是一个高端音响制造公司的销售员，他从朋友那里了解到了该网站
        # 华少打开了这个网站
        self.browser.get(self.live_server_url)

        # 华少在网页上看到了山姆发布的采购需求
        product_container = self.browser.find_element_by_css_selector(".product-container:first-child")
        self.assertEqual(product_container.find_element_by_css_selector(".purchaser-name .value").text, "山姆采购商")

        # 华少对山姆的采购需求很感兴趣，便点击报价
        product_container.find_element_by_css_selector(".make-offer").click()

        # 页面跳转到了一个登陆页面
        self.assertRegex(self.browser.current_url, "/auth/login")

        # 华少由于没有对应的账号，于是便注册
        self.browser.find_element_by_css_selector("form #id_sign-up").click()
        form = self.browser.find_element_by_tag_name("form")
        form.find_element_by_id("id_username").send_keys("supplier2")
        form.find_element_by_id("id_password").send_keys("testpassword")
        form.find_element_by_id("id_email").send_keys("supplier1@dc.com")
        form.find_element_by_id("id_submit").click()

        # 注册完了之后，页面跳转到了登陆页面
        self.assertRegex(self.browser.current_url, '/auth/login')
        form = self.browser.find_element_by_tag_name("form")
        form.find_element_by_id("id_username").send_keys("supplier2")
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

        # 华少注册好了之后，跳回到了首页
        self.assertRegex(self.browser.current_url, "/")

        # (TODO: 华少想看下自己的供应商信息是否正确）
