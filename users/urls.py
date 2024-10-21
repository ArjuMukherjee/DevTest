# users/urls.py
from django.urls import path
from .views import profile_view, edit_profile_view, delete_profile_view, register_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('delete-profile/', delete_profile_view, name='delete_profile'),
]
