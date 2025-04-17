"""Test for models"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """test creating a user with an email is successful"""
        email = "test@email.com"
        password = "testpass@123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ["test1@EMAIL.com", "test1@email.com"],
            ["Test2@Email.com", "Test2@email.com"],
            ["TEST3@EMAIL.COM", "TEST3@email.com"],
            ["test4@email.COM", "test4@email.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "testpass@123")

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            'test@123'
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
