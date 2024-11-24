from django.contrib import admin

from workoutApp.nutrition.models import Meal


# Register your models here.

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "calories",
        "date",
        "created_at",
        "type",
        "user",
    ]
    list_filter = ["user","type", "calories",]


