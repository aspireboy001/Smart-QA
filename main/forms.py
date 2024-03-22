from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User 
        fields = ["username","email","password1","password2"]

class PostQuestion(forms.ModelForm): #PostForm
    class Meta:
        model = Question 
        fields = ['title','description']

class PostAnswer(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']


# Db Models