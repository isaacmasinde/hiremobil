# Generated by Django 2.2.10 on 2020-06-23 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiremobilindex', '0005_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Contact', models.CharField(max_length=50)),
                ('Pin', models.CharField(max_length=50)),
            ],
        ),
    ]
