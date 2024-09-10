from django.urls import path
from . import views
from . import views1

urlpatterns = [
    path('', views.index, name='index'),  
    path('weather/', views.weather_data_view, name='weather_data'),  
    path('api/weather/', views1.weather_data_api, name='weather_data_api'),  # Add this line
]
