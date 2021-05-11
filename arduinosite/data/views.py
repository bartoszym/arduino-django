from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

import urllib.request

from .models import Temperature, Humidity, Lightness

def index(request):
    return HttpResponse("Hello world")

class TemperatureListView(ListView):
    model = Temperature
    paginate_by = 10
    
    def post(self, request, *args, **kwargs):
        self.model.get_temperature()
        return HttpResponseRedirect(self.request.path)
    
class TemperatureDeleteView(DeleteView):
    model = Temperature
    template_name = 'data/data_object_delete.html'
    success_url = reverse_lazy('data:temperature-list')
        
class HumidityListView(ListView):
    model = Humidity
    paginate_by = 10
    
    def post(self, request, *args, **kwargs):
        self.model.get_humidity()
        return HttpResponseRedirect(self.request.path)
    
class HumidityDeleteView(DeleteView):
    model = Humidity
    template_name = 'data/data_object_delete.html'
    success_url = reverse_lazy('data:humidity-list')

class LightnessListView(ListView):
    model = Lightness
    paginate_by = 10
    
    def post(self, request, *args, **kwargs):
        self.model.get_lightness()
        return HttpResponseRedirect(self.request.path)
    
class LightnessDeleteView(DeleteView):
    model = Lightness
    template_name = 'data/data_object_delete.html'
    success_url = reverse_lazy('data:lightness-list')
