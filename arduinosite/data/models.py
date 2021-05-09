from django.db import models
from django.utils import timezone

from datetime import datetime, timedelta

import urllib.request


class DataManager(models.Manager):
    def is_last_higher_than_next_week(self):
        last_value = self.model.objects.latest().value
        time_now = datetime.utcnow()
        seven_days_ago = time_now - timedelta(days=7)
        last_weeks = self.model.objects.filter(date_time__gte=seven_days_ago)
        mean_values_last_week = last_weeks.aggregate(models.Avg('value'))['value__avg']
        print(mean_values_last_week)
        return True if last_value > mean_values_last_week else False


class Temperature(models.Model):
    class Meta:
        ordering = ['-date_time']
        get_latest_by = ['-date_time']
    value = models.FloatField()
    date_time = models.DateTimeField(auto_now=True)
    
    @classmethod
    def get_temperature(cls):
        url = 'http://192.168.1.16/t'
        n = urllib.request.urlopen(url).read()
        n = n.decode("utf-8")
        cls.objects.create(value=n)
        return
    
    def __str__(self):
        return f'Temperatura {self.value} dnia {self.date_time.date()} o godz. {self.date_time.time()}'
    
    objects = DataManager()
    

class Humidity(models.Model):
    class Meta:
        ordering = ['-date_time']
        get_latest_by = ['-date_time']
        verbose_name_plural = 'humidities'
    value = models.FloatField()
    date_time = models.DateTimeField(auto_now=True)
    
    @classmethod
    def get_humidity(cls):
        url = 'http://192.168.1.16/h'
        n = urllib.request.urlopen(url).read()
        n = n.decode("utf-8")
        cls.objects.create(value=n)
        return
    
    def __str__(self):
        return f'Wilgotność {self.value} dnia {self.date_time.date()} o godz. {self.date_time.time()}'
    
    objects = DataManager()