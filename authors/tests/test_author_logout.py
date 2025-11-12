from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        respose = self.client.get(
            reverse('authors:logout'),
            follow=True
        )

        self.assertIn(
            'Invalid logout request',
            respose.content.decode('utf-8')
        )

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        respose = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'another_user'
            },
            follow=True
        )

        self.assertIn(
            'Invalid logout user',
            respose.content.decode('utf-8')
        )

    def test_user_tries_to_logout_successfully(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        respose = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'my_user'
            },
            follow=True
        )

        self.assertIn(
            'Logged out successfully',
            respose.content.decode('utf-8')
        )
