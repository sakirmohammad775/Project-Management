from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm, TaskForm, TaskDetailModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages


# Create your views here.
def manager_dashboard(request):
    type = request.GET.get("type", "all")  # dynamic query,Urls,Url tag

    counts = Task.objects.aggregate(
        total=Count("id"),
        completed=Count("id", filter=Q(status="COMPLETED")),
        in_progress=Count("id", filter=Q(status="IN_PROGRESS")),
        pending=Count("id", filter=Q(status="PENDING")),
    )

    base_query = (
        Task.objects.select_related("details").prefetch_related("assigned_to").all()
    )
    if type == "completed":
        tasks = base_query.filter(status="COMPLETED")
    elif type == "in-progress":
        tasks = base_query.filter(status="IN_PROGRESS")
    elif type == "pending":
        tasks = base_query.filter(status="PENDING")
    elif type == "all":
        tasks = base_query.all()

    context = {"tasks": tasks, "counts": counts}
    return render(request, "dashboard/manager-dashboard.html", context)


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def create_task(request):
    # employees=Employee.objects.all()
    task_form = TaskModelForm()  # For GET
    task_detail_form = TaskDetailModelForm(request.POST)

    if request.method == "POST":  # For POST
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)

        if task_form.is_valid() and task_detail_form.is_valid():

            """For Model form data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request,"Task Added Successfully")
            return redirect('create-task')

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


def view_task(request):
    projects = Project.objects.annotate(num_task=Count("task")).order_by("num_task")
    return render(request, "show_task.html", {"projects": projects})
