from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from workoutApp.common_utils.validators import validate_filesize
from workoutApp.workouts.models import Exercise
from decimal import Decimal


# User = get_user_model()
class CustomUser(AbstractUser):

    first_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Enter your first name (not required).."
    )

    last_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Enter your last name (not required).."
    )

    email = models.EmailField(
        max_length=30,
        unique=True,
        error_messages={
            "unique": "Choose different e-mail, please.", }
    )

    class Meta:
        permissions = [
            ('can_view_management_profile', 'Can view Management profile'),
        ]


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(
        upload_to="profiles/profile_picture",
        default='default_profile.jpg',
        validators=[
            validate_filesize,
        ],
        help_text="Upload your profile picture..",
        null=True,
    )

    trainer = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)


class RepMax(models.Model):
    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='rep_maxes'
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name='rep_maxes'
    )

    max_weight = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        # validators=[MinValueValidator(0)],
    )

    reps = models.PositiveIntegerField(
        # validators=[MinValueValidator(1)]
    )

    calculated_rm = models.DecimalField(
        decimal_places=2,
        max_digits=5
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        print("Save of RM")
        if self.max_weight and self.reps:
            self.calculated_rm = self.max_weight * (1 + Decimal(0.0333) * self.reps)
            print(f"{self.user.username}'s RepMax for {self.exercise.name}: {self.calculated_rm} kg")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s RepMax for {self.exercise.name}: {self.calculated_rm} kg"
