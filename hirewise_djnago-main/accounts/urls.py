"""
accounts/urls.py — URL patterns for authentication
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',        views.auth_view,    name='auth'),
    path('login/',  views.auth_view,    name='login'),
    path('logout/', views.logout_view,  name='logout'),
    path('profile/',views.profile_view, name='profile'),
]
