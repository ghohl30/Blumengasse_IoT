# Generated by Django 3.2.9 on 2021-11-25 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlantSensors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]