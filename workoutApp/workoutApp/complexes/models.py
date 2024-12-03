from django.db import models

from workoutApp.common_utils.workout_choices import ComplexType, Load
from workoutApp.workouts.models import Exercise
import random


class Complex(models.Model):
    name = models.CharField(max_length=30)
    exercises = models.ManyToManyField(Exercise, related_name='complexes')
    type = models.CharField(max_length=30, choices=ComplexType.choices)
    loading = models.CharField(max_length=30, choices=Load.choices)


