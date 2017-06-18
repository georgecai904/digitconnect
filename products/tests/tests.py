from django.test import TestCase
from products.models import Product
# Create your tests here.


class CreateProductTest(TestCase):

    def setUp(self):
        self.response = self.client.get('/products/new')

    def create_product(self):
        return self.client.post(
            '/products/new',
            data={
                "name": "B&O音响",
                "image": "/images/product.jpg",
                "amount": "10",
                "location": "江浙沪",
                "category": "音像制品"
            }
        )

    def test_new_product_template_load(self):
        self.assertTemplateUsed(self.response, 'products/new_product.html')

    def test_new_product_redirect_after_created(self):
        self.response = self.create_product()
        self.assertEqual(self.response.status_code, 302)

    def test_new_product_created(self):
        self.response = self.create_product()
        self.assertEqual(Product.objects.count(), 1)