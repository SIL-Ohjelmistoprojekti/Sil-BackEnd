import requests

def get_metar_data():
    url = "https://api.met.no/weatherapi/tafmetar/1.0/metar.txt?icao=EFHK"

    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return {"error": "Failed to retrieve data", "status_code": response.status_code}
