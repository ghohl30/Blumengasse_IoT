from django.urls import path

from . import views

app_name = "PlantSensors"
urlpatterns = [
    path('', views.index, name='index'),
    path('datum', views.date_view, name='date_view'),
    path('data/<int:sensor_id>', views.get_data, name="get_data"),
    path('register', views.register_sensor, name="register_sensor")
]
