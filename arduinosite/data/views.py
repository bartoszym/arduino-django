from django.db.models.functions import ExtractDay
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from calendar import monthrange
from collections import defaultdict
from datetime import date, datetime

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

def temperature_chart(request):
    chart_dict = {}
    temperatures_current_month = Temperature.objects.filter(
        date_time__month=datetime.today().month
        ).annotate(day=ExtractDay('date_time')).values('day', 'value')
    month_length = monthrange(datetime.today().year, datetime.today().month)[1]
    for i in range(1, month_length+1):
        daily_values = temperatures_current_month.filter(day=i)
        values_amount = daily_values.aggregate(amount=Sum('value'))['amount']
        if values_amount:
            average_value = round(values_amount/len(daily_values), 2)
            chart_dict[i] = average_value
        else:
            chart_dict[i] = 0
        print(i, chart_dict[i])
    
    return JsonResponse({
        'title': 'Temperatury',
        'data': {
            'labels': list(chart_dict.keys()),
            'datasets': [{
                'label': 'Temperature',
                'background-color': '#79aec8',
                'border-color': '#79aec8',
                'data': list(chart_dict.values()),
            }]
        }
    })
            
            
            
    # for i in temperatures_current_month:
    #     chart_dict[i['day']] = chart_dict[i['day']] + i.get('value')
    #     # print(i.get('value'))
    # print(temperatures_current_month)
    # print(chart_dict)
