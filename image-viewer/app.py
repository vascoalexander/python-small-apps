# image-viewer
import tkinter as tk
from tkinter import ttk, filedialog
import ttkbootstrap as ttk
import os
from pathlib import Path

def view_image(image_file):
    if window.image_files:
        button_filedir.pack_forget()
        label = tk.Label(window, image=image_file).pack(side="top")
        create_close_button()
        pass

def next_image():
    pass
def prev_image():
    pass

def open_dir():
    filepath = filedialog.askdirectory(initialdir=Path.home(), title="Open Folder") 
    for file in os.listdir(filepath):
        if any(file.lower().endswith(ext) for ext in image_ext):
            image_path = os.path.join(filepath, file)
            image = tk.PhotoImage(file=image_path)
            window.image_files.append(image)
    print(window.image_files)
    view_image(window.image_files[0])

def close_dir():
    window.image_files = []
    create_close_button()


def create_close_button():
    if button_closedir.winfo_ismapped():
        button_closedir.pack_forget()
        button_filedir.pack(expand=True)
    else:
        button_filedir.pack_forget()
        button_closedir.pack(side="bottom")

# def find_images():
#     for file in os.listdir(image_dir):
#         if any(file.lower().endswith(ext) for ext in image_ext):
#             window.image_files.append(file)
#     return window.image_files

def open_file():
    pass

window = ttk.Window(themename="darkly")
window.title("Tk Image Viewer")
window.geometry("800x600")

window.image_files = []
image_ext = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp']

# frame_display = ttk.Frame(window, width=800, height=450)
# frame_display.pack(expand=True, fill="both")

#placeholder_slides_path = os.path.join(image_dir,"placeholder_120x120.png")

#for i in range(7):
#    image = tk.PhotoImage(file=placeholder_slides_path)
#    image_files.append(image)
#    tk.Label(frame_display,image=image).pack(side="left")

button_filedir = ttk.Button(window, text="Open folder", command=open_dir)
button_filedir.pack(expand=True)
button_closedir = ttk.Button(window, text="Close", command=close_dir)

print(window.image_files)


##for file in os.listdir(image_dir):
##    image_path = os.path.join(image_dir, file)
##    image = tk.PhotoImage(file=image_path)
##    if "120x120" in image_path:
##        image_files.append(image)
##        tk.Label(frame_images,image=image).pack(side="left")
        

window.mainloop()