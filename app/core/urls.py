from rest_framework.routers import DefaultRouter
from user.views import UserViewSet
from ride.views import RideViewSet, RideEventViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"rides", RideViewSet, basename="ride")
router.register(r"rideevents", RideEventViewSet, basename="rideevent")
urlpatterns = router.urls

urlpatterns = [
    path("", include(router.urls)),
]
