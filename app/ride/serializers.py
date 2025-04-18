"""Serializers for Ride API"""

from django.utils.timezone import now
from rest_framework import serializers

from core.models import Ride, RideEvent


class RideSerializer(serializers.ModelSerializer):
    """Ride object serializer"""

    distance = serializers.SerializerMethodField()
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            "id",
            "status",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
            "pickup_time",
            "id_rider",
            "id_driver",
            "distance",
            "todays_ride_events",
        ]

    def get_distance(self, obj):
        if hasattr(obj, "distance") and obj.distance is not None:
            return f"{round(obj.distance, 2)} km"
        return None

    def get_todays_ride_events(self, obj):
        today = now().date()
        events = RideEvent.objects.filter(id_ride=obj, created_at__date=today)
        return RideEventSerializer(events, many=True).data


class RideEventSerializer(serializers.ModelSerializer):
    """Ride event object serializer"""

    class Meta:
        model = RideEvent
        fields = "__all__"
