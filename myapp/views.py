from django.http import HttpResponse
import os
from django.conf import settings

def index(request):
    return HttpResponse("Tervetuloa sovelluksen etusivulle!")
#python manage.py runserver
#http://127.0.0.1:8000/weather
def weather_data_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'w.txt')
    
    with open(file_path, 'r') as file:
        data = file.read()

    # datan jako osiksi
    lines = data.split('\n')

    # tehdään termit ja muuttujattt
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

    # käydää jaetut osat läpi ja lisätään ne muuttujiin
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

    # jotta saadaan tohon nettisivuun niin ilmeisesti html rakennetta pitää olla. tehdään myös riveittäi
    html_response = "<h2>Weather Data</h2><ul>"
    
    for key, values in weather_data.items():
        html_response += f"<li><strong>{key.replace('_', ' ').title()}:</strong></li>"
        for value in values:
            html_response += f"<li>{value}</li>"
    
    html_response += "</ul>"

    return HttpResponse(html_response)