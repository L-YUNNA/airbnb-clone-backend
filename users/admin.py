from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ("Profile", 
         {"fields": ("username", 
                     "password", 
                     "name", 
                     "email", 
                     "is_host",),
          "classes": ("wide",),},),
        ("Permissions",
         {"fields": ("is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",),
          "classes": ("collapse",),},),
        ("Important dates",
         {"fields": ("last_login", "date_joined",),
          "classes": ("collapse",),},),
    )

    list_display = ("username", "email", "name",)