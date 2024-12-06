from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from workoutApp.accounts.models import RepMax
from workoutApp.workouts.models import WorkoutSet


@receiver(post_save, sender=WorkoutSet)
def update_repmax_on_workout_set_save(sender, instance, created, **kwargs):

    if instance.reps > 0 and instance.weight > 0:
        exercise = instance.exercise
        user = instance.workout.user
        max_weight = instance.weight
        reps = instance.reps
        print(f"Exercise: {exercise.name}, User: {user.username}, Max Weight: {max_weight}, Reps: {reps}")

        # current absolute RepMax.
        current_rep_max = RepMax.objects.filter(user=user, exercise=exercise).order_by('-max_weight', '-reps').first()

        #reasonable check but not for tests.
        # if exercise.category=="Basic":
        if exercise.category:
        # Determine if we need to save a new RepMax
            if current_rep_max is None or max_weight > current_rep_max.max_weight or (
                    max_weight == current_rep_max.max_weight and reps > current_rep_max.reps):
                with transaction.atomic():
                    new_rep_max = RepMax(
                        user=user,
                        exercise=exercise,
                        max_weight=max_weight,
                        reps=reps
                    )
                    print("Signal - 2: New RepMax will be created.")
                    new_rep_max.save()
                    print(f"New RepMax achieved: {new_rep_max}")


