from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView


class RegisterForm(UserCreationForm):
    email = forms.EmailField() #adding email field
    CHOICES = [('student', 'Student'),
               ('company', 'Company')]
    user_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    
    class Meta:
        model = User
        fields = ["username","email","user_type", "password1","password2",] #order of fields

