from django.db import models
from django.utils import timezone

# Create your models here.
class Sensor(models.Model):
    sensor_id = models.IntegerField(unique=True)
    sensor_name = models.CharField(max_length=20, unique=True)
    sensor_type = models.CharField(max_length=20)
    sensor_interval = models.IntegerField()

    def __str__(self):
        return str(self.sensor_name)

class measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    reading = models.FloatField()
    type = models.CharField(max_length=20)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.sensor.sensor_name + self.type + str(self.reading)
