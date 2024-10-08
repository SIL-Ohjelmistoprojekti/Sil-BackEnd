import requests
from datetime import datetime
import math
import re

# Funktio suhteellisen kosteuden laskemiseen
def calculate_relative_humidity(temperature, dew_point):
    temp_k = float(temperature) + 273.15
    dew_point_k = float(dew_point) + 273.15
    
    humidity = 100 * (math.exp((17.625 * float(dew_point)) / (243.04 + float(dew_point))) / 
                      math.exp((17.625 * float(temperature)) / (243.04 + float(temperature))))
    
    return round(humidity, 2)

# METAR-datan parsiminen
def parse_metar(raw_metar):
    lines = raw_metar.strip().split('\n')
    
    if not lines or len(lines) < 2:
        raise ValueError("METAR data is not in the expected format")
    
    latest_metar = lines[-1]
    parts = latest_metar.split(' ')
    
    # Aika
    timestamp = parts[1]
    day = int(timestamp[:2])
    hour = int(timestamp[2:4])
    minute = int(timestamp[4:6])
    observed_time = datetime.utcnow().replace(day=day, hour=hour, minute=minute, second=0, microsecond=0)
    observed_str = observed_time.strftime('%d-%m-%Y %H:%M UTC')
    
    # Muutoksen koodit
    change_codes = {
        'NOSIG': 'No significant changes expected',
        'BECMG': 'Becoming - Conditions are expected to change gradually',
        'TEMPO': 'Temporary - Temporary changes expected',
        'PROB30': 'Probability 30% - 30% chance of occurrence',
        'PROB40': 'Probability 40% - 40% chance of occurrence',
        'FM': 'From - Change starting from a specific time',
        'TL': 'Until - Change lasting until a specific time',
        'AT': 'At - Change occurring at a specific time'
    }
    
    change_code = parts[-1] if parts[-1] in change_codes else 'NOSIG'
    change_description = change_codes.get(change_code, 'No significant changes expected')
    
    # Lämpötila ja kastepiste
    temperature = 'N/A'
    dew_point = 'N/A'
    for part in parts:
        if '/' in part:
            temperature, dew_point = part.split('/')
            break
    
    humidity = 'N/A'
    if temperature != 'N/A' and dew_point != 'N/A':
        humidity = calculate_relative_humidity(temperature, dew_point)
    
    # Barometri (QNH)
    barometer = 'N/A'
    for part in parts:
        if part.startswith('Q'):
            barometer = part[1:]
            break
    
    # Pilvien kattavuus (ceiling)
    cloud_cover = []
    ceiling = 'N/A'
    for part in parts:
        if part.startswith(('FEW', 'SCT', 'BKN', 'OVC')):
            try:
                cloud_altitude = int(part[3:6]) * 100  # Ota numerot pilvikoodista
                cloud_cover.append(part)  # Lisää kaikki pilvien kattavuudet listaan
                if part.startswith('BKN') or part.startswith('OVC'):
                    ceiling = cloud_altitude  # Kattavuus "ceiling" tarkoittaa BKN/OVC kerrosta
            except ValueError:
                ceiling = 'N/A'
    
    # Tuuli
    wind_direction = parts[2][:3]
    wind_speed = parts[2][3:5]
    wind_unit = parts[2][-2:]  # Yksikkö (esim. KT)
    
    # Näkyvyys
    visibility = parts[3]
    visibility_text = f"{visibility} meters"
    if visibility.isdigit() and int(visibility) >= 9999:
        visibility_text = "10 km or more"
    
    # Palautettava data sanakirjassa
    data = {
        'station': {'name': parts[0]},
        'raw_text': latest_metar,
        'temperature': {'celsius': temperature},
        'dew_point': {'celsius': dew_point},
        'humidity': {'percent': humidity},
        'wind': {
            'direction': wind_direction,
            'speed_kph': round(float(wind_speed) * 1.852, 2),
            'unit': wind_unit
        },
        'visibility': {'text': visibility_text},
        'barometer': {'hpa': barometer},
        'ceiling': {'feet': ceiling},
        'cloud_cover': cloud_cover,
        'observed': observed_str,
        'change_code': change_code,
        'change_description': change_description
    }
    
    return data

# Funktio METAR-datan hakemiseen
def get_metar_data():
    url = "https://api.met.no/weatherapi/tafmetar/1.0/metar.txt?icao=EFHK"

    response = requests.get(url)
    if response.status_code == 200:
        raw_metar = response.text
        return parse_metar(raw_metar)
    else:
        return {"error": "Failed to retrieve data", "status_code": response.status_code}


# PostgreSQL-tallennus testivaiheessa
"""
def save_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write(str(data))

def save_to_postgresql(data):
    try:
        connection = psycopg2.connect(
            dbname="dbname",
            user="käyttis",
            password="passu",
            host="hostti",
            port="portti"
        )
        cursor = connection.cursor()
        
        insert_query = 
       INSERT INTO metar_data (station, raw_text, temperature, dew_point, humidity, wind_direction, wind_speed, wind_variety, visibility, barometer, ceiling, observed, change_code, change_description)
       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
     
        cursor.execute(insert_query, (
            data['station']['name'],
            data['raw_text'],
            data['temperature']['celsius'],
            data['dew_point']['celsius'],
            data['humidity']['percent'],
            data['wind']['direction'],
            data['wind']['speed_kph'],
            data['wind']['variety'],
            data['visibility']['text'],
            data['barometer']['hpa'],
            data['ceiling']['feet'],
            data['observed'],
            data['change_code'],
            data['change_description']
        ))
        
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as error:
        print(f"Error saving to PostgreSQL: {error}")
"""

if __name__ == "__main__":
    metar_data = get_metar_data()
    if "error" not in metar_data:
        save_to_file(metar_data, 'metar_data.txt')
        save_to_postgresql(metar_data)
    else:
        print(metar_data)
