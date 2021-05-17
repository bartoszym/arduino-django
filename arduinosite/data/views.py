from django.db.models.functions import ExtractDay
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from calendar import month, monthrange
from datetime import datetime

from .forms import MonthForm
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

def create_form(request):
    chosen_month = datetime.today().month
    if request.method == 'POST':
        form = MonthForm(request.POST, initial={'month': chosen_month})
        if form.is_valid():
            chosen_month = form.cleaned_data['month']
    else:
        form = MonthForm(initial={'month': chosen_month})
        
    return form, chosen_month

def create_chart_data(queryset):
    chart_dict = {}
    month_length = monthrange(datetime.today().year, datetime.today().month)[1]
    
    for i in range(1, month_length+1):
        daily_values = queryset.filter(day=i)
        values_amount = daily_values.aggregate(amount=Sum('value'))['amount']
        if values_amount:
            average_value = round(values_amount/len(daily_values), 2)
            chart_dict[i] = average_value
        else:
            chart_dict[i] = 0
            
    return chart_dict

def temperature_chart(request):
    form, chosen_month = create_form(request)
    
    temperatures_current_month = Temperature.objects.filter(
        date_time__month=chosen_month
        ).annotate(day=ExtractDay('date_time')).values('day', 'value')
    
    chart_dict = create_chart_data(temperatures_current_month)
    
    return render(request, 'data/chart.html', {
        'labels': list(chart_dict.keys()),
        'data': list(chart_dict.values()),
        'form': form,
    })

def humidity_chart(request):
    form, chosen_month = create_form(request)
    
    humidities_current_month = Humidity.objects.filter(
        date_time__month=chosen_month
        ).annotate(day=ExtractDay('date_time')).values('day', 'value')
    
    chart_dict = create_chart_data(humidities_current_month)
    
    return render(request, 'data/chart.html', {
        'labels': list(chart_dict.keys()),
        'data': list(chart_dict.values()),
        'form': form,
    })
    
def lightness_chart(request):
    form, chosen_month = create_form(request)
    
    lightnesses_current_month = Lightness.objects.filter(
        date_time__month=chosen_month
        ).annotate(day=ExtractDay('date_time')).values('day', 'value')
    
    chart_dict = create_chart_data(lightnesses_current_month)
    
    return render(request, 'data/chart.html', {
        'labels': list(chart_dict.keys()),
        'data': list(chart_dict.values()),
        'form': form,
    })