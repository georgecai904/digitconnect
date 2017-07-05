from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import skip

class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(FunctionalTest, cls).setUpClass()
        cls.browser = webdriver.Chrome(executable_path="/driver/chromedriver")
        # cls.live_server_url = "http://localhost:8000"

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(FunctionalTest, cls).tearDownClass()

    def _create_user(self, username="purchaser1"):
        email = "{}@dc.com".format(username)
        password = "testpassword"
        from django.contrib.auth.models import User
        u = User.objects.create(username=username, email=email)
        u.set_password(password)
        u.save()
        return u

    def _create_purchaser(self, username="purchaser1", name="山姆采购商"):
        u = self._create_user(username=username)
        from clients.models import Purchaser
        p = Purchaser.objects.create(
            user=u,
            name=name,
            phone="13868892809",
            address="上海市浦东新区罗山路1502号10号楼502室",
            location="江浙沪",
            license="G92719234",
            area="IT行业"
        )
        return p

    def _create_supplier(self, username, name="华少供应"):
        u = self._create_user(username=username)
        from clients.models import Supplier
        s, created = Supplier.objects.update_or_create(
            user=u,
            name=name,
            phone="12839991231",
            address="上海自贸区11号",
            location="江浙沪",
            license="H182119821",
            area="IT行业"
        )
        return s

    def _create_product(self, purchaser, name='B&O音响'):
        from stocks.models import Product
        p = Product.objects.create(
            purchaser=purchaser,
            name=name,
            image='/images/product.jpg',
            category='高档音响',
            location='江浙沪',
        )

        return p

    def _create_purchase_order(self, initiator, product, amount):
        from deals.models import PurchaseOrder
        po = PurchaseOrder.objects.create(
            initiator=initiator,
            product=product
        )
        po.add_purchaser(purchaser=initiator, amount=amount)
        return po


    def _stop(self, sleep_time=10):
        import time
        time.sleep(sleep_time)

    def _login(self, username, password="testpassword", login_url=None):
        if not login_url:
            self.browser.get(self.live_server_url)
            self.browser.find_element_by_css_selector("nav .login").click()
        else:
            self.browser.get(login_url)
        login_form = self.browser.find_element_by_css_selector("form")
        login_form.find_element_by_id("id_username").send_keys(username)
        login_form.find_element_by_id("id_password").send_keys(password)
        # self._stop()
        login_form.find_element_by_id("id_submit").click()

    def _refresh(self):
        self.browser.get(self.browser.current_url)