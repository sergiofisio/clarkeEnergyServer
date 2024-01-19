from django.urls import path
from app import views  # Importe o módulo views

urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
    path('login/', views.login, name='login'),
    path('csrf/', views.get_csrf_token, name='get_csrf_token'),
    path('users/', views.get_users, name='get_users'),
]
