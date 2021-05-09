from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

import urllib.request

from .models import Temperature, Humidity

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
    success_url = reverse_lazy('data:temperature-list')
        
class HumidityListView(ListView):
    model = Humidity
    paginate_by = 10
    
    def post(self, request, *args, **kwargs):
        self.model.get_humidity()
        return HttpResponseRedirect(self.request.path)
    
class HumidityDeleteView(DeleteView):
    model = Humidity
    success_url = reverse_lazy('data:humidity-list')
