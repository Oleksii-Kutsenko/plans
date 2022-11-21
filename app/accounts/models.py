from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """
    Custom user model
    """

    country = models.ForeignKey("countries.Country", on_delete=models.CASCADE, null=False)
    email = models.EmailField(unique=True, max_length=255)
    birth_date = models.DateField()
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(choices=(("Male", "Male"), ("Female", "Female")), max_length=10)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email}"


class PensionSystemInformation(models.Model):
    """
    Pension system information model
    """

    country = models.ForeignKey("countries.Country", on_delete=models.PROTECT)
    male_pension_age = models.FloatField()
    female_pension_age = models.FloatField()
    male_life_expectancy = models.FloatField()
    female_life_expectancy = models.FloatField()
