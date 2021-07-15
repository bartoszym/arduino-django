from django.db import models
from django.db.utils import IntegrityError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from datetime import timedelta
from bs4 import BeautifulSoup
import requests


class DataManager(models.Manager):
    def get_last_week_average(self):
        time_now = timezone.now()
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
    
    @classmethod
    def get_data(cls, element_id):
        url = 'http://192.168.1.5' # adres dom
        try:
            page = requests.get(url)
        except requests.exceptions.ConnectionError:
            return -1
        soup = BeautifulSoup(page.content, 'html.parser')
        temp = soup.find_all(id=element_id)[-1].get_text()
        try:
            cls.objects.create(value=temp)
        except IntegrityError:
            return -2
        return

class Temperature(Data):
    
    @classmethod
    def get_data(cls, element_id='t'):
        return super().get_data(element_id)
    
    def __str__(self):
        return _('Temperature {} day {} at {}').format(self.value, self.date_time.date(), self.date_time.time().strftime("%H:%M"))
    

class Humidity(Data):
    
    @classmethod
    def get_data(cls, element_id='h'):
        return super().get_data(element_id)
    
    def __str__(self):
        return _('Humidity {} day {} at {}').format(self.value, self.date_time.date(), self.date_time.time().strftime("%H:%M"))
    
    class Meta(Data.Meta):
        verbose_name_plural = 'humidities'
        

class Lightness(Data):
        
    @classmethod
    def get_data(cls, element_id='l'):
        return super().get_data(element_id)
    
    def __str__(self):
        return _('Lightness {} day {} at {}').format(self.value, self.date_time.date(), self.date_time.time().strftime("%H:%M"))