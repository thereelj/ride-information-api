"""Serializers for Ride API"""

from rest_framework import serializers

from core.models import Ride


class RideSerializer(serializers.ModelSerializer):
    """Ride object serializer"""

    class Meta:
        model = Ride
        fields = "__all__"
