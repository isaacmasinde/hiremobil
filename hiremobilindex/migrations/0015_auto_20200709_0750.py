# Generated by Django 2.2.10 on 2020-07-09 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiremobilindex', '0014_auto_20200709_0749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pickloc',
            name='Latitude',
        ),
        migrations.RemoveField(
            model_name='pickloc',
            name='Longitude',
        ),
    ]