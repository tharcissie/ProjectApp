from django.urls import path, include
from .views import home, UserViewSet, ProjectViewSet, ProfileViewSet,signup,profile, edit_profile, project, search_project
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('projects', ProjectViewSet)
router.register('profile', ProfileViewSet)


urlpatterns = [
   
    path('', home, name = 'home'),
    path('signup/', signup, name='signup'),
    path('api/', include(router.urls)),
    #path('<username>/',user_profile, name='userprofile'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('profile/<username>/', profile, name='profile'),
    path('profile/<username>/', edit_profile, name='edit_Profile'),
    path('project/<pk>',project, name='project'),
    path('search/', search_project, name='search'),
]
