# Generated by Django 2.2.10 on 2020-07-10 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hiremobilindex', '0018_delete_deal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('To', models.DateField()),
                ('Status', models.CharField(max_length=50)),
                ('Charge', models.IntegerField()),
                ('Car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hiremobilindex.Car')),
                ('Client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hiremobilindex.Client')),
                ('Location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hiremobilindex.PickLoc')),
                ('Saler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hiremobilindex.Owner')),
            ],
        ),
    ]
