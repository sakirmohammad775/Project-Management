from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse ('welcome to the world')

def show_task(request):
    return HttpResponse("show all tasks")
