import os
from celery import Celery
import logging

# Настройка логгера для Celery
logger = logging.getLogger(__name__)

# Установка переменной окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')

# Создание экземпляра Celery
app = Celery('habit_tracker')

# Конфигурация из настроек Django (префикс CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в файлах tasks.py приложений
app.autodiscover_tasks()

# Тестовая задача для проверки работы Celery
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """
    Тестовая задача для отладки работы Celery.
    Логирует полученный контекст запроса.
    """
    try:
        logger.info(f'Celery task received: {self.request!r}')
        logger.debug('Debug task executed successfully')
        return "Debug task completed"
    except Exception as e:
        logger.error(f'Debug task failed: {e}')
        raise

# Глобальная настройка для всех задач
@app.task(bind=True)
def on_failure(self, exc, task_id, args, kwargs, einfo):
    """Обработчик ошибок для всех задач"""
    logger.error(f'Task {task_id} failed: {exc}')