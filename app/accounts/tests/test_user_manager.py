"""
User manager test cases
"""
from datetime import date
from unittest import TestCase

from django.contrib.auth import get_user_model

from countries.tests.factories.country import CountryFactory

User = get_user_model()


class UserManagerTests(TestCase):
    """
    Test the custom user manager
    """

    def test_create_user(self) -> None:
        """
        Test creating a user
        Returns:
            None
        """
        expected_email = "test@gmail.com"

        user = User.objects.create_user(
            email=expected_email, password="testpass123", birth_date=date(1990, 1, 1), country=CountryFactory()
        )
        self.assertEqual(user.email, expected_email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="testpass123")

        user.delete()

    def test_create_superuser(self) -> None:
        """
        Test creating a superuser
        Returns:
            None
        """
        expected_email = "test@gmail.com"

        admin_user = User.objects.create_superuser(
            email=expected_email, password="testpass123", birth_date=date(1990, 1, 1), country=CountryFactory()
        )
        self.assertEqual(admin_user.email, expected_email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=expected_email, password="testpass123", is_superuser=False
            )

        admin_user.delete()
