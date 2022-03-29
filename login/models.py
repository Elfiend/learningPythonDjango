from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                        BaseUserManager)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class LocalUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class LocalUser(AbstractUser):
    username = models.CharField(_("username"), max_length=150, blank=True)
    email = models.EmailField(
        _("email address"),
        max_length=255,
        unique=True,
    )
    email_confirmed = models.BooleanField(default=True)
    is_social_auth = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = LocalUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    social_name = models.CharField(_("name"), max_length=150, blank=True)


@receiver(post_save, sender=LocalUser)
def update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


def create_profile(backend, user, response, *args, **kwargs):
    profile = user.profile
    if profile is None:
        profile = Profile(user_id=user.id)
    if not profile.social_name:
        profile.social_name = kwargs.get('details').get('fullname')
        profile.save()
