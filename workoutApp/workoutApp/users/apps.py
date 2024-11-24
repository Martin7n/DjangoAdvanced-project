from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workoutApp.users'  # Ensure this is correct

    def ready(self):
        import workoutApp.users.signals


# class UsersConfig(AppConfig):
#     name = 'workoutApp.users'
#     verbose_name = "Users"
