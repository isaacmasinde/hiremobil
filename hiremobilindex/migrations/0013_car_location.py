# Generated by Django 2.2.10 on 2020-07-09 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hiremobilindex', '0012_auto_20200709_0745'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='Location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hiremobilindex.PickLoc'),
        ),
    ]
