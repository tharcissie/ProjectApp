from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Profile, Rate
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.forms import *
from rest_framework import viewsets
from .serializers import ProfileSerializer, ProjectSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse
# Create your views here.

class ProjectList(APIView):
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileList(APIView):
    def get(self, request, format=None):
        all_users = Profile.objects.all()
        serializers = ProfileSerializer(all_users, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


    

def home(request):
    profiles = Profile.objects.all()
    rates = Rate.objects.all()
    if request.method == "POST":
        form = ProjectForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user.profile
            project.save()
    else:
        form = ProjectForm()

    try:
        projects = Project.objects.all()
    except Project.DoesNotExist:
        projects = None
    return render(request, 'home.html', {'projects': projects, 'form': form, 'profiles':profiles, 'rates':rates})



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


# class ProfileViewSet(viewsets.ModelViewSet):     
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class ProjectViewSet(viewsets.ModelViewSet):
#     """
#     A simple ViewSet for listing or retrieving projects.
#     """
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer


@login_required(login_url='login')
def profile(request, username):
    projects = request.user.profile.projects.all()
    if request.method == 'POST':
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return redirect(request.path_info)
    else:
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    if request.method == "POST":
        form = ProjectForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user.profile
            project.save()
    else:
        form = ProjectForm()

    context = {
        'prof_form': prof_form,
        'projects': projects,
        'form':form,

    }
    return render(request, 'profile.html', context)



# @login_required(login_url='login')
# def user_profile(request, username):
#     user_prof = get_object_or_404(User, username=username)
#     if request.user == user_prof:
#         return redirect('userprofile', username=request.user.username)
#     user_projects = user_prof.profile.projects.all()
#     context = {
#         'user_prof': user_prof,
#         'user_posts': user_posts,
#     }
#     return render(request, 'userprofile.html', context)


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
def project(request,id):
    project = Project.objects.get(id = id)
    rates = Rate.objects.order_by('-date')
    current_user = request.user
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            design = form.cleaned_data['design']
            usability = form.cleaned_data['usability']
            content = form.cleaned_data['content']
            rate = Rate()
            rate.project = project
            rate.user = current_user
            rate.design = design
            rate.usability = usability
            rate.content = content
            rate.average = (rate.design + rate.usability + rate.content)/3
            rate.save()
            # return redirect('index')
            return HttpResponseRedirect(reverse('project', args=(project.id,)))
    else:
        form = RateForm()
    context={"project":project,"rates":rates,"form":form}
    return render(request, 'project.html',context)



# @login_required(login_url='login')
# def rate_project(request,project_id):
#     proj = Project.project_by_id(id=project_id)
#     project = get_object_or_404(Project, pk=project_id)
#     current_user = request.user
#     if request.method == 'POST':
#         form = RateForm(request.POST)
#         if form.is_valid():
#             design = form.cleaned_data['design']
#             usability = form.cleaned_data['usability']
#             content = form.cleaned_data['content']
#             rate = Rate()
#             rate.project = project
#             rate.user = current_user
#             rate.design = design
#             rate.usability = usability
#             rate.content = content
#             rate.average = (rate.design + rate.usability + rate.content)/3
#             rate.save()
#             # return redirect('index')
#             return HttpResponseRedirect(reverse('project', args=(project.id,)))
#     else:
#         form = RateForm()
#     return render(request, 'rates.html', {"user":current_user,"project":proj,"form":form})








def search_projects(request):
    if 'project' in request.GET and request.GET["project"]:
        search = request.GET.get("project")
        projects = Project.search_by_project_name(search)
        message = f"{search}"
        context = {"projects":projects, 'search':search}
        return render(request, 'result.html',context)
    else:
        message = "You haven't searched for any term"
        return render(request, 'result.html',{"message":message})
