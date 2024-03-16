from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser


UserAdmin.fieldsets += (
    (
        'Extra Fields',
        {'fields': ('bio', 'experience')}
    ),
)


admin.site.register(MyUser, UserAdmin)
