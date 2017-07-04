from functional_tests.base import FunctionalTest
import unittest


class IndexPageViewTest(FunctionalTest):
    def setUp(self):
        # 乔治打开浏览器登陆网站
        self.browser.get(self.live_server_url)

    def test_user_view_index_page(self):
        # 乔治看到了网页的名称叫做 Direct Connect
        self.assertEqual(self.browser.title, "Direct Connect")

        # 乔治看到了一条目录栏, 目录栏的名称叫做 “欢迎来到 Direct Connect”
        nav_title = self.browser.find_element_by_css_selector(".navbar-header a")
        self.assertEqual(nav_title.text, "欢迎来到 Direct Connect")

        # 目录栏里面分别有主页，论坛，展会，电子会议，申请入驻，公司介绍
        expected_list = ["主页", "论坛", "展会", "电子会议",
                         "申请入驻", "公司介绍", "发布订单"]
        nav_list = self.browser.find_elements_by_css_selector("nav .menus li")

        self.assertEqual(
            [nav_item.text for nav_item in nav_list],
            expected_list
        )

        # 其中主页的状态是激活的
        nav_bar_item = self.browser.find_element_by_css_selector(".navbar-list li:first-child")
        self.assertIn("active", nav_bar_item.get_attribute("class"))

        # 乔治在目录栏的下方看到了新品广告栏
        adv_bar = self.browser.find_element_by_css_selector(".advbar")

        # 广告栏里面放这一张"欢迎光临"照片
        adv_bar_image = adv_bar.find_element_by_tag_name("img")
        self.assertEqual(adv_bar_image.get_attribute("src"), self.live_server_url+"/static/images/welcome.png")

        # 乔治在新品广告栏的下方看到买家发布的商品列表
        product_list = self.browser.find_elements_by_css_selector(".product-container")

        if product_list:
            first_product = product_list[0]
            # 每排显示四个商品
            self.assertIn("col-md-3", first_product.get_attribute("class"))

            # 每个商品格内显示了产品图片
            self.assertNotEqual(first_product.find_element_by_css_selector(".product-image"), None)
            # 图片下方显示商品信息，包括产品类别，数量，送货地点
            self.assertNotEqual(first_product.find_element_by_css_selector(".product-category"), None)
            self.assertNotEqual(first_product.find_element_by_css_selector(".product-amount"), None)
            self.assertNotEqual(first_product.find_element_by_css_selector(".product-location"), None)

            # 商品信息下面有三个按钮
            buttons = first_product.find_elements_by_tag_name("button")
            self.assertEqual(len(buttons), 3)
            # 按钮名字分别为报价，加入采购，在线交流
            self.assertEqual([button.text for button in buttons], ["报价", "加入采购", "在线交流"])
