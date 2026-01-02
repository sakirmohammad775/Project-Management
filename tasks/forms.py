from django import forms

class TaskForm (forms.Form):
    title=forms.CharField(max_length=250 ,label='Task Tile')
    description=forms.CharField(widget=forms.Textarea,label='Task Description')
    due_date=forms.DateField(widget=forms.SelectDateWidget,label="Due Date")
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label="Assigned To")


    def __init__(self, *args, **kwargs):
        employees=kwargs.pop("employees",[])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices=[(emp.id,emp.name)for emp in employees]
        