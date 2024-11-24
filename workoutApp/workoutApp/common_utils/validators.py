

from django.core.exceptions import ValidationError
import re

from datetime import datetime


def name_validator(value):
    '''Letters, numbers, and etc. are allowed'''
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



# TODO
# @deconstructible
# class FileSizeValidator:
#     def __init__(self, file_size_mb: int, message=None):
#         self.file_size_mb = file_size_mb
#         self.message = message
#
#     @property
#     def message(self):
#         return self.__message
#
#     @message.setter
#     def message(self, value):
#         if value is None:
#             self.__message = f"File size must be below or equal to {self.file_size_mb}MB"
#         else:
#             self.__message = value
#
#     def __call__(self, value):
#         if value.size > self.file_size_mb * 1024 * 1024:
#             raise ValidationError(self.message)