# text-editor
import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk

def save_file():
    text = ""
    with open('test.txt', 'a') as file:
        file.write(text)

def copy_file():
    pass

def load_file():
    try:
        with open('test.txt') as fobj:
            print(fobj.read())
    except FileNotFoundError:
        print("File not found!")

def set_mode():
    pass

window = tk.Tk()
window.title("Text Editor")
window.geometry("800x600")

button_toggle = ttk.Checkbutton(bootstyle="dark-round-toggle", command=set_mode)
button_toggle.pack(side="top")

menubar = tk.Menu(window)
window.config(menu=menubar)

open_image = tk.PhotoImage(file="./text-editor/icons/folder-open.png")
save_image = tk.PhotoImage(file="./text-editor/icons/disk.png")
exit_image = tk.PhotoImage(file="./text-editor/icons/leave.png")

file_menu = tk.Menu(menubar, tearoff=0, font=("Arial", 14))
menubar.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")
file_menu.add_command(label="Save As")
file_menu.add_separator()
file_menu.add_command(label="Exit")



window.mainloop()