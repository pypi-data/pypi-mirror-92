# Generated by Django 3.1.2 on 2020-11-04 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcalendar', '0006_auto_20201104_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventhost',
            name='twitter',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
