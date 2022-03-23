import unicodedata

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import LocalUser, Profile


class EmailField(forms.CharField):

    def to_python(self, value):
        return unicodedata.normalize("NFKC", super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "username",
        }


class LocalUserCreationForm(UserCreationForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    class Meta(UserCreationForm.Meta):
        model = LocalUser
        fields = ('email', )
        field_classes = {"email": EmailField}


class LocalUserChangeForm(UserChangeForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    class Meta(UserChangeForm.Meta):
        model = LocalUser
        fields = "__all__"
        field_classes = {"email": EmailField}


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('social_name', )
