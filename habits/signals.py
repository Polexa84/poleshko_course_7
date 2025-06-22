from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Habit
from telegram_bot.tasks import send_telegram_notification

@receiver(post_save, sender=Habit)
def habit_created_or_updated(sender, instance, created, **kwargs):
    """
    Отправляет уведомление в Telegram при создании или обновлении привычки.
    """
    if created or instance.is_public: # Отправляем уведомление только если привычка создана или публична.
        send_telegram_notification.delay(instance.pk) # Запускаем Celery task