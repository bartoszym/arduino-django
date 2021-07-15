from django.urls import path

from .views import *
from .models import Temperature, Humidity, Lightness

urlpatterns = [
    path('temperatures/', TemperatureListView.as_view(), name='temperature-list'),
    path('temperatures/charts', chart, kwargs=dict(model=Temperature), name='temperature-chart'),
    path('temperatures/delete/<int:pk>/', TemperatureDeleteView.as_view(), name='temperature-delete'),
    path('humidities/', HumidityListView.as_view(), name='humidity-list'),
    path('humidities/charts', chart, kwargs=dict(model=Humidity), name='humidity-chart'),
    path('humidities/delete/<int:pk>/', HumidityDeleteView.as_view(), name='humidity-delete'),
    path('lightnesses/', LightnessListView.as_view(), name='lightness-list'),
    path('lightnesses/charts', chart, kwargs=dict(model=Lightness), name='lightness-chart'),
    path('lightnesses/delete/<int:pk>/', LightnessDeleteView.as_view(), name='lightness-delete'),
]