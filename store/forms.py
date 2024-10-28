from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from store.models import UserProfile,Project

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

class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=["title","description","preview_image","price",
                "files","tag_objects","thumbnail"]
        widgets={
            "title":forms.TextInput(attrs={'class':'w-full p-2 border border-3 border-solid border-black'}),
            "description":forms.Textarea(attrs={'class':'w-full p-2 border border-3 border-solid border-black'}),
            "preview_image":forms.FileInput(attrs={'class':'w-full'}),
            "price":forms.TextInput(attrs={'class':'w-full p-2 border border-3 border-solid border-black'}),
            "files":forms.FileInput(attrs={'class':'w-full'}),
            "tag_objects":forms.SelectMultiple(attrs={'class':'w-full'}),
            "thumbnail":forms.TextInput(attrs={'class':'w-full p-2 border border-3 border-solid border-black'})
        }
