from django.test import TestCase

from UserManagement.models import UserManageModel
from UserManagement.serializers import UserRegistrationSerializer, UserProfileSerializer
from rest_framework.test import APITestCase


# userManagement Serializers:

class TestUserRegistrationSerializer(TestCase):
    def test_serializer_valid_data(self):

        test_data = {
            'username': 'test_user',
            'email': 'test_mail@example.com',
            'password': 'test_password',
            'password2': 'test_password'
        }

        serializer = UserRegistrationSerializer(data=test_data)
        self.assertTrue(serializer.is_valid())

        expected_data = {
            'username': 'test_user',
            'email': 'test_mail@example.com',

        }
        self.assertEqual(serializer.data, expected_data)

    def test_password_mismatch(self):
        test_data = {
            'username': 'test_user',
            'email': 'test_mail@example.com',
            'password': 'test_password',
            'password2': 'different_password'
        }

        serializer = UserRegistrationSerializer(data=test_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'][0], 'Passwords do not match!')

    def test_serializer_create(self):
        test_data = {
            'username': 'test_user',
            'email': 'test_mail@example.com',
            'password': 'test_password',
            'password2': 'test_password'
        }
        serializer = UserRegistrationSerializer(data=test_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test_mail@example.com')
        self.assertTrue(user.check_password('test_password'))

    def test_serializer_with_existing_username_or_email(self):
        existing_user = UserManageModel.objects.create_user(
            username='existing_user',
            email='existing_email@example.com',
            password='existing_password'
        )

        test_data = {
            'username': 'existing_user',
            'email': 'test_mail@example.com',
            'password': 'test_password',
            'password2': 'test_password'
        }

        serializer = UserRegistrationSerializer(data=test_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

        test_data = {
            'username': 'test_user',
            'email': 'existing_email@example.com',
            'password': 'test_password',
            'password2': 'test_password'
        }

        serializer = UserRegistrationSerializer(data=test_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'][0], 'Email already exists.')


class TestUserProfileSerializer(APITestCase):
    def setUp(self):
        self.user = UserManageModel.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            address='123 Test Street',
            phone_number='1234567890'
        )

    def tearDown(self):
        UserManageModel.objects.all().delete()

    def test_serialize_user_profile(self):
        serializer = UserProfileSerializer(instance=self.user)

        expected_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone_number': '1234567890',
            'address': '123 Test Street',
        }
        self.assertEqual(serializer.data, expected_data)

        self.assertEqual(serializer.data, expected_data)

    def test_update_user_profile(self):
        updated_data = {
            'address': '456 Test Avenue',
            'phone_number': '0987654321'
        }
        serializer = UserProfileSerializer(instance=self.user, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.address, '456 Test Avenue')
        self.assertEqual(self.user.phone_number, '0987654321')



