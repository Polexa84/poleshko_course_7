import logging
import requests
from celery import shared_task
from django.conf import settings
from .models import TelegramUser
from habits.models import Habit
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()


def send_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при отправке сообщения в Telegram: {e}")


@shared_task
def send_telegram_notification(habit_id):
    """
    Отправляет уведомление в Telegram о привычке.
    """
    try:
        habit = Habit.objects.get(pk=habit_id)
        telegram_user = TelegramUser.objects.get(user=habit.user)
        telegram_id = telegram_user.telegram_id
        bot_token = settings.TELEGRAM_BOT_TOKEN

        message = f"Напоминание: Пора выполнить привычку '{habit.action}' в {habit.time} в {habit.place}."
        send_message(bot_token, telegram_id, message)

        logger.info(f"Уведомление отправлено в Telegram пользователю {habit.user.username} ({telegram_id})")

    except Habit.DoesNotExist:
        logger.error(f"Привычка с ID {habit_id} не найдена.")
    except TelegramUser.DoesNotExist:
        logger.error(f"TelegramUser для пользователя {habit.user.username} не найден.")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления в Telegram: {e}")

@shared_task
def process_telegram_message(message_json):
    """
    Обрабатывает входящие сообщения от Telegram.
    """
    try:
        logger.info("Received message from Telegram")  # Add this line
        message = message_json['message']
        chat_id = message['chat']['id']
        text = message['text']
        bot_token = settings.TELEGRAM_BOT_TOKEN

        if text == '/start':
            logger.info("Received /start command")  # Add this line
            # Получаем user_id из message (если он есть)
            user_id = None
            entities = message.get('entities', [])
            for entity in entities:
                if entity['type'] == 'mention':
                    username = message['text'][entity['offset'] + 1:entity['offset'] + entity['length']]
                    try:
                        logger.info(f"Trying to find user with username: {username}")  # Add this line
                        user = User.objects.get(username=username)
                        user_id = user.id
                        logger.info(f"User found with ID: {user_id}")  # Add this line
                    except User.DoesNotExist:
                        logger.warning(f"User with username {username} not found.")  # Add this line
                        pass

            # Если user_id не найден, отправляем сообщение с просьбой указать имя пользователя
            if not user_id:
                send_message(bot_token, chat_id, "Пожалуйста, укажите ваше имя пользователя Django после команды /start, например: /start your_username")
                return

            try:
                # Пытаемся найти TelegramUser по user_id
                telegram_user = TelegramUser.objects.get(user_id=user_id)
                telegram_user.telegram_id = chat_id
                telegram_user.save()
                send_message(bot_token, chat_id, f"Telegram ID успешно обновлен для пользователя {telegram_user.user.username}!")
            except TelegramUser.DoesNotExist:
                # Если TelegramUser не существует, создаем его
                user = User.objects.get(pk=user_id)
                TelegramUser.objects.create(user=user, telegram_id=chat_id)
                send_message(bot_token, chat_id, f"Telegram ID успешно зарегистрирован для пользователя {user.username}!")
            except User.DoesNotExist:
                send_message(bot_token, chat_id, "Пользователь с таким именем не найден.")
            except Exception as e:
                logger.error(f"Ошибка при обработке команды /start: {e}")
        else:
            send_message(bot_token, chat_id, "Я понимаю только команду /start.")
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения Telegram: {e}")