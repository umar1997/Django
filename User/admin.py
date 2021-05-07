from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.db import models

from User.models import Person

class UserAdminConfig(UserAdmin):
    model = Person
    search_fields = ('email', 'username',)
    list_filter = ('is_staff', 'is_active')
    ordering = ('-created_at',)
    list_display = ('id', 'email', 'username', 'phone_number', 'is_staff', 'created_at', 'last_login')
    fieldsets = (
        (None, {'fields': ('email', 'username','phone_number',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )


def has_superuser_permission(request):
    return request.user.is_superuser

admin.site.has_permission = has_superuser_permission

admin.site.register(Person, UserAdminConfig)