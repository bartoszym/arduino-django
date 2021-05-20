from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import ExtractDay
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from calendar import month, monthrange
from datetime import datetime

from .forms import MonthForm
from .models import Temperature, Humidity, Lightness


class TemperatureListView(LoginRequiredMixin, ListView):
    model = Temperature
    paginate_by = 10
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('get_temp') is not None:
            self.model.get_temperature()
        elif request.POST.get('see_charts') is not None:
            return redirect('data:temperature-chart')
        return HttpResponseRedirect(self.request.path)
    
class TemperatureDeleteView(LoginRequiredMixin, DeleteView):
    model = Temperature
    template_name = 'data/data_object_delete.html'
    success_url = reverse_lazy('data:temperature-list')
        
class HumidityListView(LoginRequiredMixin, ListView):
    model = Humidity
    paginate_by = 10
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('get_hum') is not None:
            self.model.get_humidity()
        elif request.POST.get('see_charts') is not None:
            return redirect('data:humidity-chart')
        return HttpResponseRedirect(self.request.path)
    
class HumidityDeleteView(LoginRequiredMixin, DeleteView):
    model = Humidity
    template_name = 'data/data_object_delete.html'
    success_url = reverse_lazy('data:humidity-list')

class LightnessListView(LoginRequiredMixin, ListView):
    model = Lightness
    paginate_by = 10
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('get_light') is not None:
            self.model.get_lightness()
        elif request.POST.get('see_charts') is not None:
            return redirect('data:lightness-chart')
        return HttpResponseRedirect(self.request.path)
    
class LightnessDeleteView(LoginRequiredMixin, DeleteView):
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

@login_required
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

@login_required
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

@login_required
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