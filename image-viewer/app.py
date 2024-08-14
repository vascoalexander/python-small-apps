# image-viewer
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import os

def view_image():
    pass

def filedialog():
    pass

def find_images():
    for file in os.listdir(image_dir):
        if any(file.lower().endswith(ext) for ext in image_ext):
            image_files.append(file)
    return image_files

window = ttk.Window(themename="darkly")
window.title("Tk Image Viewer")
window.geometry("800x600")

image_dir = "./image-viewer/img/"
image_ext = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp']
image_files = []

frame_display = ttk.Frame(window, width=800, height=450)
frame_display.pack(expand=True, fill="both")

button_filedir = ttk.Button(frame_display, text="Open folder", command=filedialog)
button_filedir.pack(expand=True)

frame_images = ttk.Frame(window,width=800, height=150)
frame_images.pack(side="bottom", fill="both")

placeholder_slides_path = os.path.join(image_dir,"placeholder_120x120.png")

for i in range(7):
    image = tk.PhotoImage(file=placeholder_slides_path)
    image_files.append(image)
    tk.Label(frame_images,image=image).pack(side="left")

##for file in os.listdir(image_dir):
##    image_path = os.path.join(image_dir, file)
##    image = tk.PhotoImage(file=image_path)
##    if "120x120" in image_path:
##        image_files.append(image)
##        tk.Label(frame_images,image=image).pack(side="left")
        

window.mainloop()