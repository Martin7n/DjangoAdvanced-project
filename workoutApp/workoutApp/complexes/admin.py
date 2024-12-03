from django.contrib import admin

from workoutApp.complexes.models import Complex


@admin.register(Complex)
class ComplexesAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "loading",
        'get_exercises',
    ]

    def get_exercises(self, obj):
        exercises = obj.exercises.all()

        return ", ".join([exercise.name for exercise in exercises])
