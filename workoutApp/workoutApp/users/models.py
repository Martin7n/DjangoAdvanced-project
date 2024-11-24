from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser
from django.db import models

from workoutApp.common_utils.validators import validate_filesize


#
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
            "unique": "Choose different e-mail, please.",}
    )

    # profile_picture = models.ImageField(
    #     upload_to="profiles/profile_picture",
    #     default='default_profile.jpg',
    #     validators=[
    #         validate_filesize,
    #     ],
    #     help_text="Upload your profile picture.."
    # )
    #
    # trainer = models.BooleanField(default=False)

#
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


