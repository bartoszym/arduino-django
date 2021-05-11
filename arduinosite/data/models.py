from django.db import models

from datetime import datetime, timedelta
import urllib.request


class DataManager(models.Manager):
    def get_last_week_average(self):
        time_now = datetime.utcnow()
        seven_days_ago = time_now - timedelta(days=7)
        last_weeks = self.model.objects.filter(date_time__gte=seven_days_ago)
        mean_value_last_week = last_weeks.aggregate(models.Avg('value'))['value__avg']
        return mean_value_last_week


class Data(models.Model):
    value = models.FloatField()
    date_time = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering = ['-date_time']
        get_latest_by = ['-date_time']

    objects = DataManager()
    

class Temperature(Data):
    
    @classmethod
    def get_temperature(cls):
        url = 'http://192.168.1.16/t' # adres dom
        # url = 'http://192.168.0.109/t' # adres Domi
        n = urllib.request.urlopen(url).read()
        n = n.decode("utf-8")
        cls.objects.create(value=n)
        return
    
    def __str__(self):
        return f'Temperatura {self.value} dnia {self.date_time.date()} o godz. {self.date_time.time()}'
    

class Humidity(Data):
    
    @classmethod
    def get_humidity(cls):
        url = 'http://192.168.1.16/h' # adres dom
        # url = 'http://192.168.0.109/h' # adres Domi
        n = urllib.request.urlopen(url).read()
        n = n.decode("utf-8")
        cls.objects.create(value=n)
        return
    
    def __str__(self):
        return f'Wilgotność {self.value} dnia {self.date_time.date()} o godz. {self.date_time.time()}'
    
    class Meta(Data.Meta):
        verbose_name_plural = 'humidities'
        

class Lightness(Data):
        
    @classmethod
    def get_lightness(cls):
        url = 'http://192.168.1.16/l' # adres dom
        # url = 'http://192.168.0.109/l' # adres Domi
        n = urllib.request.urlopen(url).read()
        n = n.decode("utf-8")
        cls.objects.create(value=n)
        return
    
    def __str__(self):
        return f'Jasność {self.value} dnia {self.date_time.date()} o godz. {self.date_time.time()}'