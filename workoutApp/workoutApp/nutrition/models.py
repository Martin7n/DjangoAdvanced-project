from django.db import models

from workoutApp.common_utils.validators import date_today_validator
from workoutApp.common_utils.workout_choices import MealChoice
from django.utils import timezone

# Create your models here.


class Meal(models.Model):
    description = models.TextField(max_length=600)

    calories = models.IntegerField(default=0)

    date = models.DateField(
        blank=True,
        null=True,
        default=timezone.now,
        validators=[date_today_validator],
    )

    created_at = models.DateField(auto_now_add=True)

    type = models.CharField(
        max_length=50,
        choices=MealChoice.choices,
    )
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='meals',
    )

    def save(self, *args, **kwargs):
        if not self.user:
            self.user = request.user
        super().save(*args, **kwargs)
