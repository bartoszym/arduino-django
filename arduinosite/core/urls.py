from django.urls import path

from .views import *

urlpatterns = [
    # path('', HomePageView.as_view(), name='home'),
    path('', home_page, name='home'),
    path('get_temperature/', get_temperature, name='get-temperature'),
    path('get_humidity/', get_humidity, name='get-humidity'),
    path('get_lightness/', get_lightness, name='get-lightness'),
    path('register/', register, name='register'),
]