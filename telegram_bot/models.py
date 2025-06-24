from django.db import models
from django.conf import settings

class TelegramUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='telegram_user')
    telegram_id = models.CharField(max_length=255, verbose_name='Telegram ID')
    telegram_username = models.CharField(max_length=255, blank=True, null=True, verbose_name='Имя пользователя Telegram') # Добавлено
    tg_chat_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Telegram Chat ID')  # Добавлено

    def __str__(self):
        return f"Telegram user for {self.user.email}" # Возвращаем email пользователя Django