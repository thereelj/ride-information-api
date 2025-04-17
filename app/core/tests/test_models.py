"""Test for models"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Ride, RideEvent


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
        user = get_user_model().objects.create_superuser("test@email.com", "test@123")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_ride(self):
        """Test creating a ride object"""
        rider = get_user_model().objects.create_user("ridertest@email.com", "Test@1234")
        driver = get_user_model().objects.create_user(
            "driverrtest@email.com", "Test@1234"
        )

        payload = {
            "status": "en-route",
            "id_rider": rider,
            "id_driver": driver,
            "pickup_latitude": 40.7128,
            "pickup_longitude": -74.0060,
            "dropoff_latitude": 14.5995,
            "dropoff_longitude": 120.9842,
            "pickup_time": "2025-04-17T14:30:00",
        }
        ride = Ride.objects.create(**payload)

        self.assertEqual(ride.status, payload["status"])
        self.assertEqual(rider, payload["id_rider"])
        self.assertEqual(driver, payload["id_driver"])

    def test_create_ride_event(self):
        rider = get_user_model().objects.create_user("ridertest@email.com", "Test@1234")
        driver = get_user_model().objects.create_user(
            "driverrtest@email.com", "Test@1234"
        )

        ride_payload = {
            "status": "en-route",
            "id_rider": rider,
            "id_driver": driver,
            "pickup_latitude": 40.7128,
            "pickup_longitude": -74.0060,
            "dropoff_latitude": 14.5995,
            "dropoff_longitude": 120.9842,
            "pickup_time": "2025-04-17T14:30:00",
        }
        ride = Ride.objects.create(**ride_payload)

        ride_event_payload = {
            "id_ride": ride,
            "description": "Sample description of a ride event",
            "created_at": "2025-04-17T14:30:00",
        }

        ride_event = RideEvent.objects.create(**ride_event_payload)
        self.assertEqual(ride_event.description, ride_event_payload["description"])
        self.assertEqual(ride_event.id_ride, ride_event_payload["id_ride"])
