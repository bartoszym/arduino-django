from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('temperatures/', TemperatureListView.as_view(), name='temperature-list'),
    path('temperatures/charts', temperature_chart, name='temperature-chart'),
    path('temperatures/delete/<int:pk>/', TemperatureDeleteView.as_view(), name='temperature-delete'),
    path('humidities/', HumidityListView.as_view(), name='humidity-list'),
    path('humidities/delete/<int:pk>/', HumidityDeleteView.as_view(), name='humidity-delete'),
    path('lightnesses/', LightnessListView.as_view(), name='lightness-list'),
    path('lightnesses/delete/<int:pk>/', LightnessDeleteView.as_view(), name='lightness-delete'),
]