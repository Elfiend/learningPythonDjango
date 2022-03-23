from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordChangeView)
from django.urls import include, path, re_path

from . import views
from .views import ProfileView

urlpatterns = [
    path('', views.index, name='home'),
    path("dashboard/<int:pk>/", ProfileView.as_view(), name="dashboard"),
    re_path(r"^register/", views.register, name="register"),
    re_path('logout', views.logout, name="logout"),
    path('activate/<uidb64>/<token>/', views.activate_account,
         name='activate'),
    path('resend-verification-email',
         views.resend_verification_email,
         name='resend_email'),
    path('accounts/password_change/',
         PasswordChangeView.as_view(
             template_name=
             "login/templates/registration/password_change_form.html"),
         name='password_change'),
    path('accounts/password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name=
             "login/templates/registration/password_change_done.html"),
         name='password_change_done'),
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    re_path(r"^oauth/", include("social_django.urls")),
]
