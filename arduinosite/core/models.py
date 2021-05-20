from django.db import models
from django.utils.translation import gettext_lazy as _

class Settings(models.Model):
    time_choices = [(0, '')]
    time_choices.extend([(h, h) for h in range(1, 25)])
    
    auto_update_temperature = models.BooleanField(default=False, verbose_name=_('Automatic update of temperature'))
    update_temperature_time1 = models.IntegerField(choices=time_choices, default=0, verbose_name=_('Update time of temperature'))
    update_temperature_time2 = models.IntegerField(choices=time_choices, default=0, verbose_name=_('Update time of temperature'))
    update_temperature_time3 = models.IntegerField(choices=time_choices, default=0, verbose_name=_('Update time of temperature'))
    
    auto_update_humidity = models.BooleanField(default=False, verbose_name=_('Automatic update of humidity'))
    update_humidity_time1 = models.IntegerField(choices=time_choices, default=0, verbose_name=_('Update time of humidity'))
    update_humidity_time2 = models.IntegerField(choices=time_choices, default=0, verbose_name=_('Update time of humidity'))
    update_humidity_time3 = models.IntegerField(choices=time_choices, default=0, verbose_name=_('Update time of humidity'))
    
    auto_update_lightness = models.BooleanField(default=False, verbose_name=_('Automatic update of lightness'))
    update_lightness_time1 = models.IntegerField(choices=time_choices, default=0, verbose_name=_('Update time of lightness'))
    update_lightness_time2 = models.IntegerField(choices=time_choices, default=0, verbose_name=_('Update time of lightness'))
    update_lightness_time3 = models.IntegerField(choices=time_choices, default=0, verbose_name=_('Update time of lightness'))