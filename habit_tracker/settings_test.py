# settings_test.py
from .settings import *  # Импортируем все из settings.py

CELERY_TASK_ALWAYS_EAGER = True  # Отключаем Celery
CELERY_TASK_STORE_EAGER_RESULT = True # Сохраняем результаты задач