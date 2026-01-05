from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskModelForm, TaskForm
from tasks.models import Employee, Task,TaskDetail,Project
from django.db.models import Q,Count,Max,Min,Avg
# Create your views here.


def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def create_task(request):
    # employees=Employee.objects.all()
    form = TaskModelForm()  # for GET

    if request.method == "POST":  # for POST
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """For Model form data"""
            form.save()
            return render(
                request,
                "task_form.html",
                {"form": form, "message": "task added successfully"},
            )

    context = {"form": form}
    return render(request, "task_form.html", context)


def view_task(request):
    projects=Project.objects.annotate (num_task=Count('task')).order_by("num_task")
    return render(request, "show_task.html", {"projects": projects})
