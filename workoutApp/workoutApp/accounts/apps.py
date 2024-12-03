from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workoutApp.accounts'  # Ensure this is correct

    def ready(self):
        import workoutApp.accounts.signals


# class UsersConfig(AppConfig):
#     name = 'workoutApp.accounts'
#     verbose_name = "Users"
