from django.db import models

# Create your models here.

class Task(models.Model):
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
