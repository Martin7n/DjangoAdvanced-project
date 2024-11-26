

from django.db import models
from django.db.models import Max

class ExerciseManager(models.Manager):

    def create_exercise(self, workout, **kwargs):
        max_order = self.filter(workout=workout).aggregate(Max('order'))['order__max']
        order = (max_order or 0) + 1
        exercise = self.model(workout=workout, order=order, **kwargs)
        exercise.save()
        return exercise