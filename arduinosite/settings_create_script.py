import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arduinosite.settings")
import django
django.setup()

from core.models import Settings
Settings.objects.create(
    auto_update_temperature=False,
    auto_update_humidity=False,
    auto_update_lightness=False
    )