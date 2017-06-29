from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


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

    def _create_user(self):
        from django.contrib.auth.models import User
        u = User.objects.create(username="georgecai904", email="test@test.com")
        u.set_password("testpassword")
        u.save()
        return u

    def _create_purchaser(self):
        u = self._create_user()
        from clients.models import Purchaser
        p = Purchaser.objects.create(
            user=u,
            name="山姆采购商",
            phone="13868892809",
            address="上海市浦东新区罗山路1502号10号楼502室",
            location="江浙沪",
            license="G92719234",
            area="IT行业"
        )
        return p

    def _create_product(self):
        purchaser = self._create_purchaser()
        from products.models import Product
        p = Product.objects.create(
            purchaser=purchaser,
            name='B&O音响',
            image='/images/product.jpg',
            category='高档音响',
            amount='100',
            location='江浙沪',
        )

        return p

    def _stop(self, sleep_time=10):
        import time
        time.sleep(sleep_time)