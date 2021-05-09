from django.db import models
from django.utils import timezone

from datetime import datetime, timedelta

import urllib.request


class DataManager(models.Manager):
    def is_last_higher_than_next_week(self):
        last_temperature = self.model.objects.latest().temperature
        time_now = datetime.utcnow()
        seven_days_ago = time_now - timedelta(days=7)
        last_weeks = self.model.objects.filter(date_time__gte=seven_days_ago)
        model_name = self.model.__name__.lower()
        mean_temperature_last_week = last_weeks.aggregate(models.Avg(model_name))[model_name+'__avg']
        print(mean_temperature_last_week)
        return True if last_temperature > mean_temperature_last_week else False


class Temperature(models.Model):
    class Meta:
        ordering = ['-date_time']
        get_latest_by = ['-date_time']
    temperature = models.FloatField()
    date_time = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f'Temperatura {self.temperature} dnia {self.date_time.date()} o godz. {self.date_time.time()}'
    
    objects = DataManager()


class Humidity(models.Model):
    class Meta:
        ordering = ['-date_time']
        get_latest_by = ['-date_time']
        verbose_name_plural = 'humidities'
    humidity = models.FloatField()
    date_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Wilgotność {self.humidity} dnia {self.date_time.date()} o godz. {self.date_time.time()}'
    
    objects = DataManager()