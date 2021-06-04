from typing import Set
from django_cron import CronJobBase, Schedule

from core.models import Settings
from data.models import Humidity, Lightness, Temperature

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
    hours = [f'{i}:49' for i in hours]
    
    return hours

class UpdateTemperatureCron(CronJobBase):
    RUN_AT_TIMES = get_temperature_update_times()
    
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'core.UpdateTemperatureCron'
    
    def do(self):
        Temperature.get_temperature()
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
    hours = [f'{i}:49' for i in hours]
    
    return hours

class UpdateHumidityCron(CronJobBase):
    RUN_AT_TIMES = get_humidity_update_times()
    
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'core.UpdateHumidityCron'
    
    def do(self):
        Humidity.get_humidity()
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
    hours = [f'{i}:49' for i in hours]
    
    return hours

class UpdateLightnessCron(CronJobBase):
    RUN_AT_TIMES = get_lightness_update_times()
    
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'core.UpdateLightnessCron'
    
    def do(self):
        Lightness.get_lightness()
        return