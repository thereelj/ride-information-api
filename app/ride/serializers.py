"""Serializers for Ride API"""

from rest_framework import serializers

from core.models import Ride, RideEvent


class RideSerializer(serializers.ModelSerializer):
    """Ride object serializer"""

    distance = serializers.SerializerMethodField()

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
        ]

    def get_distance(self, obj):
        if hasattr(obj, "distance") and obj.distance is not None:
            return f"{round(obj.distance, 2)} km"
        return None


class RideEventSerializer(serializers.ModelSerializer):
    """Ride event object serializer"""

    class Meta:
        model = RideEvent
        fields = "__all__"
