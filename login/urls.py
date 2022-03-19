from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('resend-verification-email',views.resend_verification_email),
    path('reset-password', views.reset_password),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
]