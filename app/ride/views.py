"""Views for Ride API"""

from django.db.models import F
from django.db.models.functions import ACos, Cos, Sin, Radians
from rest_framework import filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import viewsets
from core.models import Ride, RideEvent
from core.permissions import IsAdminUserRole
from .serializers import RideSerializer, RideEventSerializer


class RideFilter(filters.FilterSet):
    """Custom filter for Ride model"""

    status = filters.ChoiceFilter(choices=Ride.RIDE_STATUS_CHOICES)
    rider_email = filters.CharFilter(field_name="id_rider__email", lookup_expr="iexact")

    class Meta:
        model = Ride
        fields = ["status", "id_rider__email"]


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAdminUserRole]
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = RideFilter  # Specify the custom filter class
    ordering_fields = ["pickup_time", "distance"]
    ordering = ["pickup_time"]  # default ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("lng")
        ordering = self.request.query_params.get("ordering", "")

        # Distance sorting (Haversine formula)
        if "distance" in ordering and lat and lng:
            try:
                lat = float(lat)
                lng = float(lng)

                queryset = queryset.annotate(
                    distance=6371
                    * ACos(
                        Cos(Radians(lat))
                        * Cos(Radians(F("pickup_latitude")))
                        * Cos(Radians(F("pickup_longitude")) - Radians(lng))
                        + Sin(Radians(lat)) * Sin(Radians(F("pickup_latitude")))
                    )
                )
            except (ValueError, TypeError):
                pass  # Handle invalid lat/lng input gracefully

        return queryset


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUserRole]
