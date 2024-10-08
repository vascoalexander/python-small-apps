# A small app that generates passwords of variable length (8-32 chars) out of a
# list of 92 chars. The user can copy the generated password to the clipboard.
# The main generator function (generate_pw) in pw_generator.py can also be used as
# standalone CLI script

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from pw_generator import generate_pw

def request_pw():
    """Enables the entry box, calls the generate_pw function and inserts the
    return into the entry box"""
    pw_entry.config(state="normal")
    pw_entry.delete(0,"end")
    pw_entry.config(fg="#00FF00")
    pw_length = pw_length_scale.get()
    pw_entry.insert(0,generate_pw(pw_length))

def copy_to_clipboard():
    """Copies the content of the entry box to the clipboard, warns the user if
    no password has been generated"""
    new_pw = pw_entry.get()
    if new_pw == "new password":
        messagebox.showwarning(title="PW Generator", message="Generate a password first")
    else:
        window.clipboard_clear()
        window.clipboard_append(new_pw)
        window.update()

window = ttk.Window(themename="vapor")
window.geometry("250x130")
window.resizable(False,False)

pw_entry = tk.Entry(window,width=150,font=("Consolas", 16,"italic"),justify=tk.CENTER)
pw_entry.insert(0,"new password")
pw_entry.configure(state="readonly")
pw_entry.pack()

length_label = tk.Label(window,text="Set the Password length (Default: 8)")
length_label.pack()

pw_length_scale = tk.Scale(window,from_=8,to=32,orient=tk.HORIZONTAL,tickinterval=4,
                           showvalue=1,resolution=4,length=300)
pw_length_scale.pack()

frame_buttons = tk.Frame(window)
frame_buttons.pack()

copy_to_cliboard_button = ttk.Button(frame_buttons,text="Copy to Clipboard", command=copy_to_clipboard)
copy_to_cliboard_button.pack(side="right",padx=5,pady=5)

generate_button = ttk.Button(frame_buttons, text="Generate", command=request_pw)
generate_button.pack(side="left",padx=5,pady=5)

window.mainloop()