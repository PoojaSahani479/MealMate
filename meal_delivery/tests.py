from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Customers


class CustomerSignupSigninTests(TestCase):
    def test_signup_creates_hashed_password_and_redirects_to_signin(self):
        response = self.client.post(reverse('signup'), {
            'username': 'sam',
            'email': 'sam@example.com',
            'password': 'safe-password',
            'mobile': '1234567890',
            'address': 'Example street',
        })

        self.assertRedirects(response, reverse('open_signin'))
        customer = Customers.objects.get(username='sam')
        self.assertTrue(check_password('safe-password', customer.password))

    def test_signin_accepts_registered_credentials(self):
        Customers.objects.create(
            username='sam',
            email='sam@example.com',
            password='safe-password',
            mobile='1234567890',
            address='Example street',
        )

        response = self.client.post(reverse('signin'), {
            'username': 'sam',
            'password': 'safe-password',
        })

        self.assertRedirects(response, reverse('home'))
        customer = Customers.objects.get(username='sam')
        self.assertEqual(self.client.session['customer_id'], customer.pk)
        self.assertTrue(check_password('safe-password', customer.password))

    def test_staff_signin_redirects_to_admin_home(self):
        admin = get_user_model().objects.create_user(
            username='admin',
            password='admin-password',
            is_staff=True,
        )

        response = self.client.post(reverse('signin'), {
            'username': 'admin',
            'password': 'admin-password',
        })

        self.assertRedirects(response, reverse('admin_home'))
        self.assertEqual(int(self.client.session['_auth_user_id']), admin.pk)

    def test_customer_cannot_open_admin_home(self):
        Customers.objects.create(
            username='sam',
            email='sam@example.com',
            password='safe-password',
            mobile='1234567890',
            address='Example street',
        )

        response = self.client.get(reverse('admin_home'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_signin_rejects_invalid_credentials(self):
        response = self.client.post(reverse('signin'), {
            'username': 'missing',
            'password': 'wrong-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password.')
