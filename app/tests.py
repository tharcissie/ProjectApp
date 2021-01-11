from django.test import TestCase
from .models import *


class TestProfile(TestCase):
    def setUp(self):
        self.user = User(id=1, username='tharcissie', password='12345678')
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()


class ProjectTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='tharcissie')
        self.project = Project.objects.create(id=1, project_name='name', details='details',
                                        user=self.user, link='http://link.coml')

    def test_instance(self):
        self.assertTrue(isinstance(self.project, project))

    def test_save_Project(self):
        self.project.save_Project()
        project = Project.objects.all()
        self.assertTrue(len(project) > 0)

    def test_get_Projects(self):
        self.project.save()
        projects = Project.all_Projects()
        self.assertTrue(len(projects) > 0)

    def test_search_Project(self):
        self.project.save()
        project = project.search_project('test')
        self.assertTrue(len(project) > 0)

    def test_delete_Project(self):
        self.project.delete_Project()
        project = project.search_project('test')
        self.assertTrue(len(project) < 1)


class RatingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='tharcissie')
        self.project = Project.objects.create(id=1, project_name='name', details='details',
                                        user=self.user, link='http://link.coml')
        self.rating = Rating.objects.create(id=1, design=6, usability=7, content=9, user=self.user, project=self.project)

    def test_instance(self):
        self.assertTrue(isinstance(self.rating, Rating))

    def test_save_rating(self):
        self.rating.save_rating()
        rating = Rating.objects.all()
        self.assertTrue(len(rating) > 0)

    def test_get_Project_rating(self, id):
        self.rating.save()
        rating = Rating.get_ratings(project_id=id)
        self.assertTrue(len(rating) == 1)
