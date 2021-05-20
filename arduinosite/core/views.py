from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from .forms import RegisterForm
from datetime import datetime

from .models import Settings
from data.models import Temperature, Humidity, Lightness


class SettingsView(LoginRequiredMixin, UpdateView):
    model = Settings
    fields = [
        'auto_update_temperature', 'update_temperature_time1', 'update_temperature_time2', 'update_temperature_time3',
        'auto_update_humidity', 'update_humidity_time1', 'update_humidity_time2', 'update_humidity_time3',
        'auto_update_lightness', 'update_lightness_time1', 'update_lightness_time2', 'update_lightness_time3'
        ]
    template_name = 'settings_form.html'
    success_url = '/'
    
def home_page(request):
    last_temperature = Temperature.objects.latest('date_time')
    last_humidity = Humidity.objects.latest('date_time')
    last_lightness = Lightness.objects.latest('date_time')
    temperature_week_average = Temperature.objects.get_last_week_average()
    humidity_week_average = Humidity.objects.get_last_week_average()
    lightness_week_average = Lightness.objects.get_last_week_average()
    current_date = datetime.utcnow()
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

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, password = request.POST['password1'])
            login(request, authenticated_user)
            return redirect('core:home')
    else:
        form = RegisterForm()
        
    context = {'form': form}
    
    return render(request, 'register.html', context)