import requests
from datetime import datetime
import math

def calculate_relative_humidity(temperature, dew_point):
    # Muunna lämpötila ja kastepiste Celsius-asteista Kelvin-asteiksi. Joo tää on COpilot shittii
    temp_k = float(temperature) + 273.15
    dew_point_k = float(dew_point) + 273.15
    
    # Laske suhteellinen kosteus
    humidity = 100 * (math.exp((17.625 * float(dew_point)) / (243.04 + float(dew_point))) / 
                      math.exp((17.625 * float(temperature)) / (243.04 + float(temperature))))
    
    return round(humidity, 2)

def parse_metar(raw_metar):
    #  METAR-data
    lines = raw_metar.strip().split('\n')
    
    if not lines or len(lines) < 2:
        raise ValueError("METAR data is not in the expected format")
    
    latest_metar = lines[-1]  # Viimeisin rivi
    parts = latest_metar.split(' ')
    
    # Kellonaika ja päivämäärä. HUOM SIVUSTOLLA ON SUOMEN AIKA KUN API KÄYTTÄÄ NORJAN AIKAA.
    timestamp = parts[1]
    day = int(timestamp[:2])
    hour = int(timestamp[2:4])
    minute = int(timestamp[4:6])
    observed_time = datetime.utcnow().replace(day=day, hour=hour, minute=minute, second=0, microsecond=0)
    observed_str = observed_time.strftime('%d-%m-%Y %H:%M UTC')
    
    # Nsoig eli vika kohta ja siihen selitykset
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
    
    # Tsekataan, että lämpötila- ja kastepistearvot on olemassa
    temperature = 'N/A'
    dew_point = 'N/A'
    for part in parts:
        if '/' in part:
            temperature, dew_point = part.split('/')
            break
    
    # Lasketaan  (ilman) kosteus
    humidity = 'N/A'
    if temperature != 'N/A' and dew_point != 'N/A':
        humidity = calculate_relative_humidity(temperature, dew_point)
    
    #  ilmanpaine kässittely (barometer)
    barometer = 'N/A'
    for part in parts:
        if part.startswith('Q'):
            barometer = part[1:]
            break
    
    #  pilvikorkeus lasku (ceiling)
    ceiling = 'N/A'
    for part in parts:
        if part.startswith('FEW') or part.startswith('SCT') or part.startswith('BKN') or part.startswith('OVC'):
            ceiling = int(part[3:]) * 100  # Muunna jalat metreiksi
            break
    
    data = {
        'station': {'name': parts[0]},
        'raw_text': latest_metar,
        'temperature': {'celsius': temperature},
        'dew_point': {'celsius': dew_point},
        'humidity': {'percent': humidity},
        'wind': {'speed_kph': parts[2]},
        'variety': parts[3],
        'visibility': {'meters': parts[4]},
        'barometer': {'hpa': barometer},
        'ceiling': {'feet': ceiling},
        'observed': observed_str,
        'change_code': change_code,
        'change_description': change_description
    }
    
    return data

def get_metar_data():
    url = "https://api.met.no/weatherapi/tafmetar/1.0/metar.txt?icao=EFHK"

    response = requests.get(url)
    if response.status_code == 200:
        raw_metar = response.text
        return parse_metar(raw_metar)
    else:
        return {"error": "Failed to retrieve data", "status_code": response.status_code}
