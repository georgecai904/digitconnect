from django.test import TestCase
from purchasers.forms import NewPurchaserForm
from purchasers.models import Purchaser
from django.contrib.auth.models import User
from unittest import skip


class CreateSupplierTest(TestCase):
    def setUp(self):
        user = self._create_new_user()
        self._login(user)
        self.response = self.client.get('/purchasers/new')

    @staticmethod
    def _create_new_user():
        user = User.objects.create(username="george")
        user.set_password("yiming123")
        user.save()
        return user

    def _login(self, user):
        self.client.login(username=user.username, password="yiming123")

    def _create_new_purchaser(self):
        return self.client.post(
            '/purchasers/new',
            data={
                'name': "Sam",
                'phone': "13868892809",
                'address': "上海市浦东新区罗山路1502号10号楼502室",
                'location': "江浙沪",
                'license': "G92719234",
                'area': 'IT行业'
            },
        )

    def test_new_purchaser_template_load(self):
        self.assertTemplateUsed(self.response, "purchasers/purchaser_form.html")

    def test_new_purchaser_form_load(self):
        self.assertIsInstance(self.response.context['form'], NewPurchaserForm)

    def test_new_purchaser_created(self):
        self.response = self._create_new_purchaser()
        self.assertEqual(Purchaser.objects.count(), 1)

    @skip
    def test_new_purchaser_created_redirect(self):
        self.response = self._create_new_purchaser()
        self.assertEqual(self.response.status_code, 302)


class SupplierModelTest(TestCase):
    def _create_new_user(self):
        user = User.objects.create(username="george")
        user.password("hello")
        user.save()
        return user

    @skip
    def test_purchaser_reated(self):
        user = self._create_new_user()
        p = Purchaser.objects.create(name='Sam', user=user)
        self.assertEqual(p, Purchaser.objects.first())
        self.assertEqual(p.name, Purchaser.objects.first().name)
