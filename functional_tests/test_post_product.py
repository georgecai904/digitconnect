from functional_tests.base import FunctionalTest


class PostNewProductTest(FunctionalTest):

    def test_post_new_product(self):
        # 山姆成功注册后，回到首页，他看到了菜单栏最右边的 "产品发布"
        self.browser.get(self.live_server_url)
        post_product_link = self.browser.find_element_by_css_selector("nav li:last-child")
        self.assertIn("产品发布", post_product_link.text)

        # 山姆有一些产品向发布，于是他便点了进去
        post_product_link.click()
        self.assertEqual(self.browser.current_url, self.live_server_url + "/products/new")

        # 和之前注册一样，页面跳转到了一个表单页面
        form = self.browser.find_element_by_tag_name()

        # 山姆将他想要发布的商品以此都填写进去
        form.find_element_by_id('id_name').send_keys('B&O 音响')
        form.find_element_by_id('id_image').send_keys('/images/product.jpg')
        form.find_element_by_id('id_category').send_keys('高档音响')
        form.find_element_by_id('id_amount').send_keys('100')
        form.find_element_by_id('id_location').send_keys('江浙沪')

        # 山姆填写并成功提交了
        form.find_element_by_id('id_submit').click()

        # 提交后，页面跳转到了首页，山姆成功的在首页的商品列表里面看到了他刚刚发布的产品
        self.assertEqual(self.browser.current_url, self.live_server_url+"/")
        container = self.browser.find_element_by_css_selector(".product-container:first-child")
        self.assertEqual(container.find_element_by_css_selector(".product-name").text, 'B&O 音响')
