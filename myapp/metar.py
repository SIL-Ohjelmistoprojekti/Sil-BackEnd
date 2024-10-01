import requests

def parse_metar(raw_metar):
    # Jäsennä METAR-data
    lines = raw_metar.strip().split('\n')
    
    if not lines or len(lines) < 2:
        raise ValueError("METAR data is not in the expected format")
    
    latest_metar = lines[-1] # viimisin rivi.
    parts = latest_metar.split(' ')
    
    data = {
       'station': {'name': parts[0]},
    'raw_text': latest_metar,
    'temperature': {'celsius': parts[7].split('/')[0] if '/' in parts[7] else 'N/A'},
    'wind': {'speed_kph': parts[2]},
        'variety': { parts[3]},

    'visibility': {'meters': parts[4]},
    'barometer': {'hpa': parts[9][1:] if len(parts) > 9 else 'N/A'},
    'observed': parts[1]
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
