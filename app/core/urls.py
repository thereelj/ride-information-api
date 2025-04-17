from rest_framework.routers import DefaultRouter
from user.views import UserViewSet
from ride.views import RideViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"rides", RideViewSet, basename="ride")
urlpatterns = router.urls

urlpatterns = [
    path("", include(router.urls)),
]
