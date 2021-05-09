from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.template import loader

from datetime import datetime

from data.models import Temperature, Humidity


class HomePageView(TemplateView):
    template_name = "home.html"
    
def home_page(request):
    last_temperature = Temperature.objects.latest('date_time')
    is_temp_higher = Temperature.objects.is_last_higher_than_next_week()
    is_humidity_higher = Humidity.objects.is_last_higher_than_next_week()
    last_humidity = Humidity.objects.latest('date_time')
    current_time = datetime.utcnow()
    context = {
        'last_temperature': last_temperature,
        'current_time': current_time,
        'last_humidity': last_humidity,
        'is_temp_higher': is_temp_higher,
        'is_humidity_higher': is_humidity_higher,
        }
    return render(request, 'home.html', context)
