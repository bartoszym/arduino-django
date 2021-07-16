from django_cron import CronJobBase, Schedule

from core.models import Settings
from data.models import Humidity, Lightness, Temperature
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

import datetime
import requests

from bs4 import BeautifulSoup
from arduinosite.settings import EMAIL_HOST_USER


def get_temperature_update_times():
    sett = Settings.objects.first()
    if sett.auto_update_temperature == False:
        return
    hours = []
    if sett.update_temperature_time1 != -1:
        hours.append(sett.update_temperature_time1)
    if sett.update_temperature_time2 != -1:
        hours.append(sett.update_temperature_time2)
    if sett.update_temperature_time3 != -1:
        hours.append(sett.update_temperature_time3)
    hours.sort()
    hours = [f'{i}:01' for i in hours]
    
    return hours

class UpdateTemperatureCron(CronJobBase):
    RUN_AT_TIMES = get_temperature_update_times()
    
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'core.UpdateTemperatureCron'
    
    def do(self):
        Temperature.get_data()
        return


def get_humidity_update_times():
    sett = Settings.objects.first()
    if sett.auto_update_humidity == False:
        return
    hours = []
    if sett.update_humidity_time1 != -1:
        hours.append(sett.update_humidity_time1)
    if sett.update_humidity_time2 != -1:
        hours.append(sett.update_humidity_time2)
    if sett.update_humidity_time3 != -1:
        hours.append(sett.update_humidity_time3)
    hours.sort()
    hours = [f'{i}:01' for i in hours]
    
    return hours

class UpdateHumidityCron(CronJobBase):
    RUN_AT_TIMES = get_humidity_update_times()
    
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'core.UpdateHumidityCron'
    
    def do(self):
        Humidity.get_data()
        return
    
    
def get_lightness_update_times():
    sett = Settings.objects.first()
    if sett.auto_update_lightness == False:
        return
    hours = []
    if sett.update_lightness_time1 != -1:
        hours.append(sett.update_lightness_time1)
    if sett.update_lightness_time2 != -1:
        hours.append(sett.update_lightness_time2)
    if sett.update_lightness_time3 != -1:
        hours.append(sett.update_lightness_time3)
    hours.sort()
    hours = [f'{i}:01' for i in hours]
    
    return hours

class UpdateLightnessCron(CronJobBase):
    RUN_AT_TIMES = get_lightness_update_times()
    
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'core.UpdateLightnessCron'
    
    def do(self):
        Lightness.get_data()
        return
    
    
class MoveDetectionCron(CronJobBase):
    RUN_EVERY_MINS = 1
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'core.MoveDetectionCron'
    
    def do(self):
        sett = Settings.objects.first()
        if sett.move_checker_beeper == False:
            return
    
        now = datetime.datetime.now().time()
        times = sett.move_checker_time
        times_splitted = times.split(',')
        for i in times_splitted:
            first, second = i.split('-')
            first_hour, first_minutes = first.split(':')
            second_hour, second_minutes = second.split(':')
            first_hour, first_minutes, second_hour, second_minutes = int(first_hour), int(first_minutes), int(second_hour), int(second_minutes)
            start_time = datetime.time(first_hour, first_minutes, 0)
            end_time = datetime.time(second_hour, second_minutes, 0)
            if start_time <= now <= end_time:
                url = 'http://192.168.1.5/m'
                try:
                    page = requests.get(url)
                except requests.exceptions.ConnectionError:
                    return False
                soup = BeautifulSoup(page.content, 'html.parser')
                move = soup.find_all(id='t')[-1].get_text()
                move = move.rstrip()
                if move == '11' or move == '1111' and sett.move_checker_email:
                    send_mail(_('Move detected'), _(f'Arduino detected move.'), EMAIL_HOST_USER, [sett.user_email], fail_silently=False)