from django.db import models
from django.utils import timezone

# Create your models here.
class Sensor(models.Model):
    sensor_name = models.CharField(max_length=20)
    sensor_type = models.CharField(max_length=20)

    def __str__(self):
        return str(self.sensor_name)

class measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    reading = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.reading)
