from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import CustomUserCreationForm


# Create your views here.
def dashboard(request):
    return render(request, "users/dashboard.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
