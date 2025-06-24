from django.apps import AppConfig

class HabitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'habits'
    verbose_name = 'Управление привычками'

    def ready(self):
        import habits.signals