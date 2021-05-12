from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.template import loader

from datetime import datetime

from data.models import Temperature, Humidity, Lightness


class HomePageView(TemplateView):
    template_name = "home.html"
    
def home_page(request):
    last_temperature = Temperature.objects.latest('date_time')
    last_humidity = Humidity.objects.latest('date_time')
    last_lightness = Lightness.objects.latest('date_time')
    temperature_week_average = Temperature.objects.get_last_week_average()
    humidity_week_average = Humidity.objects.get_last_week_average()
    lightness_week_average = Lightness.objects.get_last_week_average()
    current_date = datetime.utcnow()
    # current_time = 
    current_hour = datetime.utcnow().hour
    context = {
        'last_temperature': last_temperature,
        'current_hour': current_hour,
        'current_date': current_date,
        'last_humidity': last_humidity,
        'temperature_week_average': temperature_week_average,
        'humidity_week_average': humidity_week_average,
        'last_lightness': last_lightness,
        'lightness_week_average': lightness_week_average
        }
    return render(request, 'home.html', context)

def get_temperature(request):
    Temperature.get_temperature()
    return redirect('core:home')

def get_humidity(request):
    Humidity.get_humidity()
    return redirect('core:home')

def get_lightness(request):
    Lightness.get_lightness()
    return redirect('core:home')