from django.apps import AppConfig


class WorkoutsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workoutApp.workouts'

    def ready(self):
        import workoutApp.workouts.signals
