from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','password1','password2','email']
        
    def __init__(self, *args, **kwargs):
        super(UserCreationForm,self).__init__(*args, **kwargs)
        
        for fieldname in ['username','password1','password2']:
            self.fields[fieldname].help_text=None

class CustomRegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField()
    
    class Meta:
        model=User 
        fields=['username','first_name','last_name','password','confirm_password','email']

        def clean_password1(self):
            
            