from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Profile, Rating
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserCreationFormm, ProjectForm, UpdateUserForm, UpdateUserProfileForm, RatingsForm
import random
from rest_framework import viewsets
from .serializers import ProfileSerializer, UserSerializer, ProjectSerializer
# Create your views here.


def home(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
    else:
        form = ProjectForm()

    try:
        projects = Project.objects.all()
        random_project = random.randint(0, len(projects)-1)
        random_project = posts[random_project]
    except Project.DoesNotExist:
        projects = None
    return render(request, 'home.html', {'projects': projects, 'form': form, 'random_project': random_project})



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class ProfileViewSet(viewsets.ModelViewSet):     
    """
    A simple ViewSet for listing or retrieving users.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving projects.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


@login_required(login_url='login')
def profile(request, username):
    return render(request, 'profile.html')


def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    context = {
        'user_prof': user_prof,
    }
    return render(request, 'userprofile.html', context)


@login_required(login_url='login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', user.username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'prof_form': prof_form
    }
    return render(request, 'update.html', context)


@login_required(login_url='login')
def project(request, pk):
    project = Project.objects.get(pk=pk)
    rating = Rating.objects.filter(user=request.user, project=project).first()
    rating_status = None
    if rating is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project = project
            rate.save()
            project_rating = Rating.objects.filter(project=project)

            design_rating = [design.design for design in project_rating]
            design_average = sum(design_rating) / len(design_rating)

            usability_rating = [usability.usability for usability in project_rating]
            usability_average = sum(usability_rating) / len(usability_rating)

            content_rating = [content.content for content in project_rating]
            content_average = sum(content_rating) / len(content_rating)

            score = (design_average + usability_average + content_average) / 3
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingsForm()
    context = {
        'project': project,
        'rating_form': form,
        'rating_status': rating_status

    }
    return render(request, 'project.html', context)


def search_project(request):
    if request.method == 'GET':
        project_name = request.GET.get("project_name")
        results = Project.objects.filter(title__icontains=project_name).all()
        context = {
            'results': results,
        }
        return render(request, 'results.html', context)