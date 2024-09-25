from django.urls import path
from .views import *

urlpatterns = [
    path('', pm_home, name='pm-home'),
    path('posts/', pm_post, name='pm-post'),
    path('users/', pm_user, name='pm-user')
]