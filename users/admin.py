from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    fields = ("email", "phone_number", "city")
    search_fields = ("email", "city")
    ordering = ("email",)
