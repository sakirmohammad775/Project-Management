from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm
from tasks.models import Employee

# Create your views here.


def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def create_task(request):
    employees=Employee.objects.all()
    form = TaskForm(employees=employees)
    context = {"form": form}
    return render(request, "task_form.html", context)
