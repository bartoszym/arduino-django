from django.db import models
from django.utils.translation import gettext_lazy as _

class Settings(models.Model):
    time_choices = [(-1, '')]
    time_choices.extend([(h, h) for h in range(1, 24)])
    time_choices.extend([(0, 24)])
    
    auto_update_temperature = models.BooleanField(default=False, verbose_name=_('Automatic update of temperature'))
    update_temperature_time1 = models.IntegerField(choices=time_choices, default=-1, verbose_name=_('Update time of temperature'))
    update_temperature_time2 = models.IntegerField(choices=time_choices, default=-1, verbose_name=_('Update time of temperature'))
    update_temperature_time3 = models.IntegerField(choices=time_choices, default=-1, verbose_name=_('Update time of temperature'))
    
    auto_update_humidity = models.BooleanField(default=False, verbose_name=_('Automatic update of humidity'))
    update_humidity_time1 = models.IntegerField(choices=time_choices, default=-1, verbose_name=_('Update time of humidity'))
    update_humidity_time2 = models.IntegerField(choices=time_choices, default=-1, verbose_name=_('Update time of humidity'))
    update_humidity_time3 = models.IntegerField(choices=time_choices, default=-1, verbose_name=_('Update time of humidity'))
    
    auto_update_lightness = models.BooleanField(default=False, verbose_name=_('Automatic update of lightness'))
    update_lightness_time1 = models.IntegerField(choices=time_choices, default=-1, verbose_name=_('Update time of lightness'))
    update_lightness_time2 = models.IntegerField(choices=time_choices, default=-1, verbose_name=_('Update time of lightness'))
    update_lightness_time3 = models.IntegerField(choices=time_choices, default=-1, verbose_name=_('Update time of lightness'))
    
    move_checker_beeper = models.BooleanField(default=False, verbose_name=_('Should Arduino beep when something is moving'))
    move_checker_email = models.BooleanField(default=False, verbose_name=_('Should e-mail be send when something is moving'))
    user_email = models.EmailField(null=True, blank=True, verbose_name=_('E-mail on which message will be sent'))
    move_checker_time = models.CharField(
        blank=True, null=True, max_length=100,
        help_text=_('In which hours motion detector should be on.'
                    'Values has to be in format hh:mm-hh:mm, divided by commas, f.e. 13:40-15:60'),
        verbose_name=_('Hours in which move detection is on'))