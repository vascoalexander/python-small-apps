# weather-app
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from timezonefinder import TimezoneFinder
import json, requests
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.request import urlopen
from PIL import ImageTk

with open('./weather-app/api.json', 'r') as fobj:
    API_key = json.load(fobj)['api_key']

def wind_direction_to_compass(degree):
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    index = round(degree / 22.5) % 16
    return directions[index]

def update_labels(event):
    ow_api = update_api_data()
    data = update_data(ow_api)
    label_test.configure(text=data)
    label_city.configure(text=f"{city.get()}, {data['country']}")
    weather_image = get_weather_image(data)
    label_weather_image.configure(image=weather_image)
    label_weather_image.image = weather_image

def update_api_data():
    ow_api_call = f"https://api.openweathermap.org/data/2.5/weather?q={city.get()}&appid={API_key}&units={unit}"
    return requests.get(ow_api_call).json()

def update_data(ow_api):
    data['lon'] = ow_api['coord']['lon']
    data['lat'] = ow_api['coord']['lat']
    data['country'] = ow_api['sys']['country']
    data['datetime'] = get_datetime(ow_api)
    data['weather_id'] = ow_api['weather'][0]['id']
    data['weather_desc'] = ow_api['weather'][0]['description']
    data['weather_icon'] = ow_api['weather'][0]['icon']
    data['temp'] = ow_api['main']['temp']
    data['feels_like'] = ow_api['main']['feels_like']
    data['pressure'] = ow_api['main']['pressure']
    data['humidity'] = ow_api['main']['humidity']
    data['wind_speed'] = ow_api['wind']['speed']
    data['wind_direction'] = wind_direction_to_compass(ow_api['wind']['deg'])
    return data

def get_datetime(api_response):
    tz_obj = TimezoneFinder()
    timezone = tz_obj.timezone_at(lng=data['lon'],lat=data['lat'])
    time = datetime.now(ZoneInfo(timezone))
    timeformat_date = time.strftime("%b %d, %H:%M (%Z)")
    return timeformat_date

def get_weather_image(data):
    image_url = f"https://openweathermap.org/img/wn/{data['weather_icon']}@2x.png"
    image = urlopen(image_url)
    weather_image = ImageTk.PhotoImage(data=image.read())
    print(image_url)
    return weather_image

# setup
window = ttk.Window(themename='darkly')
window.title('Global Weather')
window.geometry('600x400')

city = tk.StringVar(value='New York')
unit = 'metric'

ow_api_call = f"https://api.openweathermap.org/data/2.5/weather?q={city.get()}&appid={API_key}&units={unit}"
ow_api = requests.get(ow_api_call).json()

data = {}
data = update_data(ow_api)
weather_image = get_weather_image(data)

city_list = ['New York', 'London', 'Paris', 'Berlin', 'Tokyo', 'Melbourne',
             'Hong Kong', 'Sydney', 'Rio de Janeiro', 'Boston', 'Miami',
             'Lisabon', 'Kairo', 'Istanbul', 'Dubai', 'Kabul',
             'Bangkok', 'Kuala Lumpur', 'Jakarta', 'Sydney', 'Auckland', 'Lima',
             'Buenes Aires', 'Bogota', 'Havana', 'Chicago', 'Montreal', 'Vancouver',
             'Seattle', 'Mexico City', 'Las Vegas', 'Houston', 'Honolulu']

# widgets
label_datetime = ttk.Label(window, text=data['datetime'], font=('Arial', 10), foreground='red')
label_city = ttk.Label(window, text=f"{city.get()}, {data['country']}", font=('Arial', 24, 'bold'))
combo_cities = ttk.Combobox(window, textvariable=city)
combo_cities['values'] = sorted(city_list)

label_lon = ttk.Label(window, text=f'{data['lon']:.2f}')
label_lat = ttk.Label(window, text=f'{data['lat']:.2f}')

label_weather_image = ttk.Label(window, image=weather_image)
label_test = ttk.Label(window, text=f"{data}")

# layout
label_datetime.pack()
label_city.pack()
combo_cities.pack()
label_lon.pack()
label_lat.pack()
label_test.pack()
label_weather_image.pack()

# events
combo_cities.bind('<<ComboboxSelected>>', update_labels)

# run
window.mainloop()