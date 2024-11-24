import os
import random

import django
from django.utils import timezone
from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workoutApp.settings")
django.setup()

from django.contrib.auth import get_user_model

from workoutApp.common_utils.workout_choices import ExrxCategory, ExrxType, WorkoutType
from workoutApp.users.models import UserProfile
from workoutApp.workouts.models import Exercise, Workout, WorkoutSet


def create_superuser():
    User = get_user_model()

    username = 'admin'
    password = 'admin'

    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username=username, password=password)
        # Create a UserProfile for the superuser
        UserProfile.objects.create(user=user)
        print(f"Superuser '{username}' and UserProfile created successfully.")
    else:
        print(f"Superuser '{username}' already exists.")


def create_exercises():
    exercises_data = [
        {"name": "Squat", "category": ExrxCategory.BASIC, "type": ExrxType.LOWER},
        {"name": "Deadlift", "category": ExrxCategory.BASIC, "type": ExrxType.LOWER},
        {"name": "Front Squat", "category": ExrxCategory.AUXILIARY, "type": ExrxType.LOWER},
        {"name": "KB Swing", "category": ExrxCategory.ASSISTANCE, "type": ExrxType.LOWER},
        {"name": "Goblet Squat", "category": ExrxCategory.ASSISTANCE, "type": ExrxType.LOWER},
        {"name": "Lunges", "category": ExrxCategory.AUXILIARY, "type": ExrxType.LOWER},
        {"name": "Bulgarian squat", "category": ExrxCategory.AUXILIARY, "type": ExrxType.LOWER},

        {"name": "Pull up", "category": ExrxCategory.AUXILIARY, "type": ExrxType.PULL},
        {"name": "Weighted Pull up", "category": ExrxCategory.BASIC, "type": ExrxType.PULL},
        {"name": "Row", "category": ExrxCategory.BASIC, "type": ExrxType.PULL},
        {"name": "Power Clean", "category": ExrxCategory.BASIC, "type": ExrxType.PULL},
        {"name": "Curl", "category": ExrxCategory.AUXILIARY, "type": ExrxType.PULL},
        {"name": "DB row", "category": ExrxCategory.ASSISTANCE, "type": ExrxType.PULL},
        {"name": "Australian Row", "category": ExrxCategory.ASSISTANCE, "type": ExrxType.PULL},

        {"name": "Press", "category": ExrxCategory.BASIC, "type": ExrxType.PUSH},
        {"name": "Dip", "category": ExrxCategory.ASSISTANCE, "type": ExrxType.PUSH},
        {"name": "Bench", "category": ExrxCategory.BASIC, "type": ExrxType.PUSH},
        {"name": "Push up", "category": ExrxCategory.AUXILIARY, "type": ExrxType.PUSH},
        {"name": "Incline Bench", "category": ExrxCategory.AUXILIARY, "type": ExrxType.PUSH},
        {"name": "French Press", "category": ExrxCategory.ASSISTANCE, "type": ExrxType.PUSH},
        {"name": "Weighted Dips", "category": ExrxCategory.AUXILIARY, "type": ExrxType.PUSH},

    ]

    for exercise_data in exercises_data:
        exercise, created = Exercise.objects.get_or_create(
            name=exercise_data["name"],
            defaults={
                "category": exercise_data["category"],
                "type": exercise_data["type"]
            }
        )

        if created:
            print(f"Exercise '{exercise.name}' created successfully.")
        else:
            print(f"Exercise '{exercise.name}' already exists.")


def create_workout():
    User = get_user_model()
    user = User.objects.get(username='admin')

    for workout_type, _ in WorkoutType.choices:
        workout = Workout.objects.create(workout_type=workout_type, user=user, workout_date=timezone.now())
        exercises = Exercise.objects.all().order_by('?')[:random.randint(3, 5)]


        for exercise in exercises:

            num_sets = random.randint(2, 5)

            for _ in range(num_sets):
                reps = random.randint(3, 10)
                weight = random.randint(50, 120)

                WorkoutSet.objects.create(
                    workout=workout,
                    exercise=exercise,
                    reps=reps,
                    weight=weight,
                )

        print(f"Workout '{workout_type}' created with {len(exercises)} exercises")



def main():
    create_superuser()
    create_exercises()
    create_workout()
    print("Initial data setup complete.")


if __name__ == "__main__":
    main()
