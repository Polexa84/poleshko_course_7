from django.test import TestCase
from .models import TelegramUser
from django.contrib.auth import get_user_model
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json

User = get_user_model()

class TelegramBotTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',  # Добавлено username
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='password123'
        )
        self.telegram_user = TelegramUser.objects.create(
            user=self.user,
            telegram_id='123456789',
            tg_chat_id='987654321'
        )
        self.client = APIClient()

    def test_telegram_user_creation(self):
        self.assertEqual(TelegramUser.objects.count(), 1)
        self.assertEqual(self.telegram_user.user, self.user)
        self.assertEqual(self.telegram_user.telegram_id, '123456789')
        self.assertEqual(self.telegram_user.tg_chat_id, '987654321')