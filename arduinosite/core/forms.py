from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email_user = forms.EmailField(max_length=50, label='E-mail', help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email_user', 'password1', 'password2')