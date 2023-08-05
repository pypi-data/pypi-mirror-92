# Generated by Django 3.1.2 on 2020-11-04 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcalendar', '0002_auto_20201104_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Host',
                'verbose_name_plural': 'Hosts',
            },
        ),
    ]
