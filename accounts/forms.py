# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile
from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')


class ProfileForm(forms.ModelForm):
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': "locationTextField"}))

    class Meta:
        model = Profile
        fields = ('bio', 'location')
