import json
from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings
from django.shortcuts import render
import requests

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .metar import get_metar_data

#laitettu pip install scrapy, pip install django djangorestframework


def index(request):
    return HttpResponse("Tervetuloa sovelluksen etusivulle!")
#python manage.py runserver
#http://127.0.0.1:8000/weather
def weather_data_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'w.txt')
    
    with open(file_path, 'r') as file:
        data = file.read()

    # Datan jako palasiksi
    lines = data.split('\n')

    # Tehdään termit ja muuttujattt
    weather_data = {
        'one_hour_rainfall': [],
        'twenty_four_hour_rainfall': [],
        'temperature': [],
        'humidity': [],
        'barometric_pressure': [],
        'wind_direction': [],
        'average_wind_speed': [],
        'max_wind_speed': []
    }

    # Käydään jaetut osat läpi ja lisätään ne muuttujiin
    for line in lines:
        if 'One Hour' in line:
            weather_data['one_hour_rainfall'].append(line.split(': ')[1])
        elif 'Rain Fall (24 Hour)' in line:
            weather_data['twenty_four_hour_rainfall'].append(line.split(': ')[1])
        elif 'Temperature' in line:
            weather_data['temperature'].append(line.split(': ')[1])
        elif 'Humidity' in line:
            weather_data['humidity'].append(line.split(': ')[1])
        elif 'Barometric Pressure' in line:
            weather_data['barometric_pressure'].append(line.split(': ')[1])
        elif 'Wind Direction' in line:
            weather_data['wind_direction'].append(line.split(': ')[1])
        elif 'Average Wind Speed (One Minute)' in line:
            weather_data['average_wind_speed'].append(line.split(': ')[1])
        elif 'Max Wind Speed (Five Minutes)' in line:
            weather_data['max_wind_speed'].append(line.split(': ')[1])

    # HTML-vastailun käsittely. Sekä strong class että selkeempi näkyvyys
    html_response = "<h2>Weather Data</h2><ul>"
    
    for key, values in weather_data.items():
        html_response += f"<li><strong>{key.replace('_', ' ').title()}:</strong></li>"
        for value in values:
            html_response += f"<li>{value}</li>"
    
    html_response += "</ul>"

    # Tsekkaillaan URLI
    #http://127.0.0.1:8000/weather/?muoto=html
    response_format = request.GET.get('muoto', 'html')
#http://127.0.0.1:8000/weather/?muoto=json
    if response_format == 'json':
        return JsonResponse(weather_data)
    else:
        return HttpResponse(html_response)#
    

@api_view(['GET'])
def metar(request):
    data = get_metar_data()
    response_format = request.GET.get('muoto', 'html')
    
    if response_format == 'json':
        return JsonResponse(data)
    else:
        # Luo HTML-vastaus
        html_response = f"""
        <html>
        <body>
            <h1>METAR Data for {data['data'][0]['station']['name']}</h1>
            <p>Temperature: {data['data'][0]['temperature']['celsius']}°C</p>
            <p>Humidity: {data['data'][0]['humidity']['percent']}%</p>
            <p>Wind: {data['data'][0]['wind']['speed_kph']} kph</p>
            <p>Visibility: {data['data'][0]['visibility']['meters']} meters</p>
            <p>Clouds: {data['data'][0]['clouds'][0]['text']} at {data['data'][0]['clouds'][0]['base_feet_agl']} feet</p>
        </body>
        </html>
        """
        return HttpResponse(html_response)
    #http://127.0.0.1:8000/metar/
    #http://127.0.0.1:8000/metar/?muoto=html
    #http://127.0.0.1:8000/metar/?muoto=json¨
    