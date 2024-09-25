from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='pro-home'),
    path('drafts/<str:str>/', draft_list, name='draft-list'),
    path('draft/<str:str>/<slug:slug>/', draft_detail, name='draft-detail'),
    path('post/<int:int>/', post_detail, name='pro-post-detail'),
    path('create-section/', create_section, name='create-section'),
    path('create-draft/', create_draft, name='create-draft'),
    path('update-draft/<str:str>/<slug:slug>/', update_draft, name='update-draft'),
    path('update-post/<int:int>/', update_post, name='update-post'),
    path('list-edit/', list_edit, name='list-edit'),
    path('pending-list/', pending_list, name='pending-list'),
    path('confirmation-list/', confirmation_list, name='confirmation-list')
]