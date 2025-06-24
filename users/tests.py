from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('register')
        self.valid_payload = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'password123',
            'password2': 'password123'
        }
        self.invalid_payload = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'password123',
            'password2': 'wrongpassword'
        }

    def test_register_user_with_valid_data(self):
        response = self.client.post(self.registration_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_register_user_with_invalid_data(self):
        response = self.client.post(self.registration_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

class UserLoginTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(  # Изменено
            username='testuser',  # Добавлено username
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='password123',
        )
        self.valid_payload = {
            'email': 'test@example.com', # Используем email
            'password': 'password123'
        }
        self.invalid_payload = {
            'email': 'test@example.com', # Используем email
            'password': 'wrongpassword'
        }

    def test_login_user_with_valid_data(self):
        response = self.client.post(self.login_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_user_with_invalid_data(self):
        response = self.client.post(self.login_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Или другой код ошибки