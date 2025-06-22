from celery import shared_task
import telegram
from django.conf import settings
from .models import TelegramUser
from habits.models import Habit

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

        bot = telegram.Bot(token=bot_token)
        message = f"Напоминание: Пора выполнить привычку '{habit.action}' в {habit.time} в {habit.place}."

        bot.send_message(chat_id=telegram_id, text=message)
        print(f"Уведомление отправлено в Telegram пользователю {habit.user.username} ({telegram_id})")

    except Habit.DoesNotExist:
        print(f"Привычка с ID {habit_id} не найдена.")
    except TelegramUser.DoesNotExist:
        print(f"TelegramUser для пользователя {habit.user.username} не найден.")
    except Exception as e:
        print(f"Ошибка при отправке уведомления в Telegram: {e}")