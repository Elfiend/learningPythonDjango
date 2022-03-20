from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .local.accounts import LocalUser

admin.site.register(LocalUser, UserAdmin)

# unregister the Group model from admin.
admin.site.unregister(Group)
