# Generated by Django 3.2.2 on 2021-05-18 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='update_humidity_times',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='update_lighntess_times',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='update_temperature_times',
            field=models.JSONField(null=True),
        ),
    ]