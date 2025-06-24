from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Habit

User = get_user_model()

class HabitTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(  # Изменено
            username='testuser',  # Добавлено username
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)  # Аутентифицируем клиента
        self.habit_url = reverse('habit-list')  # Предполагается, что у вас есть URL с именем 'habit-list'
        self.valid_payload = {
            'user': self.user.pk,  # Не нужно передавать user_id, он будет установлен автоматически
            'action': 'Read a book',
            'place': 'Library',
            'time': '10:00',
            'execution_time': 60,  # Укажите корректное время выполнения
            'is_public': True
        }

    def tearDown(self):
        # Очищаем базу данных после каждого теста
        Habit.objects.all().delete()
        User.objects.all().delete()

    def test_create_habit_with_valid_data(self):
        response = self.client.post(self.habit_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().action, 'Read a book')
        self.assertEqual(Habit.objects.get().user, self.user) # Проверяем, что привычка принадлежит текущему пользователю
