# Generated by Django 3.1.2 on 2020-11-04 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcalendar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcategory',
            name='color',
            field=models.CharField(choices=[('green', 'Green'), ('red', 'Red'), ('orange', 'Orange'), ('blue', 'Blue'), ('grey', 'Grey'), ('yellow', 'Yellow'), ('purple', 'Purple')], default='green', max_length=6),
        ),
    ]
