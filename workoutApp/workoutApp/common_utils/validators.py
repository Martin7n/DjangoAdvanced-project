

from django.core.exceptions import ValidationError
import re

from datetime import datetime


def name_validator(value):
    pass
    # if not value.isalnum():
    #     raise ValidationError("Invalid name")


def alphabet_validator(name):
    if not re.match(r'^[A-Za-z]+$', name):
        raise ValidationError("Your name must contain letters only!")


def date_today_validator(entry_date):
    if entry_date > datetime.today().date():
        raise ValidationError("Please use today or a past date.")


def validate_filesize(value):
    if value.size > 5 * 1024 * 1024:
        raise ValidationError('File size should not exceed 5MB')
