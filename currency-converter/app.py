# currency-converter
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import requests
import json
from urllib import parse

api_url = 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/'

def currency_convert(curr_from, curr_to, amount):
    currency_url = parse.urljoin(api_url, curr_from) + '.json'
    api_response = requests.get(currency_url).json()[curr_from]
    converted_currency = api_response[curr_to] * amount 
    return converted_currency

window = ttk.Window(themename="flatly")
window.title("Currency Converter")
window.geometry("600x400")

currencies = ['eur', 'usd', 'frf', 'gbp', 'trl', 'rub', 'cny', 'aud', 'jpy', 
              'chf','btc', 'eth', 'usdt', 'xau']
currency_list = requests.get('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json').json()

currencies_fullname = []
for item in currencies:
    full_name = currency_list[item]
    currencies_fullname.append(full_name)

# widget
currency = tk.StringVar(value=currencies_fullname[0])
combobox = ttk.Combobox(window, textvariable=currency)
combobox['values'] = currencies_fullname

entry_amount = ttk.Entry(window)

label_currency = ttk.Label(window, textvariable=currency)
# layout
combobox.pack()
entry_amount.pack()
label_currency.pack()

# run
window.mainloop()
