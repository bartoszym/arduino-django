from typing import Set
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, View

from .forms import *
from datetime import datetime

from .models import Settings
from data.models import Temperature, Humidity, Lightness

class SettingsView(LoginRequiredMixin, View):
    template_name = 'settings_form.html'
    
    def get_object(self):
        try:
            object = Settings.objects.get(pk=1)
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
    
    # form_class = SettingsForm
    # success_url = '/'
    
    # def get_form_class(self):
    #     form_class = super().get_form_class()
    #     print(form_class.fields)
    #     return form_class
    
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
    if Temperature.get_temperature() == False:
        messages.add_message(request, messages.ERROR, _('Arduino is not working, check if it\'s turned on!'))
    return redirect('core:home')

def get_humidity(request):
    if Humidity.get_humidity() == False:
        messages.add_message(request, messages.ERROR, _('Arduino is not working, check if it\'s turned on!'))
    return redirect('core:home')

def get_lightness(request):
    if Lightness.get_lightness() == False:
        messages.add_message(request, messages.ERROR, _('Arduino is not working, check if it\'s turned on!'))
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