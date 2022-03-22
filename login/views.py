import json
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import LocalUserCreationForm
from .models import LocalUser


def index(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, 'users/index.html')

    if user.email_confirmed is not True:
        return render(request, 'users/email_verification.html')

    return redirect(dashboard)


@login_required()
def dashboard(request):
    return render(request, "users/dashboard.html")


def register(request):
    if request.method == "POST":
        form = LocalUserCreationForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.username = user.email
            user.email_confirmed = False
            user.is_social_auth = False
            user.save()
            # Send email
            _send_verification_email(request, user)

            login(request, user)
            return redirect(reverse("home"))
    else:
        form = LocalUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def resend_verification_email(request):
    user = request.user
    _send_verification_email(request, user)
    return redirect(reverse("home"))


def activate_account(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = LocalUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, LocalUser.DoesNotExist):
        user = None

    if user is not None and PasswordResetTokenGenerator().check_token(
            user, token):
        user.backend = "django.contrib.auth.backends.ModelBackend"
        user.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, ('Your account have been confirmed.'))
        return redirect(reverse("home"))

    messages.warning(request, (
        'The confirmation link was invalid, possibly because it has already been used.'
    ))
    return redirect(reverse("home"))


def logout(request):
    user = request.user
    if user.is_social_auth is True:
        return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
        logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    else:
        logout_url = reverse("home")

    log_out(request)
    return HttpResponseRedirect(logout_url)


def _send_verification_email(request, user):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string(
        'users/email/account_activation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': PasswordResetTokenGenerator().make_token(user),
        })
    user.email_user(subject, message)

    messages.success(request,
                     ('Please Confirm your email to complete registration.'))
