from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

from .models import Sensor, measurement

from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .forms import coarse, datepicker

def index(request, coarsing=1, timeframe=1):
    if 'Auflösung' in request.GET.keys():
        coarsing=int(request.GET['Auflösung'])
    if 'Zeitrahmen' in request.GET.keys():
        timeframe=int(request.GET['Zeitrahmen'])

    plots = []

    for s in Sensor.objects.all():
        queryset = measurement.objects.filter(sensor=s)

        # Timeframe filter
        if timeframe!=0:
            now = datetime.now()
            earlier = now - timedelta(hours=timeframe)
            queryset = queryset.filter(time__range=[earlier, now])

        types = list(queryset.order_by().values_list('type', flat=True).distinct())
        for type in types:
            q = queryset.filter(type=type)

            time = []
            data = []

            for r in q:
                time.append(r.time.isoformat())
                data.append(r.reading)
            time = time[::coarsing]
            data = data[::coarsing]
            #plots.append({'time': time, 'data': data, 'type': s.sensor_type})
            plots.append((time,data,type,s.sensor_name))


    context = {'plots': plots}
    context['form'] = coarse(initial={'Auflösung':str(coarsing), 'Zeitrahmen':str(timeframe)})


    return render(request, 'PlantSensors/charts.html', context=context)

def date_view(request, coarsing=20):
    begin = datetime.now()- timedelta(hours=24)
    end = datetime.now()
    if 'Auflösung' in request.GET.keys():
        coarsing=int(request.GET['Auflösung'])
    if 'Anfang_month' in request.GET.keys():
        begin=datetime(year=int(request.GET['Anfang_year']), month=int(request.GET['Anfang_month']), day=int(request.GET['Anfang_day']))
    if 'Ende_month' in request.GET.keys():
        end=datetime(year=int(request.GET['Ende_year']), month=int(request.GET['Ende_month']), day=int(request.GET['Ende_day']))


    plots = []

    for s in Sensor.objects.all():
        queryset = measurement.objects.filter(sensor=s)

        queryset = queryset.filter(time__range=[begin, end])

        types = list(queryset.order_by().values_list('type', flat=True).distinct())
        for type in types:
            q = queryset.filter(type=type)
            time = []
            data = []

            for r in q:
                time.append(r.time.isoformat())
                data.append(r.reading)
            time = time[::coarsing]
            data = data[::coarsing]
            #plots.append({'time': time, 'data': data, 'type': s.sensor_type})
            plots.append((time,data,type,s.sensor_name))


    context = {'plots': plots}
    context['form'] = datepicker(initial={'Anfang':begin, 'Ende':end})


    return render(request, 'PlantSensors/charts.html', context=context)


@csrf_exempt
def get_data(request, sensor_id):
    if not request.method=='POST':
        return HttpResponseForbidden('Nothing to get here')
    if not request.headers['token'] == '1234':
        return HttpResponseForbidden('Permission denied')

    data = json.loads(request.body)
    sensor = Sensor.objects.get(sensor_id=sensor_id)
    for key, value in data.items():
        print(value)
        new_measurement = measurement(sensor=sensor, reading=value, type=key)
        new_measurement.save()
    settings = {'interval': sensor.sensor_interval}
    return JsonResponse(settings)

@csrf_exempt
def register_sensor(request):
    data = json.loads(request.body)
    if not request.method=='POST':
        return HttpResponseForbidden('Nothing to get here')
    if not request.headers['token'] == '1234':
        return HttpResponseForbidden('Permission denied')
    if not Sensor.objects.filter(sensor_id=data['sensor_id']):
        s = Sensor(sensor_id=data['sensor_id'], sensor_type=data['sensor_type'], sensor_name=data['sensor_id'], sensor_interval=data['interval'])
        s.save()
        return HttpResponse("Gotcha")
    return HttpResponse("Already know you")
