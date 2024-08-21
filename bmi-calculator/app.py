# bmi-calculator
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk

def calculate_bmi():
    try:
        if float(entry_weight.get()) == 0:
            messagebox.showwarning(title='Invalid Input', message='Please enter a valid number')
        elif float(entry_height.get()) == 0:
            messagebox.showwarning(title='Invalid Input', message='Please enter a valid number')
        else:
            height = abs(float(entry_height.get())) / 100
            weight = abs(float(entry_weight.get()))
            bmi = round(weight / (height**2), 1)
            label_result.configure(text=bmi)
            label_category.configure(text=bmi_category(bmi)[0], foreground=bmi_category(bmi)[1])

    except ValueError:
        reset()
        messagebox.showerror(title='Invalid Input', message='Pleas enter a valid number')

def reset():
    entry_height.delete(0, tk.END)
    entry_height.insert(0, 0)
    entry_weight.delete(0, tk.END)
    entry_weight.insert(0, 0)
    label_result.configure(text=0.0)
    label_category.configure(text='None', foreground='white')

def bmi_category(bmi):
    if bmi < 16.0:
        bmi_category = "Underweight (Severe thinness)"
        color = 'darkblue'
    elif 16.0 < bmi < 16.9:
        bmi_category = "Underweight (Moderate thinness)"
        color = 'blue'
    elif 17.0 < bmi < 18.4:
        bmi_category = "Underweight (Mild thinness)"
        color = 'lightblue'
    elif 18.5 < bmi < 24.9:
        bmi_category = "Normal range"
        color = 'green'
    elif 25.0 < bmi < 29.9:
        bmi_category = "Overweight (Pre-obese)"
        color = 'yellow'
    elif 30.0 < bmi < 34.9:
        bmi_category = "Obese (Class I)"
        color = 'orange'
    elif 35.0 < bmi < 39.9:
        bmi_category = "Obese (Class II)"
        color = 'red'
    elif bmi >= 40.0:
        bmi_category = "Obese (Class III)"
        color = 'darkred'
    return bmi_category, color

def entry_focus_out(event):
    if entry_height.get() == '':
        entry_height.insert(0, 0)
    if entry_weight.get() == '':
        entry_weight.insert(0, 0)

# setup
window = ttk.Window(themename='darkly')
window.title('BMI-Calculator')
window.geometry('400x230')

weight = tk.DoubleVar(value=0)
height = tk.DoubleVar(value=0)

# widgets
frame_top = ttk.Frame(window)
frame_bottom = ttk.Frame(window)

label_title = ttk.Label(window, text='BMI-Calculator', font=('Arial', 20, 'bold'), foreground='pink')
label_height = ttk.Label(frame_top, text='Height (cm)', font=('Arial', 14))
label_weight = ttk.Label(frame_top, text='Weight (kg)', font=('Arial', 14))
entry_weight = ttk.Entry(frame_top, justify='center', textvariable=weight)
entry_height = ttk.Entry(frame_top, justify='center', textvariable=height)
button_submit = ttk.Button(frame_top, text='Submit', command=calculate_bmi)
button_reset = ttk.Button(frame_top, text='Reset', command=reset)
label_bmi = ttk.Label(frame_bottom, text=f'Your BMI: ', font=('Arial', 12))
label_result = ttk.Label(frame_bottom, text=0.0, font=('Arial', 12, 'bold'))
label_category_text = ttk.Label(frame_bottom, text=f"According to the WHO Definition your BMI-Category is: ")
label_category = ttk.Label(frame_bottom, text='None', font=('Arial',12, "bold"))

# layout
label_title.pack(pady=(5, 10))

frame_top.pack(pady=(0,8))
label_weight.grid(row=0, column=0)
label_height.grid(row=0, column=1)
entry_height.grid(row=1, column=1)
entry_weight.grid(row=1, column=0)
button_submit.grid(row=2, column=0, pady=(8,0), padx=(0,4), sticky='e')
button_reset.grid(row=2, column=1, pady=(8,0), padx=(4,0), sticky='w')

frame_bottom.pack(pady=(0,8))
label_bmi.grid(row=0,column=0, padx=(0,5), sticky='e')
label_result.grid(row=0, column=1, sticky='w')
label_category_text.grid(row=1,columnspan=2)
label_category.grid(row=2, column=0, columnspan=2)

# events
entry_height.bind('<FocusIn>', lambda event: entry_height.delete(0, tk.END))
entry_height.bind('<FocusOut>', entry_focus_out)
entry_weight.bind('<FocusIn>', lambda event: entry_weight.delete(0, tk.END))
entry_weight.bind('<FocusOut>', entry_focus_out)

# run
window.mainloop()