from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import CustomRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


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
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("Doc", username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("home")
    return render(request, "registration/login.html")


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
