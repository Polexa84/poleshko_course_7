import os
from celery import Celery
from django.apps import apps
import logging

# Настройка логгера
logger = logging.getLogger(__name__)

# 1. Обязательная инициализация Django ДО создания celery app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')

# 2. Импорт настроек Django после установки переменной окружения
import django
django.setup()  # Критически важно для работы с моделями!

# 3. Создание экземпляра Celery
app = Celery('habit_tracker')

# 4. Конфигурация (префикс CELERY_ в settings.py)
app.config_from_object('django.conf:settings', namespace='CELERY')

# 5. Автоподгрузка задач из всех apps
def find_tasks():
    """Кастомный поиск задач во всех установленных приложениях"""
    installed_apps = apps.get_app_configs()
    return [app.name for app in installed_apps]

app.autodiscover_tasks(find_tasks())  # Автоподгрузка для всех apps

# 6. Тестовая задача для проверки
@app.task(bind=True)
def debug_task(self):
    """Задача для проверки работы Celery + Django"""
    from django.contrib.admin.apps import AdminConfig  # Проверка доступа к админке
    logger.info("Django admin available: %s", AdminConfig.name)
    return "Celery + Django works!"

# 7. Глобальный обработчик ошибок
@app.task(bind=True)
def on_failure(self, exc, task_id, args, kwargs, einfo):
    logger.error(f'Task FAILED: {task_id} | Error: {exc}')
    if 'admin' not in apps.all_models:
        logger.critical("Django admin app not loaded!")