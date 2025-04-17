"""Views for Ride API"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Ride
from core.permissions import IsAdminUserRole
from .serializers import RideSerializer


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAdminUserRole]
