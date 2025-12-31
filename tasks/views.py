from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm

# Create your views here.


def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def create_task(request):
    form = TaskForm()
    context = {"form": form}
    return render(request, "task_form.html",context)
