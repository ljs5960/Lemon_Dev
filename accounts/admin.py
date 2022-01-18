from django.contrib import admin
from accounts.models import user


@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'uid',
        'email',
        'phonenumber',
    )