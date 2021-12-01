from django.urls import path

from . import views

app_name = "PlantSensors"
urlpatterns = [
    path('', views.index, name='index'),
    path('data/<int:sensor>/<int:reading>', views.get_data, name="get_data")
]
