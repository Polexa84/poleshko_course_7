# settings_test.py
from .settings import *

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_STORE_EAGER_RESULT = True

# Отключаем signal-ы
DISABLE_SIGNALS = True