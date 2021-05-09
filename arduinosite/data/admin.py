from django.contrib import admin

from .models import Temperature, Humidity

admin.site.register(Temperature)
admin.site.register(Humidity)