from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
MANAGE_USER_URL = reverse('user:manage_user')


def create_user(**kwargs):
    """Helper function for creating a user"""
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """

    """

    def setUp(self):
        """

        """
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """

        """

        payload = {
            'email': 'noreply@ntc.com',
            'password': 'password123',
            'name': 'John Smith'
        }
        r = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**r.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', r.data)

    def test_user_exists(self):
        """

        """

        payload = {
            'email': 'noreply@ntc.com',
            'password': 'password123',
            'name': 'John Smith'
        }
        create_user(**payload)

        r = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """

        """

        payload = {
            'email': 'noreply@ntc.com',
            'password': 'pass',
            'name': 'John Smith'
        }
        r = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """

        """

        payload = {
            'email': 'noreply@ntc.com',
            'password': 'pass1234',
            'name': 'John Smith'
        }
        create_user(**payload)

        r = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', r.data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_creds(self):
        """

        """

        create_user(email='noreply@ntc.com', password='pass1234')
        payload = {
            'email': 'noreply@ntc.com',
            'password': 'wrongpass1234'
        }
        r = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', r.data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """

        """

        payload = {
            'email': 'noreply@ntc.com',
            'password': 'pass1234',
            'name': 'John Smith'
        }
        r = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', r.data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """

        """

        payload = {
            'email': 'noreply@ntc.com',
            'password': '',
            'name': 'John Smith'
        }
        r = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', r.data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """

        """

        r = self.client.get(MANAGE_USER_URL)

        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """

    """

    def setUp(self):
        """

        """
        self.user = create_user(
            email='noreply@ntc.com',
            password='password123',
            name='John Smith'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retreive_profile_success(self):
        """

        """
        r = self.client.get(MANAGE_USER_URL)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(
            r.data,
            {
                'name': self.user.name,
                'email': self.user.email
            }
        )

    def test_post_manage_user_not_allowed(self):
        """

        """
        r = self.client.post(MANAGE_USER_URL)

        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """

        """
        payload = {
            'name': 'new name',
            'password': 'newpass1234'
        }

        r = self.client.patch(MANAGE_USER_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
