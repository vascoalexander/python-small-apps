# Simple currency-converter that uses an api to get acutal conversion rates
# The user can input an amount and what currency to convert from / convert to
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
import requests
from urllib import parse

def currency_convert(event):
    """Gets actual currency data from api and converts a given amount of one
    currency to another"""
    api_url = 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/'
    entry_output.delete(0, tk.END)
    curr_from = currency_list_reversed[currency_from.get()]
    curr_to = currency_list_reversed[currency_to.get()]
    currency_url = parse.urljoin(api_url, curr_from) + '.json'
    api_response = requests.get(currency_url).json()[curr_from]

    try:
        if curr_to != 'btc' and curr_to != 'eth':
            converted_currency = str(f'{(api_response[curr_to] * int(abs(currency_amount.get()))):.2f}')
        else:
            converted_currency = str(f'{(api_response[curr_to] * int(abs(currency_amount.get()))):.5f}')

    except Exception as e:
        messagebox.showerror(title="Input Error", message=f"Input error: {e}. Enter a valid number.")

    entry_output.insert(0, converted_currency)

def update_label_input(event):
    """Update the label with a currency abbrevation matching the currency from
    the convert from combobox"""
    updated_label = currency_list_reversed[currency_from.get()]
    label_input.configure(text=updated_label)
    current_input = currency_amount.get()
    if current_input > 0:
        currency_convert(None)
    else:
        return

def update_label_output(event):
    """Update the Label with a currency abbrevation matching the currency form
    convert to combobox"""
    updated_label = currency_list_reversed[currency_to.get()]
    label_output.configure(text=updated_label)
    current_input = currency_amount.get()
    if current_input > 0:
        currency_convert(None)
    else:
        return
    
def change_amount(event):
    """Increase / Decrease amount to be converted with the mousewheel"""
    current = currency_amount.get()
    if event.delta > 0:
        current += 10
    else:
        if current > 0:
            current -= 10
    return currency_amount.set(current)

window = ttk.Window(themename="morph")
window.title("Currency Converter")
window.geometry("500x200")


currency_list = {'eur': 'Euro', 
                 'usd': "US Dollar", 
                 'btc': 'Bitcoin', 
                 'eth': 'Ethernum', 
                 'gbp': 'British Pound', 
                 'jpy': 'Japanese Yen', 
                 'rub': 'Russian Rubel', 
                 'trl': 'Turkish Lira', 
                 'xau': 'Gold Ounce'
}
currency_list_reversed = {value: key for key, value in currency_list.items()}

# widgets
frame_top = ttk.Frame(window)
frame_middle = ttk.Frame(window)
frame_bottom = ttk.Frame(window)

currency_from = tk.StringVar(value='Euro')
currency_to = tk.StringVar(value='US Dollar')
currency_amount = tk.IntVar(value=0)

# top
label_title = ttk.Label(
    frame_top, 
    text='Currency Converter', 
    font=('Arial', 24))

# middle
label_from = ttk.Label(
    frame_middle, 
    text='convert from', 
    font=('Arial', 14))
combobox_from = ttk.Combobox(
    frame_middle, 
    values=list(currency_list_reversed.keys()), 
    textvariable=currency_from, 
    state='readonly')
label_input = ttk.Label(
    frame_middle, 
    text='eur', 
    font=('Arial', 14))
entry_input = ttk.Entry(
    frame_middle, 
    textvariable=currency_amount, 
    justify='center')
label_to = ttk.Label(
    frame_middle, 
    text='convert to', 
    font=('Arial', 14))
combobox_to = ttk.Combobox(
    frame_middle, 
    values=list(currency_list_reversed.keys()), 
    textvariable=currency_to, 
    state='readonly')

# bottom
button_submit = ttk.Button(
    frame_bottom, 
    text='Submit', 
    command=lambda: currency_convert(None))
label_output = ttk.Label(
    frame_bottom, 
    text='usd', 
    font=('Arial', 14))
entry_output = ttk.Entry(
    frame_bottom, 
    bootstyle="info", 
    text='test', 
    justify='center')

# events
combobox_from.bind('<<ComboboxSelected>>', update_label_input)
combobox_to.bind('<<ComboboxSelected>>', update_label_output)
entry_input.bind('<Return>', currency_convert)
entry_input.bind('<MouseWheel>', change_amount)

# layout
frame_top.pack(pady=(8, 16))
frame_middle.pack()
frame_bottom.pack()

label_title.pack()

label_from.grid(row=0,column=0)
label_input.grid(row=0,column=1)
label_to.grid(row=0,column=2)

combobox_from.grid(row=1,column=0)
entry_input.grid(row=1,column=1, padx=8)
combobox_to.grid(row=1, column=2)

label_output.grid(row=0,column=0, columnspan=2)
button_submit.grid(row=1,column=0)
entry_output.grid(row=1,column=1)

# run
window.mainloop()
