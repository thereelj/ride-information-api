"""Database models."""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Create, save and return a superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    ROLE_CHOICES = [("admin", "Admin"), ("other", "Other Users")]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="other")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Ride(models.Model):
    """Ride object"""

    RIDE_STATUS_CHOICES = [
        ("en-route", "En-route"),
        ("pickup", "Pick-up"),
        ("dropoff", "Drop-off"),
    ]

    status = models.CharField(
        max_length=255, choices=RIDE_STATUS_CHOICES, default="pickup"
    )
    id_rider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rider_user"
    )
    id_driver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="driver_user"
    )
    pickup_latitude = models.FloatField(blank=True, null=True)
    pickup_longitude = models.FloatField(blank=True, null=True)
    dropoff_latitude = models.FloatField(blank=True, null=True)
    dropoff_longitude = models.FloatField(blank=True, null=True)
    pickup_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} {self.pickup_time} {self.id_rider} {self.status}"


class RideEvent(models.Model):
    id_ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id_ride} {self.description} {self.created_at}"
