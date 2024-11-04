# SIL Documentation
Welcome to the documentation for the SIL project! This documentation provides an overview of the project, installation instructions, usage examples, and API reference. Feel free to navigate through the sections below for more details.

## Overview
SIL is a comprehensive weather application designed specifically for airplanes and airports. Its primary goal is to provide real-time, accurate weather data and forecasts to support flight operations and ensure aviation safety. By integrating advanced meteorological data, the app delivers crucial information on wind speeds, visibility, precipitation, and temperature, as well as severe weather alerts such as thunderstorms and turbulence.

This system is designed to address the unique challenges faced by both airports and airlines, including:

- **Flight Planning:** Providing pilots and air traffic controllers with up-to-date weather reports for safe and efficient route planning.
* **Airport Management:** Assisting airports in handling ground operations by monitoring weather conditions affecting takeoffs, landings, and maintenance.
+ **Safety:** Issuing real-time weather alerts for hazardous conditions, helping to minimize risks and ensure compliance with aviation safety regulations.

With its intuitive interface and precise weather modeling, SIL aims to enhance the decision-making process in aviation by offering a reliable tool for meteorological insights.

## Prerequisites

Before installing **SIL**, make sure you have the following installed:

- Python 3.8+

* PostgreSQL(or another compatible databese)

+ Git

## Installation
To install **SIL**, follow these steps:

1. Clone the repository:
``` 
git clone https://github.com/SIL-Ohjelmistoprojekti/Sil-BackEnd

```

2. Install the necessary dependencies:

Option 1: Using requirements.txt (recommended):

```
pip install -r requirements.txt
```

Option 2: Manually install key dependencies:

```
pip install django
pip install djangorestframework
pip install requests
pip install django-cors-headers

``` 
## Usage
Here’s a quick guide on how to use **SIL:**

1. Run the application:
```
python manage.py runserver
``` 

By default, this runs the server on ```http://127.0.0.1:8000```.

2. Access the weather data:
+ METAR data: ```http://127.0.0.1:8000/metar/```
+ Weather data (from files): ```http://127.0.0.1:8000/weather/``` 

3. Response Formats: You can request data in both HTML or JSON format by using the ```?muoto=``` query parameter:

+ HTML: ```?muoto=html``` (default)
+ JSON: ```?muoto=json```


## API Documentation
The following section provides a reference to the API exposed by **SIL**.

Endpoints:

1. Get current weather data from the test folder:
```
GET /weather/
```
This endpoint retrieves weather data from the most recent file in the ```test``` folder. The response can be in HTML or JSON format.

Example JSON:

``` 
{
    "one_hour_rainfall": ["0.0 mm"],
    "twenty_four_hour_rainfall": ["2.5 mm"],
    "temperature": ["12°C"],
    "humidity": ["78%"],
    "barometric_pressure": ["1013 hPa"],
    "wind_direction": ["270°"],
    "average_wind_speed": ["10 km/h"],
    "max_wind_speed": ["15 km/h"]
}

```

2. Get METAR data for a specific airport

``` 
GET /metar/
``` 
This endpoint fetches METAR (Meteorological Aerodrome Report) data from an external source. You can request the data in either HTML or JSON format by using the ```?muoto=``` query parameter.

Example (JSON):

```
{
    "station": {"name": "EFHK"},
    "raw_text": "METAR EFHK 121350Z 27005KT 9999 FEW030 07/03 Q1021 NOSIG",
    "temperature": {"celsius": "7"},
    "dew_point": {"celsius": "3"},
    "humidity": {"percent": 80.0},
    "wind": {
        "direction": "270",
        "speed_kph": 9.26,
        "unit": "KT"
    },
    "visibility": {"text": "10 km or more"},
    "barometer": {"hpa": "1021"},
    "ceiling": {"feet": 3000},
    "cloud_cover": ["FEW030"],
    "observed": "12-11-2023 13:50 UTC",
    "change_code": "NOSIG",
    "change_description": "No significant changes expected"
}
```

## Contributing
We welcome contributions to **SIL**! Follow these steps to contribute:


1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of the changes.
4. Run the tests to verify your changes:
```
python manage.py test
```
5. Submit a pull request with a detailed description of your changes.

Please ensure your code adheres to the project’s coding standards, and that all tests pass.

## Code Style

+ Ensure your code is formatted according to **PEP 8** guidelines.

+ Use **black** or **flake8** to liint your code before submitting

### License
SIL is released under the MIT license. See the LICENSE file for more details.

