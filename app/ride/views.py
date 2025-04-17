"""Views for Ride API"""

from rest_framework import viewsets
from core.models import Ride, RideEvent
from core.permissions import IsAdminUserRole
from .serializers import RideSerializer, RideEventSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAdminUserRole]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['id_rider__email']


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUserRole]
