# weather-app
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from timezonefinder import TimezoneFinder
import json, requests
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.request import urlopen
from PIL import ImageTk, Image
Image.CUBIC = Image.BICUBIC

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
    label_city.configure(text=f"{city.get()}, {data['country']}")
    label_datetime.configure(text=data['datetime'])
    label_temp.configure(text=f" | {data['temp']:.1f}°C")
    weather_image = get_weather_image(data)
    label_weather_image.configure(image=weather_image)
    label_weather_image.image = weather_image
    label_location.configure(text=f'lon: {data['lon']:.2f} lat: {data['lat']:.2f}')
    label_description.configure(text=f"Feels like {data['feels_like']:.1f}°C. {data['weather_desc'].capitalize()}")
    meter_temperature.configure(amountused=int(data['temp']))
    meter_pressure.configure(amountused=int(data['pressure']))
    meter_humidity.configure(amountused=int(data['humidity']))

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
window.geometry('570x370')
window.resizable(False,False)

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
frame_main = ttk.Frame(window)
frame_top = ttk.Frame(frame_main)
frame_title = ttk.Frame(frame_main)
frame_subtitle = ttk.Frame(frame_main)
frame_meter = ttk.Frame(frame_main)
frame_combo = ttk.Frame(frame_main)

# title
label_datetime = ttk.Label(
    frame_title, 
    text=data['datetime'], 
    font=('Arial', 10, 'bold'), 
    foreground='orange'
)
label_city = ttk.Label(
    frame_title, 
    text=f"{city.get()}, {data['country']}", 
    font=('Arial', 24, 'bold')
)
label_temp = ttk.Label(
    frame_title, 
    text=f" | {data['temp']:.1f}°C", 
    font=('Arial', 24)
)
label_location = ttk.Label(
    frame_subtitle, 
    text=f'lon: {data['lon']:.2f} lat: {data['lat']:.2f}', 
    font=('Arial', 9), 
    foreground='#B3B3B3'
)
label_description = ttk.Label(
    frame_subtitle, 
    text=f"Feels like {data['feels_like']:.1f}°C. {data['weather_desc'].capitalize()}", 
    font=('Arial', 12)
)

label_weather_image = ttk.Label(window, image=weather_image)

# meters
meter_temperature = ttk.Meter(
    frame_meter, 
    metersize=160, 
    subtext='Temperature', 
    bootstyle='danger', 
    textright='°C',
    subtextfont=('Arial', 12), 
    metertype='semi', 
    amountused=int(data['temp']), 
    amounttotal=50
)

meter_pressure = ttk.Meter(
    frame_meter, 
    metersize=160, 
    subtext='Pressure', 
    bootstyle='success', 
    textright='hPa',
    subtextfont=('Arial', 12), 
    metertype='semi', 
    amountused=int(data['pressure']), 
    amounttotal=2000
)

meter_humidity = ttk.Meter(
    frame_meter, 
    metersize=160, 
    subtext='Humidity',
    bootstyle='info',
    textright='%', 
    subtextfont=('Arial', 12), 
    metertype='semi', 
    amountused=int(data['humidity']), 
    amounttotal=100
)

# combobox
combo_cities = ttk.Combobox(frame_combo, textvariable=city)
combo_cities['values'] = sorted(city_list)

# layout
frame_main.pack(padx=20, pady=20)

# frame_top.pack(anchor='sw')
frame_title.pack(side='top', anchor='w', fill='x')
label_datetime.grid(row=0, column=0, sticky='sw')
label_city.grid(row=1, column=0, sticky='n')
label_temp.grid(row=1, column=1, sticky='n')
label_weather_image.place(x=440, y=20)

frame_subtitle.pack(side='top', anchor='nw')
label_location.grid(row=0, column=0, sticky='nw')
label_description.grid(row=1, column=0, columnspan=2, sticky='nw')

frame_meter.pack(pady=(12,16))
meter_temperature.grid(row=0, column=0)
meter_pressure.grid(row=0, column=1)
meter_humidity.grid(row=0, column=2)

frame_combo.pack()
combo_cities.pack()
# events
combo_cities.bind('<<ComboboxSelected>>', update_labels)
combo_cities.bind('<Return>', update_labels)

# run
window.mainloop()