from django.contrib import admin

# Register your models here.
from .models import Sensor, measurement

admin.site.register(Sensor)

#admin.site.register(measurement)

@admin.register(measurement)
class measurementAdmin(admin.ModelAdmin):
    list_filter = ['type',]
