from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('get_temperature/', get_temperature, name='get-temperature'),
    path('get_humidity/', get_humidity, name='get-humidity'),
    path('get_lightness/', get_lightness, name='get-lightness'),
    path('settings/<int:pk>/', SettingsView.as_view(), name='settings'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]