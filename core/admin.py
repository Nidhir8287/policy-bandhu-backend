"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ["email", ]
    list_display = ["email", "id", "name"]
    fieldsets = (
        (
            None,
            {'fields': ('name', 'email', 'password', 'phone',
                        'is_seminar', 'is_subscriber')},
        ),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', )},
        ),
        (
            _('Important Dates'),
            {'fields': ('last_login', )},
        )
    )
    readonly_fields = ['last_login', ]
    add_fieldsets = (
        (
            None,
            {'fields': (
                'name',
                'email',
                'password1',
                'password2',
                'phone',
                'is_seminar',
                'is_subscriber',
                'is_active',
                'is_staff',
                'is_superuser',
            )}
        ),
    )


admin.site.register(models.User, UserAdmin)