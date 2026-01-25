from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import CustomRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from users.forms import loginForm


# jbh234OINa!@
# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # ✅ THIS LINE
            user.is_active = False
            user.save()

            messages.success(
                request, "A confirmation mail sent. Please check your email"
            )
            return redirect("sign-in")
    else:
        form = CustomRegistrationForm()

    return render(request, "registration/register.html", {"form": form})


def sign_in(request):
    form = loginForm()
    if request.method == "POST":
        form = loginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    return render(request, "registration/login.html", {"form": form})


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
