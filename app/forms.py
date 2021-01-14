from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project, Profile, Rate


class UserCreationFormm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name', 'link', 'details','image')


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'contact']


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        exclude = ['user', 'project']