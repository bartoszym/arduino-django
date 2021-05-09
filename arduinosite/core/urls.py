from django.urls import path

from .views import *

urlpatterns = [
    # path('', HomePageView.as_view(), name='home'),
    path('', home_page, name='home'),
    path('get_temperature/', get_temperature, name='get-temperature'),
]