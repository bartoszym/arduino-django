from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from .forms import *
from datetime import datetime

from .models import Settings
from data.models import Temperature, Humidity, Lightness
from data.utils import display_message


class SettingsView(LoginRequiredMixin, View):
    template_name = 'settings_form.html'
    
    def get_object(self):
        try:
            object, created = Settings.objects.get_or_create(pk=1)
        except Settings.DoesNotExist:
            raise Http404('Settings not found')
        
        return object
    
    def get_context_data(self, **kwargs):
        kwargs['settings'] = self.get_object()
        if 'temperature_settings_form' not in kwargs:
            kwargs['temperature_settings_form'] = TemperatureSettingsForm(instance=self.get_object())
        if 'humidity_settings_form' not in kwargs:
            kwargs['humidity_settings_form'] = HumiditySettingsForm(instance=self.get_object())
        if 'lightness_settings_form' not in kwargs:
            kwargs['lightness_settings_form'] = LightnessSettingsForm(instance=self.get_object())
        if 'move_checker_settings_form' not in kwargs:
            kwargs['move_checker_settings_form'] = MoveCheckerSettingsForm(instance=self.get_object())
            
        return kwargs
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        context = {}
        
        if 'temperature_settings' in request.POST:
            temperature_settings_form = TemperatureSettingsForm(request.POST, instance=self.get_object())
            
            if temperature_settings_form.is_valid():
                temperature_settings_form.save()
            else:
                context['temperature_settings_form'] = temperature_settings_form
                
        if 'humidity_settings' in request.POST:
            humidity_settings_form = HumiditySettingsForm(request.POST, instance=self.get_object())
            
            if humidity_settings_form.is_valid():
                humidity_settings_form.save()
            else:
                context['humidity_settings_form'] = humidity_settings_form
                
        if 'lightness_settings' in request.POST:
            lightness_settings_form = LightnessSettingsForm(request.POST, instance=self.get_object())
            
            if lightness_settings_form.is_valid():
                lightness_settings_form.save()
            else:
                context['lightness_settings_form'] = lightness_settings_form
                
        if 'move_checker_settings' in request.POST:
            move_checker_settings_form = MoveCheckerSettingsForm(request.POST, instance=self.get_object())
            
            if move_checker_settings_form.is_valid():
                move_checker_settings_form.save()
            else:
                context['move_checker_settings_form'] = move_checker_settings_form
                
        return render(request, self.template_name, self.get_context_data(**context))

    
def home_page(request):
    try:
        last_temperature = Temperature.objects.latest('date_time')
    except Temperature.DoesNotExist:
        last_temperature = 0
    try:
        last_humidity = Humidity.objects.latest('date_time')
    except Humidity.DoesNotExist:
        last_humidity = 0
    try:    
        last_lightness = Lightness.objects.latest('date_time')
    except Lightness.DoesNotExist:
        last_lightness = 0
    temperature_week_average = Temperature.objects.get_last_week_average()
    humidity_week_average = Humidity.objects.get_last_week_average()
    lightness_week_average = Lightness.objects.get_last_week_average()
    current_date = datetime.now()
    current_hour = datetime.now().hour
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

def get_data(request, **kwargs):
    model = kwargs['model']
    status = model.get_data()
    if status:
        display_message(status, request)
    
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