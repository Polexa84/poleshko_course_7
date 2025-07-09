import logging
import requests
from celery import shared_task
from celery.utils.log import get_task_logger  # Специальный логгер для Celery
from django.conf import settings
from .models import TelegramUser
from habits.models import Habit
from django.contrib.auth import get_user_model
from requests.exceptions import RequestException

# Используем специальный логгер Celery
logger = get_task_logger(__name__)
User = get_user_model()

def send_message(bot_token, chat_id, text):
    """Улучшенная функция отправки сообщений с обработкой ошибок"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"  # Добавляем поддержку разметки
    }
    try:
        response = requests.post(url, data=data, timeout=10)  # Таймаут 10 сек
        response.raise_for_status()
        return True
    except RequestException as e:
        logger.error(f"Ошибка отправки в Telegram: {e}\nURL: {url}\nData: {data}")
        return False

@shared_task(bind=True, max_retries=3)  # Добавляем автоматические повторы
def send_telegram_notification(self, habit_id):
    """Улучшенная задача отправки уведомлений"""
    try:
        logger.info(f"Начало обработки привычки ID: {habit_id}")

        habit = Habit.objects.select_related('user').get(pk=habit_id)
        telegram_user = TelegramUser.objects.get(user=habit.user)

        message = (
            f"⏰ Напоминание:\n"
            f"Привычка: *{habit.action}*\n"
            f"Время: {habit.time.strftime('%H:%M') if habit.time else 'не указано'}\n"
            f"Место: {habit.place or 'не указано'}"
        )

        #  Исправлено на использование telegram_user.tg_chat_id
        if not send_message(settings.TELEGRAM_BOT_TOKEN, telegram_user.tg_chat_id, message):
            logger.warning(f"Не удалось отправить сообщение для habit_id={habit_id}")
            self.retry(countdown=60)  # Повторить через 60 сек

        logger.info(f"Успешно отправлено уведомление пользователю {habit.user.email}") # Используем email

    except Habit.DoesNotExist as e:
        logger.error(f"Привычка не найдена: {e}")
    except TelegramUser.DoesNotExist as e:
        logger.error(f"TelegramUser не найден: {e}")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        self.retry(exc=e, countdown=300)  # Повторить через 5 мин

@shared_task(bind=True)
def process_telegram_message(self, message_json):
    """Улучшенная обработка входящих сообщений"""
    try:
        logger.info(f"Получено сообщение: {message_json}")

        message = message_json['message']
        chat_id = message['chat']['id']
        text = message.get('text', '').strip()
        bot_token = settings.TELEGRAM_BOT_TOKEN

        if text.startswith('/start'):
            logger.info("Обработка команды /start")

            # Извлекаем email из команды (/start email@example.com)
            email = text[7:].strip() if len(text) > 7 else None

            if not email:
                send_message(bot_token, chat_id, "Введите: /start ваш_email@example.com")
                return

            try:
                user = User.objects.get(email=email)
                TelegramUser.objects.update_or_create(
                    user=user,
                    defaults={'telegram_id': chat_id, 'tg_chat_id': chat_id}
                )
                send_message(bot_token, chat_id,
                             f"✅ Привязан аккаунт: {user.email}\n"
                             f"Теперь вы будете получать уведомления!")
            except User.DoesNotExist:
                send_message(bot_token, chat_id, "❌ Пользователь не найден")
                logger.warning(f"Пользователь не найден: {email}")

        else:
            send_message(bot_token, chat_id,
                         "Я понимаю только команду /start\n"
                         "Пример: /start ваш_email@example.com")

    except KeyError as e:
        logger.error(f"Ошибка формата сообщения: {e}\n{message_json}")
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}", exc_info=True)
        self.retry(exc=e, countdown=60)