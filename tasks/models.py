from django.db import models

# Create your models here.
class Employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    

class Task(models.Model):
    project=models.ForeignKey("Project",on_delete=models.CASCADE,default=1) # many to one
    
    assigned_to=models.ManyToManyField(Employee,related_name='tasks')
    title=models.CharField(max_length=250)
    description=models.TextField()
    due_date=models.DateField()
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class TaskDetail(models.Model):
    PRIORITY_OPTIONS=(
        ('H','High'),
        ('M','Medium'),
        ('L','Low')
    )
    assigned_to=models.CharField(max_length=100)
    priority=models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default="L")

class TaskDetail(models.Model):
    HIGH='H' 
    MEDIUM='M'
    LOW='L'
    
    PRIORITY_OPTIONS=(
        (HIGH,"High"),
        (MEDIUM,"Medium"),
        (LOW,"Low")
        
    )
    task=models.OneToOneField(Task,on_delete=models.CASCADE,related_name='details') #
    assigned_to=models.CharField(max_length=100)
    priority=models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default='L')
    
#Task.objects.get(id=2)
#select*from task where id=2
#ORM=

class Project(models.Model):
    name=models.CharField(max_length=100)
    start_date=models.DateField()