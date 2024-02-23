from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from petstagram.accounts.validators import validate_isalpha


class PetstagramUser(AbstractUser):
    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    email = models.EmailField(unique=True)
    first_name = models.CharField(
        max_length=30,
        validators=(MinLengthValidator(2), validate_isalpha),
        null=True,
        blank=True)

    last_name = models.CharField(
        max_length=30,
        validators=(MinLengthValidator(2), validate_isalpha),
        null=True,
        blank=True)

    profile_picture = models.URLField(null=True, blank=True)

    gender = models.CharField(
        max_length=11,
        choices=GENDERS,
        null=True,
        blank=True,
        default=DO_NOT_SHOW
    )

    def get_user_first_last_names(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name

    def get_user_name(self):
        result = self.get_user_first_last_names()
        if result:
            return result
        else:
            return self.username



