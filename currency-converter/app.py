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

def update_label_from(event):
    selected_currency = currency_from.get()
    label_from.configure(text=currency_list[selected_currency])

def update_label_to(event):
    selected_currency = currency_to.get()
    label_to.configure(text=currency_list[selected_currency])

window = ttk.Window(themename="flatly")
window.title("Currency Converter")
window.geometry("600x400")

currencies = requests.get('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json').json()
currency_list = {value: key for key, value in currencies.items()}

# widgets
currency_from = tk.StringVar(value='Euro')
currency_to = tk.StringVar(value='US Dollar')
combobox_from = ttk.Combobox(window, values=list(currency_list.keys()), textvariable=currency_from)
combobox_to = ttk.Combobox(window, values=list(currency_list.keys()), textvariable=currency_to)

label_from = ttk.Label(window)
label_to = ttk.Label(window)

# events
combobox_from.bind("<<ComboboxSelected>>", update_label_from)
combobox_from.bind("<Return>", update_label_from)
combobox_to.bind("<<ComboboxSelected>>", update_label_to)
combobox_to.bind("<Return>", update_label_to)

# layout
combobox_from.pack()
combobox_to.pack()
label_from.pack()
label_to.pack()

# run
window.mainloop()
