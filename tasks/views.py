from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm, TaskForm, TaskDetailModelForm
from tasks.models import Task, TaskDetail, Project
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.contrib.auth.decorators import (
    user_passes_test,
    login_required,
    permission_required,
)
from users.views import is_admin
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView,DetailView

def is_manager(user):
    return user.groups.filter(name="Manager").exists()


def is_employee(user):
    return user.groups.filter(name="Manager").exists()


# Create your views here.
user_passes_test(is_manager, login_url="no-permission")


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

    context = {"tasks": tasks, "counts": counts, "role": "manager"}
    return render(request, "dashboard/manager-dashboard.html", context)


@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


@login_required
@permission_required("tasks.add_task", login_url="no-permission")
def create_task(request):
    # employees=Employee.objects.all()
    task_form = TaskModelForm()  # For GET
    task_detail_form = TaskDetailModelForm(request.POST)

    if request.method == "POST":  # For POST
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():

            """For Model form data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Added Successfully")
            return redirect("create-task")

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


# variable for list of decorators
create_decorators = [
    login_required,
    permission_required("tasks.add_task", login_url="no-permission"),
]



class CreateTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
    """For creating task"""

    permission_required='tasks.add-task'
    login_url='sign-in'
    template_name = "task_form.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['task_form']=kwargs.get('task_form',TaskModelForm())
        context['task_detail_form']=TaskDetailModelForm()
        return context
  
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():

            """For Model form data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Added Successfully")
            context=self.get_context_data(
                task_form=task_form,task_detail_form=task_detail_form
            )
            return render(request,self.template_name,context) 


@login_required
@permission_required("tasks.change_task", login_url="no-permission")
def update_task(request, id):
    # employees=Employee.objects.all()
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)  # For GET

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)

    if request.method == "POST":  # For POST
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():

            """For Model form data"""
            task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect("update-task", id)

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


############ Class based Version ######## CBV-Update
@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("tasks.change_task", login_url="no-permission"), name="dispatch"
)
class UpdateTask(View):
    def get(self, request, id):
        task = Task.objects.get(id=id)
        task_form = TaskModelForm(instance=task)
        task_detail_form = TaskDetailModelForm(instance=task.details)
        return render(
            request,
            "task_form.html",
            {"task_form": task_form, "task_detail_form": task_detail_form},
        )

    def post(self, request, id):
        task = Task.objects.get(id=id)
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(
            request.POST, request.FILES, instance=task.details
        )

        if task_form.is_valid() and task_detail_form.is_valid():

            """For Model form data"""
            task_form.save()
            task_detail_form.save()
            messages.success(request, "Task Updated Successfully")
            return redirect("update-task", id=id)

        return render(
            request,
            "task_form.html",
            {"task_form": task_form, "task_detail_form": task_detail_form},
        )


@login_required
@permission_required("tasks.delete_task", login_url="no-permission")
def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task Deleted Successfully")
        return redirect("manager-dashboard")
    else:
        messages.error(request, "something went wrong")
        return redirect("manager-dashboard")


@login_required
@permission_required("tasks.view_task", login_url="no-permission")
def view_task(request):
    projects = Project.objects.annotate(num_task=Count("task")).order_by("num_task")
    return render(request, "show_task.html", {"projects": projects})

############CVB view project######
view_project_decorators = [
    login_required,
    permission_required("projects.view_project", login_url="no-permission"),
]
@method_decorator(view_project_decorators,name='dispatch')
class ViewProject(ListView):
    model=Project
    context_object_name='projects'
    template_name='show_task.html'

    def get_queryset(self):
        queryset=Project.objects.annotate(
            num_task=Count('task')
        ).order_by('num_task')
        return queryset

@login_required
@permission_required("tasks.view_task", login_url="no-permission")
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choice = Task.STATUS_CHOICES

    if request.method == "POST":
        selected_status = request.POST.get("task_status")
        task.status = selected_status
        task.save()
        return redirect("task-details", task.id)
    return render(
        request, "task_details.html", {"task": task, "status_choices": status_choice}
    )


class TaskDetail(DetailView):
    model=Task
    template_name='task_details.html'
    context_object_name='task'
    pk_url_kwarg='task_id'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['status_choices']=Task.STATUS_CHOICES
        return context
    
    def post(self,request,*args,**kwargs):
        task=self.get_object()
        selected_status=request.POST.get('task_status')
        task.status=selected_status
        task.save()
        return redirect('task-details',task.id)
    
@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect("manager-dashboard")
    elif is_employee(request.user):
        return redirect("user-dashboard")
    elif is_admin(request.user):
        return redirect("admin-dashboard")
    return redirect("no-permission")
 