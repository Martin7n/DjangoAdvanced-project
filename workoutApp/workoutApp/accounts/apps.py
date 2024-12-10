from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workoutApp.accounts'

    def ready(self):
        import workoutApp.accounts.signals


