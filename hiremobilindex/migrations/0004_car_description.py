# Generated by Django 2.2.10 on 2020-06-20 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiremobilindex', '0003_auto_20200619_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='Description',
            field=models.TextField(null=True),
        ),
    ]
