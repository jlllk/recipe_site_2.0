from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name')
        }),
        ('Роль на сайте', {'fields': ('role', 'is_superuser')}),
    )

    search_fields = ('email', 'username')
    ordering = ('username',)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
