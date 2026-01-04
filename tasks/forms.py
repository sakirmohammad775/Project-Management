
from django import forms
from tasks.models import Task

### Django Form
class TaskForm (forms.Form):
    title=forms.CharField(max_length=250 ,label='Task Tile')
    description=forms.CharField(widget=forms.Textarea,label='Task Description')
    due_date=forms.DateField(widget=forms.SelectDateWidget,label="Due Date")
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label="Assigned To")


    def __init__(self, *args, **kwargs):
        employees=kwargs.pop("employees",[])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices=[(emp.id,emp.name)for emp in employees]
        
"""Mixing to apply"""        
class styleFormMixin:
    default_classes="border border-gray-300 w-full p-3 rounded-lg shadow-sm focus:border-rose-500 focus:outline-none"
    
    def apply_styled_widgets(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter{field.label.lower()}",
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter{field.label.lower()}",
                    'rows':5
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                print('inside date')
                field.widget.attrs.update({
                    "class":"border border-gray-300 p-3 rounded-lg shadow-sm focus:border-rose-500 focus:outline-none"
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                print("inside checkbox")
                field.widget.attrs.update({
                    'class':"space-y-2"
                })
            
    
    
        
### DJANGO MODELFORM
class TaskModelForm(styleFormMixin,forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','description','due_date','assigned_to']
        widgets={
            'due_date':forms.SelectDateWidget,
            'assigned_to':forms.CheckboxSelectMultiple
        }
        """Manual widget"""
        # widgets={
        #     'title':forms.TextInput(attrs={
        #         'class':"border border-green-700 w-full rounded-lg shadow-sm focus:border-rose-300",
        #          'placeholder':"Enter the Title"
        #          }),
        #     'description':forms.TextInput(attrs={
        #         'class':"border-2 border-green-700 w-full rounded-lg shadow-sm focus:border-rose-300",
        #          'placeholder':"Enter the Details",
        #          "rows":5
        #     }),
        #     'due_date':forms.SelectDateWidget(attrs={
        #         'class':"border border-green-700 rounded-lg shadow-sm focus:border-rose-300",
        #          'placeholder':"Enter the due Date"}),
        #     'assigned_to':forms.CheckboxSelectMultiple(attrs={
        #         'class':"border border-green-700  rounded-lg shadow-sm focus:border-rose-300",
        #          'placeholder':"enter the details"
        #     })
        # }
        
    """Using mixins widget"""
    def __init__(self,*arg,**kwarg):
        super().__init__(*arg,**kwarg)
        self.apply_styled_widgets()