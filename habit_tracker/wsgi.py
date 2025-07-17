import os
import django
from django.core.wsgi import get_wsgi_application
from django.apps import apps
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')

# Принудительная регистрация всех приложений
def force_app_registration():
    # Сброс состояния приложений
    apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
    apps.app_configs = {}
    
    # Явная регистрация основных приложений Django
    from django.contrib.admin.apps import AdminConfig
    from django.contrib.auth.apps import AuthConfig
    from django.contrib.contenttypes.apps import ContentTypesConfig
    from django.contrib.sessions.apps import SessionsConfig
    
    CORE_APPS = {
        'admin': AdminConfig('admin', 'django.contrib.admin'),
        'auth': AuthConfig('auth', 'django.contrib.auth'),
        'contenttypes': ContentTypesConfig('contenttypes', 'django.contrib.contenttypes'),
        'sessions': SessionsConfig('sessions', 'django.contrib.sessions'),
    }
    
    for app_name, config in CORE_APPS.items():
        apps.app_configs[app_name] = config
    
    apps.populate(settings.INSTALLED_APPS)

# Вызов принудительной инициализации
try:
    force_app_registration()
except Exception as e:
    print(f"Force registration failed: {e}")

application = get_wsgi_application()