# Generated by Django 3.2.2 on 2021-05-11 16:26

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_lightness'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='humidity',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='lightness',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='temperature',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
