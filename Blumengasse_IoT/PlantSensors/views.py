from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
import datetime
import json
from django.views.decorators.csrf import csrf_exempt

from .models import Sensor, measurement

from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# # Create your views here.
# def index(request):
#     time = []
#     data = []
#
#
#     s = Sensor.objects.get(id=1)
#     queryset = measurement.objects.filter(sensor=s)
#     for r in queryset:
#         time.append(r.time)
#         data.append(r.reading)
#
#     # List of graph objects for figure.
#     # Each object will contain on series of data.
#     graphs = []
#
#     # Adding linear plot of y1 vs. x.
#     graphs.append(
#         go.Scatter(x=time, y=data, mode='markers', name='Line y1')
#     )
#
#     graphs.append(
#         go.Scatter(x=time, y=data, name='Line y1')
#     )
#
#     # Setting layout of the figure.
#     layout = {
#         'title': 'Title of the figure',
#         'xaxis_title': 'X',
#         'yaxis_title': 'Y',
#         'height': 420,
#         'width': 560,
#     }
#
#     # Getting HTML needed to render the plot.
#     plot_div = plot({'data': graphs, 'layout': layout},
#                     output_type='div')
#
#
#
#     return render(request, 'PlantSensors/plot.html',
#                   context={'plot_div': plot_div})


# Create your views here.
# def index(request):
#     time = []
#     data = []
#
#
#     s = Sensor.objects.get(id=1)
#     queryset = measurement.objects.filter(sensor=s)
#     for r in queryset:
#         time.append(r.time)
#         data.append(r.reading)
#
#     fig = make_subplots(rows=2, cols=2, start_cell="bottom-left")
#
#     # Adding linear plot of y1 vs. x.
#     plot1 = go.Scatter(x=time, y=data, mode='markers', name='Line y1')
#
#     fig.add_trace(go.Scatter(x=time, y=data, mode='markers', name='Line y1'), row=1, col=1)
#     fig.add_trace(go.Scatter(x=time, y=data, mode='markers', name='Line y1'), row=1, col=2)
#     fig.add_trace(go.Scatter(x=time, y=data, mode='markers', name='Line y1'), row=2, col=1)
#     fig.add_trace(go.Scatter(x=time, y=data, mode='markers', name='Line y1'), row=2, col=2)
#
#     fig.update_layout(autosize=True,
#                   title_text="Multiple Subplots with Titles")
#
#     context = {'graph': fig.to_html(full_html=False, default_height=500, default_width=700)}
#
#     return render(request, 'PlantSensors/plot1.html', context=context )

# def index(request):
#
#     time = []
#     data = []
#
#
#     s = Sensor.objects.get(id=1)
#     queryset = measurement.objects.filter(sensor=s)
#     for r in queryset:
#         time.append(r.time.isoformat())
#         data.append(r.reading)
#
#     context = {'time': time, 'data': data, 'type': s.sensor_type}
#
#     return render(request, 'PlantSensors/charts.html', context=context)

def index(request):

    plots = []

    for s in Sensor.objects.all():
        queryset = measurement.objects.filter(sensor=s)
        types = list(queryset.order_by().values_list('type', flat=True).distinct())
        for type in types:
            q = queryset.filter(type=type)
            time = []
            data = []

            for r in q:
                time.append(r.time.isoformat())
                data.append(r.reading)

            #plots.append({'time': time, 'data': data, 'type': s.sensor_type})
            plots.append((time,data,type))


    context = {'plots': plots}

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
        new_measurement = measurement(sensor=sensor, reading=value, type=key)
        new_measurement.save()
    return HttpResponse("Thanks!")

@csrf_exempt
def register_sensor(request):
    data = json.loads(request.body)
    if not request.method=='POST':
        return HttpResponseForbidden('Nothing to get here')
    if not request.headers['token'] == '1234':
        return HttpResponseForbidden('Permission denied')
    if not Sensor.objects.filter(sensor_id=data['sensor_id']):
        s = Sensor(sensor_id=data['sensor_id'], sensor_type=data['sensor_type'], sensor_name=data['sensor_id'])
        s.save()
        return HttpResponse("Gotcha")
    return HttpResponse("Already know you")

def test_http(request):
    print("someone requested")
    # if request.headers['token'] == '1234':
    #     return HttpResponse("That worked")
    settings = {'name': 'Wohnzimmer', 'interval': 15}
    if request.method == 'POST':
        print('yes')
        return JsonResponse(settings)
    return HttpResponseForbidden("nope")
