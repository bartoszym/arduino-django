# Generated by Django 3.2.2 on 2021-05-08 16:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='humidity',
            options={'verbose_name_plural': 'humidities'},
        ),
        migrations.AlterField(
            model_name='temperature',
            name='date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
