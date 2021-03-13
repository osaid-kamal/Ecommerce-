from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from mycart.settings import AUTHENTICATION_BACKEND
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  myuser


class RegForm(UserCreationForm):
    email = forms.EmailField(
        max_length=60, help_text="Required valid Email Address")

    class Meta:
        model = myuser
        fields = ('email', 'username', 'password1', 'password2')


class logged(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = myuser
        fields = ("email", 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invailid Login !")


