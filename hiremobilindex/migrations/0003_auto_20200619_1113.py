# Generated by Django 2.2.10 on 2020-06-19 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiremobilindex', '0002_auto_20200619_1110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='Year',
            new_name='ModelYear',
        ),
        migrations.AddField(
            model_name='car',
            name='Model',
            field=models.CharField(max_length=50, null=True),
        ),
    ]