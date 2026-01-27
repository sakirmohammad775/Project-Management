from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from users.forms import CustomRegistrationForm, AssignRoleForm,CreateGroupForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from users.forms import loginForm
from django.contrib.auth.tokens import default_token_generator


# jbh234OINa!@
# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
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


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("sign-in")
        else:
            return HttpResponse("Invalid Id or token")
    except User.DoesNotExist:
        return HttpResponse("User not found")


"""
    Admin
        - All over access
    Manager
        - project
        -Task create
    Employee
        -task read 
        - task update
"""


def admin_dashboard(request):
    users = User.objects.all()
    return render(request, "admin/dashboard.html", {"users": users})


def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form=AssignRoleForm()

    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get("role")
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,f"User {user.username} has been assigned to the {role.name} role")
            return redirect ('admin-dashboard')
    return render(request,'admin/assign_role.html',{"form":form})


def create_group(request):
    form=CreateGroupForm()
    if request.method=='POST':
        form=CreateGroupForm(request.POST)
        
        if form.is_valid():
            group=form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('create-group')
    return render(request,'admin/create_group.html',{'form':form})


def group_list(request):
    groups=Group.objects.all()
    return render(request,'admin/group_list.html',{'groups':groups})