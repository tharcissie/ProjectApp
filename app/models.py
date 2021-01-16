from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime as dt
import numpy as np


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='images/', default='default.jpg')
    bio = models.TextField(max_length=500, default="My Bio", blank=True)
    contact = models.EmailField(max_length=100, blank=True)

    def __str__(self):
         return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile

class Project(models.Model):
    project_name = models.CharField(max_length=155)
    link = models.URLField(max_length=255)
    details = models.TextField(max_length=255)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="projects")
    date = models.DateTimeField(auto_now_add=True, blank=True)
    image = models.ImageField(upload_to='projectpics/',default='a.png')

    class Meta:
        ordering = ["-pk"]


    def avg_design(self):
        design_rates = list(map(lambda x: x.design, self.project.all()))
        return np.mean(design_rates)
    def avg_content(self):
        content_rates = list(map(lambda x: x.content, self.project.all()))
        return np.mean(content_rates)
    def avg_usability(self):
        usability_rates = list(map(lambda x: x.usability, self.project.all()))
        return np.mean(usability_rates)


   



    def __str__(self):
        return self.project_name

    def delete_poject(self):
        self.delete()

    # @classmethod
    # def search_project(cls, project_name):
    #     return cls.objects.filter(project_name__icontains=project_name).all()

    @classmethod
    def get_projects(cls):
        projects = Project.objects.all()
        return projects

    def save_project(self):
        self.save()


    @classmethod
    def project_by_id(cls,id):
        project = Project.objects.filter(id =id)
        return project

    @classmethod
    def get_profile_pic(cls,profile):
        projects = Project.objects.filter(profile__pk = profile)
        return projects

    @classmethod
    def search_by_project_name(cls,search):
    	projects = cls.objects.filter(project_name__icontains=search)
    	return projects


class Rate(models.Model):
    rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rate')
    design = models.IntegerField(choices=rating, default=0, blank=True)
    usability = models.IntegerField(choices=rating,default=0, blank=True)
    content = models.IntegerField(choices=rating,default=0, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def save_rate(self):
        self.save()

    class Meta:
        ordering = ["-pk"]

  

    # def design_average(self):
    #     design_average = sum(self.design) / len(self.design)
    #     return design_average

    # def usability_average(self):
    #     usability_average = sum(self.design) / len(self.design)
    #     return usability_average

    # def content_average(self):
    #     content_average = sum(self.design) / len(self.design)
    #     return content_average