from __future__ import absolute_import, unicode_literals
import requests
import json
from celery import shared_task
from mypubsub.celery import app



BIRDY_SERVICE_URL = "http://150.230.46.230:8000/" # HOSTED ON CLOUD
BIRDY_BEARER_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NCwiZXhwIjoxNjg0MTAzNzMyfQ.Trt_slqO6ttmlfMAfmZXhA5lcNyWN4kd8NfbMSap-_U"
OPENWEATHER_SERVICE_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_APIKEY = "51221f79a18cef82c14e9e73aad25715"




ROUTING_KEYS = {
    "Santa Clara" : "sfkey",
    "Manhattan" : "nykey",
}      
        
@shared_task
def notify_user(data, exchange):

    payload = {
        "lat": data['latitude'],
        "lon": data['longitude'],
        "appid": OPENWEATHER_APIKEY,
        "units": "metric",  
    }
        
    r = requests.get(BIRDY_SERVICE_URL + "weather/fetchcurrent", params=payload, headers={'Authorization': BIRDY_BEARER_TOKEN})
    weather_data = json.loads(r.text)
    print(weather_data)
    routing_key = ROUTING_KEYS[weather_data['name']]
    
    message = {"weather_data": generate_message(weather_data)}
    
    with app.producer_pool.acquire(block=True) as producer:
        producer.publish(
            message,
            exchange=exchange,
            routing_key=routing_key,
        )


def generate_message(weather_data):
    temperature = weather_data["temp"]
    feels_like = weather_data["feels_like"]
    city = weather_data["name"]
    
    return f"{temperature}°C is the temperature in {city} and it feels like {feels_like}°C."