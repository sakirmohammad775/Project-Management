from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskModelForm,TaskForm
from tasks.models import Employee,Task

# Create your views here.


def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def create_task(request):
    #employees=Employee.objects.all()
    form = TaskModelForm() #for GET
    
    if request.method=="POST":  #for POST 
        form=TaskModelForm(request.POST)
        if form.is_valid():
            """For Model form data"""
            form.save()
            return render(request,'task_form.html',{"form":form,"message":"task added successfully"})
            '''Django form data'''
            # data=form.cleaned_data
            # title=data.get('title')
            # description=data.get('description')
            # due_date=data.get('due_date')
            # assigned_to=data.get('assigned_to')
            
            # task=Task.objects.create(title=title,description=description,due_date=due_date)
            # #assign employee to tasks
            # for emp_id in assigned_to:
            #     employee=Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
                
            return HttpResponse("Task added successfully")
        
    context = {"form": form}
    return render(request, "task_form.html", context)
