from django.urls import include, re_path

from . import views

urlpatterns = [
    re_path(r"^dashboard/", views.dashboard, name="dashboard"),
    re_path(r"^register/", views.register, name="register"),
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
]
