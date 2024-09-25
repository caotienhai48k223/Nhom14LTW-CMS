from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('account/<str:str>/', account, name='account'),
    path('post/<str:str>/<slug:slug>/', post_detail, name='post-detail'),
    path('update-profile/<str:str>/', update_profile, name='update-profile'),
    path('enjoys/<str:str>/', enjoy_posts, name='enjoy'),
    path('search/', search, name='search')
]