from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import UserService
from mailing.models import MailingAttempt

@admin.register(UserService)
class CustomUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личная информация", {"fields": ("first_name", "last_name", "avatar", "phone", "country")}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password", "is_staff", "is_active"),
            },
        ),
    )
    filter_horizontal = ("groups", "user_permissions",)

admin.site.register(MailingAttempt)
