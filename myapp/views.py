import os
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view
from .metar import get_metar_data

# Käytä pip:ä asentaaksesi tarvittavat paketit:
# pip install scrapy
# pip install django
# pip install djangorestframework
# pip install requests
# pip install django-cors-headers

def index(request):
    # Tämä näkymä näyttää yksinkertaisen tervehdyksen
    return HttpResponse("Tervetuloa sovelluksen etusivulle!")

# Helper function to get the latest file in a directory
def get_latest_file(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        return None
    latest_file = max(files, key=os.path.getmtime)
    return latest_file


# Tämä näkymä käsittelee säädatan näyttämistä
# Pythonin komennolla python manage.py runserver voit käynnistää palvelimen
# ja käydä näkymässä osoitteessa http://127.0.0.1:8000/weather
def weather_data_view(request):
    # Luetaan säädata kansiosta test
    test_folder = os.path.join(settings.BASE_DIR, 'test')

    # Get the latest file from the 'test' folder
    latest_file = get_latest_file(test_folder)

    if latest_file is None:
        return HttpResponse("No files found in the test folder.", status=404)
    
    # Avataan uusin tiedosto lukemista varten
    with open(latest_file, 'r') as file:
        data = file.read()

    # Jaetaan luettu data riveihin
    lines = data.split('\n')

    # Luodaan sanakirja säädatan säilyttämiseksi
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

    # Käydään jokainen rivi läpi ja lisätään tiedot oikeisiin kenttiin sanakirjassa
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

    # Tarkistetaan, onko käyttäjä pyytänyt JSON-muotoista dataa
    response_format = request.GET.get('muoto', 'html')
    
    if response_format == 'json':
        # Palautetaan säädata JSON-muodossa
        return JsonResponse(weather_data)
    else:
        # Renderöidään HTML-sivusto säädatalle
        return render(request, 'weather.html', {'weather_data': weather_data})

@api_view(['GET'])
def metar(request):
    # Haetaan METAR-tiedot ulkoisesta lähteestä
    data = get_metar_data()
    
    # Tarkistetaan, onko käyttäjä pyytänyt JSON-muotoista dataa
    response_format = request.GET.get('muoto', 'html')
    
    if response_format == 'json':
        # Palautetaan METAR-data JSON-muodossa
        return JsonResponse(data)
    else:
        # Renderöidään HTML-sivusto METAR-datalle
        metar_data = data['data'][0]
        return render(request, 'metar.html', {'metar_data': metar_data})
    
    # Näkymä on käytettävissä seuraavilla URL-osoitteilla:
    # http://127.0.0.1:8000/metar/
    # http://127.0.0.1:8000/metar/?muoto=html
    # http://127.0.0.1:8000/metar/?muoto=json
