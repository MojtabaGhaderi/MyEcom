from django.test import Client, TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

from UserManagement.models import UserManageModel


class TestUserRegistrationView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('registration')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'password2': 'testpassword',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(UserManageModel.objects.count(), 1)
        user = UserManageModel.objects.first()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'example')

    def test_user_registration_with_missing_data(self):
        url = reverse('registration')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(UserManageModel.objects.count(), 0)

    def test_user_registration_with_password_mismatch(self):
        url = reverse('registration')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'password2': 'wrongpassword',
        }
        response = self.client.post(url, data, format='jason')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(UserManageModel.objects.count(), 0)
