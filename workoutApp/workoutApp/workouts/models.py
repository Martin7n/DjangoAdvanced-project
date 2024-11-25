from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.db.models import Max
from django.http import request
from django.utils import timezone

from workoutApp.common_utils.mixins import AutoIncrementOrder
from workoutApp.common_utils.validators import name_validator, date_today_validator
from workoutApp.common_utils.workout_choices import WorkoutType, ExrxCategory, ExrxType


# Create your models here.
class WorkoutBase(models.Model):

    workout_type = models.CharField(
        max_length=30,
        choices=WorkoutType.choices,
        )

    created_at = models.DateTimeField(
        auto_now_add=True,
        )

    updated_at = models.DateTimeField(
        auto_now=True
        )
    # exercise = models.ManyToManyField('Exercise', blank=True)

    class Meta:
        abstract = True


class Workout(WorkoutBase):
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='workouts'
        )

    workout_date = models.DateField(
        blank=True,
        null=True,
        default=timezone.now,
        validators=[date_today_validator],
        )

    def save(self, *args, **kwargs):
        if not self.user:
            self.user = request.user
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.workout_type}"

    def get_tot_volume(self):
        total = sum(xrx.reps * xrx.weight for xrx in self.sets.all())
        return total

    def get_exercises(self):
        # return  ", ".join([p.exercise.name for p in self.sets.all()])

        return [p.exercise.name for p in self.sets.all()]

    def get_all_sets_reps(self):
        listed = []
        for xrx in self.sets.all():

            listed.append(f"{xrx.order}{xrx.reps} - {xrx.weight}")
        return ", ".join(listed)

    def get_all(self):
        all_info = {}

        for xrx in self.sets.all():
            exercise = xrx.exercise.name
            info = f"{xrx.reps}x{xrx.weight:.0f}"

            if exercise not in all_info:
                all_info[exercise] = []
            all_info[exercise].append(info)

        return all_info


class WorkoutTemplate(WorkoutBase):
    name = models.CharField(max_length=100)
    description = models.TextField(
        blank=True,
        null=True,
        )
    # frequency_per_week = models.PositiveIntegerField(default=1)


class ExerciseCategory(models.Model):
    category = models.CharField(
        max_length=100,
        choices=ExrxCategory.choices,
        )

    def __str__(self):
        return self.category


class WorkoutSet(models.Model):
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='sets',
        )

    exercise = models.ForeignKey(
        'Exercise',
        on_delete=models.CASCADE,
        related_name='workout_sets',
        )

    reps = models.PositiveIntegerField(
                    validators=[MinValueValidator(1)],
                    default=0,
                    )

    weight = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(0)], default=0,
        )

    order = models.PositiveIntegerField(
        default=0,
        )

    # Ordering the sets of the exercises.
    def save(self, *args, **kwargs):
        if self.weight > 0 and self.reps > 0:
            if self.order == 0 or not self.order:

                max_order = WorkoutSet.objects.filter(
                    workout=self.workout,
                    exercise=self.exercise).aggregate(Max('order'))[
                    'order__max']
                self.order = (max_order or 0) + 1
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.exercise.name} - {self.reps} reps : {self.weight} kg"


class Exercise(models.Model):

    MIN_LEN_NAME = 3

    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(MIN_LEN_NAME), name_validator],
        null=True,
        blank=True,
        )

    category = models.CharField(
        max_length=100,
        choices=ExrxCategory.choices)

    type = models.CharField(
        max_length=100,
        choices=ExrxType.choices)

    # xrx_instructions = models.ForeignKey("ExrxInstructions", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# class WeeklySchedule(models.Model):
#     user = models.ForeignKey(
#         'users.CustomUser',
#         on_delete=models.CASCADE,
#         related_name='weekly_schedules',
#         )
#     week_start_date = models.DateField()
#     week_end_date = models.DateField()
#     notes = models.TextField(
#         blank=True,
#         null=True,
#         )
#
#
# class WeeklyWorkout(models.Model):
#     schedule = models.ForeignKey(WeeklySchedule, on_delete=models.CASCADE, related_name='weekly_workouts')
#     workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
#     day_of_week = models.CharField(max_length=9, choices=DayOfWeek.choices)
#     order = models.PositiveIntegerField(default=0)


# Todo
# class Repmax(models.Model):
#     user = models.ForeignKey(
#         'users.CustomUser',
#         on_delete=models.CASCADE,
#         related_name='rep_maxes',
#     )
#
#     exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='rep_maxes')
#     max_weight = models.DecimalField(
#         decimal_places=2,
#         max_digits=5,
#         )
#     reps = models.PositiveIntegerField()
#     calculated_rm = models.DecimalField(
#         decimal_places=2,
#         max_digits=5,
#         )
#
#     def save(self, *args, **kwargs):
#         if self.max_weight and self.reps is not None:
#             self.calculated_rm = self.max_weight * (1 + Decimal(0.0333) * self.reps)
#         super().save(*args, **kwargs)
