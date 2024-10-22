from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from store.models import UserProfile

class SignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class SignInForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["bio","profile_picture","phone"]