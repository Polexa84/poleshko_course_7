import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')

app = Celery('habit_tracker',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['telegram_bot.tasks'])

# Настройка Celery
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()