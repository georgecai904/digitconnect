from django.test import TestCase
from suppliers.forms import NewSupplierForm
from suppliers.models import Supplier


class CreateSupplierTest(TestCase):

    def setUp(self):
        self.response = self.client.get('/suppliers/new')

    def create_new_supplier(self):
        return self.client.post(
            '/suppliers/new',
            data={
                'name': "Sam",
                'phone': "13868892809",
                'address': "上海市浦东新区罗山路1502号10号楼502室",
                'location': "江浙沪",
                'license': "G92719234",
                'area': 'IT行业'
            }
        )

    def test_new_supplier_template_load(self):
        self.assertTemplateUsed(self.response, "suppliers/new_supplier.html")

    def test_new_supplier_form_load(self):
        self.assertIsInstance(self.response.context['form'], NewSupplierForm)

    def test_new_supplier_created(self):
        self.response = self.create_new_supplier()
        self.assertEqual(Supplier.objects.count(), 1)

    def test_new_supplier_created_redirect(self):
        self.response = self.create_new_supplier()
        self.assertEqual(self.response.status_code, 302)


class SupplierModelTest(TestCase):

    def test_supplier_reated(self):
        s = Supplier.objects.create(name='Sam')
        self.assertEqual(s, Supplier.objects.first())
        self.assertEqual(s.name, Supplier.objects.first().name)
