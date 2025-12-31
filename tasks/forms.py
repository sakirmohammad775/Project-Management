from django import forms

class TaskForm (forms.Form):
    title=forms.CharField(max_length=250 ,label='Task Tile')
    description=forms.CharField(widget=forms.Textarea,label='Task Description')
    
