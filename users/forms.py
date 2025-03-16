from django import forms
from .models import Users
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['username','email', 'password1', 'password2']
