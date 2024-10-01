import requests
from datetime import datetime

def parse_metar(raw_metar):
    # Jäsennä METAR-data
    lines = raw_metar.strip().split('\n')
    
    if not lines or len(lines) < 2:
        raise ValueError("METAR data is not in the expected format")
    
    latest_metar = lines[-1]  # Viimeisin rivi
    parts = latest_metar.split(' ')
    
    # Muunna aikaleima selkeäksi päivämääräksi ja kellonajaksi
    timestamp = parts[1]
    day = int(timestamp[:2])
    hour = int(timestamp[2:4])
    minute = int(timestamp[4:6])
    observed_time = datetime.utcnow().replace(day=day, hour=hour, minute=minute, second=0, microsecond=0)
    observed_str = observed_time.strftime('%d-%m-%Y %H:%M UTC')
    
    # Tulevien muutosten koodit ja selitykset
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
    
    data = {
        'station': {'name': parts[0]},
        'raw_text': latest_metar,
        'temperature': {'celsius': parts[7].split('/')[0] if '/' in parts[7] else 'N/A'},
        'wind': {'speed_kph': parts[2]},
        'variety': parts[3],
        'visibility': {'meters': parts[4]},
        'barometer': {'hpa': parts[9][1:] if len(parts) > 9 else 'N/A'},
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
