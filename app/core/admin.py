"""Django admin customization"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ["id"]
    list_display = ["email", "first_name", "last_name", "phone_number", "role"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "role",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)


@admin.register(models.Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ["id_driver", "id_rider", "status", "pickup_time"]
    list_filter = ["status", "pickup_time"]
    search_fields = ["id_driver", "id_rider", "pickup_time"]
    ordering = ["-pickup_time"]
    date_hierarchy = "pickup_time"


@admin.register(models.RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    list_display = ["id_ride", "description"]
