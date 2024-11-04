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
          https://github.com/SIL-Ohjelmistoprojekti/Sil-FrontEnd
          https://github.com/SIL-Ohjelmistoprojekti/Linux_serveri_BackEnd
          https://github.com/SIL-Ohjelmistoprojekti/Tailwind_FrontEnd
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

Run the application:
```
python manage.py runserver
``` 

(Add additional usage examples, command-line arguments, or configuration details here if needed.)

## API Documentation
The following section provides a reference to the API exposed by **SIL**.

Example API Endpoints:

+ Get current weather data for an airport:
```
GET /api/weather/{airport_code}
```
Response:

``` 
{
  "temperature": "15°C",
  "wind_speed": "12 knots",
  "visibility": "10 km",
  "precipitation": "None",
  "alerts": []
}
```
+ Get weather forecast for a flight route:
Response

```
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

