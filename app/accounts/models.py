"""
Accounts models
"""
import datetime

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """
    Custom user model
    """

    class GenderTypes(models.TextChoices):
        """
        Ticker types
        """

        MALE = "Male", _("Male")
        FEMALE = "Female", _("Female")

    country = models.ForeignKey(
        "countries.Country", on_delete=models.CASCADE, null=False
    )
    email = models.EmailField(unique=True, max_length=255)
    birth_date = models.DateField()
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(
        choices=(("Male", "Male"), ("Female", "Female")), max_length=10
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email}"

    def get_age(self) -> int:
        """
        Get user age
        Returns:
            int: user age
        """
        return (datetime.date.today() - self.birth_date).days // 365

    def get_life_expectancy(self) -> int:
        """
        Get user life expectancy
        Returns:
            int: user life expectancy
        """
        assert self.gender
        return getattr(
            self.country.pension_system_information,
            f"{self.gender.lower()}_life_expectancy",
        )

    def get_pension_age(self) -> int:
        """
        Get user pension age
        Returns:
            int: user pension age
        """
        assert self.gender
        return getattr(
            self.country.pension_system_information,
            f"{self.gender.lower()}_pension_age",
        )


class PensionSystemInformation(models.Model):
    """
    Pension system information model
    """

    country = models.OneToOneField(
        "countries.Country",
        on_delete=models.PROTECT,
        related_name="pension_system_information",
    )
    male_life_expectancy = models.FloatField()
    female_life_expectancy = models.FloatField()
    male_pension_age = models.FloatField()
    female_pension_age = models.FloatField()
