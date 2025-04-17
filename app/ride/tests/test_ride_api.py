"""Test for Ride API"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ride

from ride.serializers import RideSerializer

RIDE_URL = reverse("ride-list")


def create_ride(rider, driver, **params):
    """Create and return a sample ride."""
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
    payload.update(params)

    ride = Ride.objects.create(**payload)

    return ride


class AdminRideAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_user(
            email="adminusertest@email.com", password="Test@1234", role="admin"
        )

        self.user = get_user_model().objects.create_user(
            email="usertest@email.com", password="Test@1234", role="other"
        )

        rider1 = get_user_model().objects.create_user(
            "ridertest@email.com", "Test@1234"
        )
        driver1 = get_user_model().objects.create_user(
            "drivertest@email.com", "Test@1234"
        )

        rider2 = get_user_model().objects.create_user(
            "ridertest2@email.com", "Test@1234"
        )
        driver2 = get_user_model().objects.create_user(
            "drivertest2@email.com", "Test@1234"
        )

        create_ride(rider=rider1, driver=driver1)
        create_ride(rider=rider2, driver=driver2)

    def test_admin_can_access_ride_list(self):
        """Test admin calling ride API"""
        self.client.login(email="adminusertest@email.com", password="Test@1234")
        res = self.client.get(RIDE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()), 2)

    def test_non_admin_cannot_access_ride_list(self):
        self.client.login(email="usertest@email.com", password="Test@1234")
        res = self.client.get(RIDE_URL)
        self.assertIn(
            res.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
        )
