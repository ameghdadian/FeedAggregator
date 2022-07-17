from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_successful(self):
        '''Test creating a new user is successful'''
        username = 'Test User'
        password = 'Test password'

        user = get_user_model().objects.create_user(
            username=username,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_superuser_successful(self):
        '''Test creating a superuser is successful'''
        username = 'Test User'
        password = 'Test password'

        user = get_user_model().objects.create_superuser(
            username=username,
            password=password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
