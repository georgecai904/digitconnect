from django.test import TestCase
from core.forms import NewUserForm
from django.contrib.auth.models import User

class AuthTest(TestCase):

    def test_sign_up(self):
        data = {
            "username": "georgecai904",
            "password": "testpassword",
            "email": "mail@georgecai.com"
        }
        NewUserForm(data).save()
        self.assertEqual(User.objects.count(), 1)
