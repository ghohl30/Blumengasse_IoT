from django.shortcuts import render
from django.http import HttpResponse
import datetime

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

        time = []
        data = []

        for r in queryset:
            time.append(r.time.isoformat())
            data.append(r.reading)

        #plots.append({'time': time, 'data': data, 'type': s.sensor_type})
        plots.append((time,data,s.sensor_type))


    context = {'plots': plots}

    return render(request, 'PlantSensors/charts.html', context=context)

def get_data(request, sensor, reading):
    sensor = Sensor.objects.get(id=sensor)
    new_measurement = measurement(sensor=sensor, reading=reading)
    new_measurement.save()
    return HttpResponse("Thanks!")
