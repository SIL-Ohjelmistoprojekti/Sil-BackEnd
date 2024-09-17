import requests

def get_metar_data():
    url = "https://api.checkwx.com/metar/EFHK/decoded"
    headers = {'X-API-Key': 'e2178bfe769b4d0792e10f9a5b'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve data", "status_code": response.status_code}
