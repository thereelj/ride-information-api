"""Serializers for Ride API"""

from rest_framework import serializers

from core.models import Ride, RideEvent


class RideSerializer(serializers.ModelSerializer):
    """Ride object serializer"""

    class Meta:
        model = Ride
        fields = "__all__"


class RideEventSerializer(serializers.ModelSerializer):
    """Ride event object serializer"""
    
    class Meta:
        model = RideEvent
        fields = "__all__"