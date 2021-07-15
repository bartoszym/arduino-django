from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Settings
import re

class RegisterForm(UserCreationForm):
    email_user = forms.EmailField(max_length=50, label='E-mail', help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email_user', 'password1', 'password2')
        
class TemperatureSettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['auto_update_temperature', 'update_temperature_time1',
                  'update_temperature_time2', 'update_temperature_time3']
        
class HumiditySettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['auto_update_humidity', 'update_humidity_time1',
                  'update_humidity_time2', 'update_humidity_time3']
        
class LightnessSettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['auto_update_lightness', 'update_lightness_time1',
                  'update_lightness_time2', 'update_lightness_time3']
        
class MoveCheckerSettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['move_checker_beeper', 'move_checker_email', 'user_email', 
                  'move_checker_time']
        
    def clean_move_checker_time(self):
        move_checker_time = self.cleaned_data['move_checker_time']
        if move_checker_time is None:
            return move_checker_time
        times = re.findall(r'^(([0-1]?[0-9]|2[0-3]):[0-5][0-9]-([0-1]?[0-9]|2[0-3]):[0-5][0-9](,|))*$', move_checker_time)
        if not times:
            raise ValidationError(_('Bad value, enter it again!'))
        times_splitted = move_checker_time.split(',')
        if len(times_splitted) > 2:
            raise ValidationError(_("You can enter up to 2 different ranges!"))
        for i in times_splitted:
            first, second = i.split('-')
            first_hour, first_minutes = first.split(':')
            second_hour, second_minutes = second.split(':')
            first_hour, first_minutes, second_hour, second_minutes = int(first_hour), int(first_minutes), int(second_hour), int(second_minutes)
            print(first_hour, second_hour)
            print(first_minutes, second_minutes)
            if first_hour > second_hour:
                raise ValidationError(_('Bad value, enter it again!'))
            if first_hour == second_hour and second_minutes < first_minutes:
                raise ValidationError(_('Bad value, enter it again!'))
            
        return move_checker_time