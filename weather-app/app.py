# weather-app
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
import requests
import json

with open('./weather-app/api.json', 'r') as fobj:
    API_key = json.load(fobj)['api_key']

def kelvin_to_celsius(kelvin):
    celsius = round((kelvin - 273.15), 2)
    return celsius

def wind_direction_to_compass(degree):
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    index = round(degree / 22.5) % 16
    return directions[index]

def get_location(city, limit=1):
    location_string = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={API_key}"
    response = requests.get(location_string).json()
    location = {}
    location['lat'] = response[0]['lat']
    location['lon'] = response[0]['lon']
    return location
    
def get_weather(city):
    lat = get_location(city)['lat']
    lon = get_location(city)['lon']
    weather_string = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}"
    weather = requests.get(weather_string).json()
    return weather

def get_weather_condition(city, condition):
    if condition == 'description':
        return get_weather(city)['weather'][0]['description']
    elif condition == 'temp':
        return kelvin_to_celsius(get_weather(city)['main']['temp'])
    elif condition == 'feels_like':
        return kelvin_to_celsius(get_weather(city)['main']['feels_like'])
    elif condition == 'humidity':
        return get_weather(city)['main']['humidity']
    elif condition == 'pressure':
        return get_weather(city)['main']['pressure']
    elif condition == 'wind_speed':
        return get_weather(city)['wind']['speed']
    elif condition == 'wind_direction':
        return wind_direction_to_compass(get_weather(city)['wind']['deg'])
    elif condition == 'clouds':
        return get_weather(city)['clouds']['all']

def update_labels(event):
    print('Labels have been updated')

# setup
window = ttk.Window('flatly')
window.title('My Weather')
window.geometry('600x400')

city_list = ['New York', 'London', 'Paris', 'Berlin', 'Tokyo', 'Melbourne',
             'Hong Kong', 'Sydney', 'Rio de Janeiro', 'Boston', 'Miami',
             'Lisabon', 'Kairo', 'Istanbul', 'Dubai', 'Kabul', 'New Dehli',
             'Bangkok', 'Kuala Lumpur', 'Jakarta', 'Sydney', 'Auckland', 'Lima',
             'Buenes Aires', 'Bogota', 'Havana', 'Chicago', 'Montreal', 'Vancouver',
             'Seattle', 'Mexico City', 'Las Vegas', 'Houston', 'Honolulu']

# widgets
combo_cities = ttk.Combobox(window)
combo_cities['values'] = sorted(city_list)

# layout
combo_cities.pack()

# events
combo_cities.bind('<<ComboboxSelected>>', update_labels)

# run
window.mainloop()