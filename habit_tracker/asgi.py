import os
import django
from django.core.asgi import get_asgi_application
from django.apps import apps
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')

def ensure_admin_registered():
    """Принудительная регистрация админки и основных приложений"""
    if not apps.ready:
        # Явная регистрация core apps
        from django.contrib.admin.apps import AdminConfig
        from django.contrib.auth.apps import AuthConfig
        from django.contrib.contenttypes.apps import ContentTypesConfig
        
        core_apps = {
            'admin': AdminConfig('admin', 'django.contrib.admin'),
            'auth': AuthConfig('auth', 'django.contrib.auth'),
            'contenttypes': ContentTypesConfig('contenttypes', 'django.contrib.contenttypes'),
        }
        
        for app_name, config in core_apps.items():
            if app_name not in apps.app_configs:
                apps.app_configs[app_name] = config
        
        apps.populate(settings.INSTALLED_APPS)

try:
    ensure_admin_registered()
except Exception as e:
    print(f"Admin registration warning: {str(e)}")

application = get_asgi_application()