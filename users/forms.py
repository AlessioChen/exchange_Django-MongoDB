from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)

    class Meta: 
        model = User 
        fields  =['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
