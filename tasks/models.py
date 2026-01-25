from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100) #store employee name
    email = models.EmailField(unique=True) # store  unique email(no duplicate employees)

    def __str__(self):
        return self.name  #defines how object appears in admin shell


class Task(models.Model): #represents an individual task under a project
    STATUS_CHOICES = [      #choice restrict values and help  Ui Consistency
        ("PENDING", "pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "completed"),
    ]
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1) #Many to One  relationship ,many tasks belong to one project, delete tasks if project is deleted
    assigned_to = models.ManyToManyField(Employee, related_name="tasks") # M2M relationships ,
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #details
    
    def __str__(self):
        return self.title


class TaskDetail(models.Model):
    HIGH = "H"
    MEDIUM = "M"
    LOW = "L"
    PRIORITY_OPTIONS = ((HIGH, "High"), (MEDIUM, "Medium"), (LOW, "Low"))
    task = models.OneToOneField(Task, on_delete=models.DO_NOTHING, related_name="details")
    # assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default="L")
    notes=models.TextField(blank=True,null=True)
    
    def __str__(self):
        return f"Details form Task {self.task.title}"


# Represents a project under which multiple tasks can exist.
class Project(models.Model):
    name = models.CharField(max_length=100) #project name
    description=models.TextField(blank=True,null=True) # Optional project description # blank=True → form validation # null=True → database allows NULL
    start_date = models.DateField()


