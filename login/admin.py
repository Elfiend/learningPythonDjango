from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import LocalUserChangeForm, LocalUserCreationForm
from .models import LocalUser


class LocalUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = LocalUserChangeForm
    add_form = LocalUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'email_confirmed', 'is_staff')
    list_filter = ('is_staff', )
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': ('email_confirmed', )
        }),
        ('Permissions', {
            'fields': ('is_staff', )
        }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('email', 'email_confirmed', 'password1', 'password2'),
    }), )
    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()


admin.site.register(LocalUser, LocalUserAdmin)
admin.site.unregister(Group)
