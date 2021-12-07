#! /bin/bash

source ~/miniforge3/etc/profile.d/conda.sh
# activate environment
conda activate django_IoT

# cd into directory
cd Blumengasse_IoT

# Startserver on localhost
python manage.py runserver 0.0.0.0:8000
