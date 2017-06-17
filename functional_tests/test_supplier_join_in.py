from functional_tests.base import FunctionalTest


class SupplierJoinInTest(FunctionalTest):

    def test_supplier_join_in(self):

        # 山姆是一个供应商，他登陆了网站
        self.browser.get(self.live_server_url)

        # 山姆看到导航栏上有"申请入驻"的标志
        # 山姆点击进去
        x = self.browser.find_element_by_css_selector("nav .join-in").click()
        self.assertRegex(self.browser.current_url, '/suppliers/new')

        # 进去之后，山姆发现页面呈现出一个表格，需要填写相关的信息
        forms = self.browser.find_elements_by_tag_name('form')
        self.assertEqual(len(forms), 1)


        # 山姆按照需要的信息填写进去并提交
        form = forms[0]
        form.find_element_by_id('name').send_keys("Sam")
        form.find_element_by_id('phone').send_keys("13868892809")
        form.find_element_by_id('address').send_keys("上海市浦东新区罗山路1502号10号楼502室")
        form.find_element_by_id('location').send_keys("江浙沪")
        form.find_element_by_id('license').send_keys("G92719234")
        form.find_element_by_id('area').send_keys('IT行业')
        form.find_element_by_tag_name('button').click()

        # 提交之后，网站回到首页，并在首页上方显示入驻成功
        self.assertEqual(self.browser.current_url, self.live_server_url)
        messages = self.browser.find_elements_by_css_selector('.message')
        self.assertIn("入驻成功", [message.text for message in messages])