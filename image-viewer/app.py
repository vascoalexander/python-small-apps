# image-viewer
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import os
from PIL import Image, ImageTk

def load_images():
    """Load a list of images in the given path that have an extension defined
    in the image_ext List"""
    window.images = []
    directory = filedialog.askdirectory(initialdir=Path.home())
    # Checking if the dialog is canceld
    if directory:

        path = os.path.abspath(directory)
        for file in os.listdir(path):
            if file.lower().endswith(image_ext):
                image_path = os.path.join(path,file)
                image = Image.open(image_path)
                window.images.append(image)

        if window.images:
            display_image(0)
        else:
            messagebox.showinfo(
                title="Image Viewer", 
                message=f"No displayable images in the folder!")          
    else:
        return

def display_image(index):
    """Create a Label to display an image from a List of Images with the given
    Index"""
    global current_image
    current_image = window.images[index]
    resized_image = resize_proportionally(current_image)
    photo = ImageTk.PhotoImage(resized_image)

    if hasattr(window, 'label_image'):
        window.label_image.config(image=photo)
        window.label_image.image = photo
    else:
        window.label_image = tk.Label(window, image=photo, bg="#2b2b2b")
        window.label_image.image = photo
        window.label_image.pack(side="top", fill=tk.BOTH, expand=True)
    

def resize_proportionally(image):
    """Resize the image proportionally to fit in a fixed size of 800x600"""
    original_width, original_height = image.size
    if original_width > original_height:
        aspect_ratio = original_height / original_width
        target_height = int(800 * aspect_ratio)
        resized_image = image.resize((800, target_height), Image.Resampling.LANCZOS)
    elif original_height > original_width:
        aspect_ratio = original_width / original_height
        target_width = int(600 * aspect_ratio)
        resized_image = image.resize((target_width, 600), Image.Resampling.LANCZOS)
    else:
        resized_image = image.resize((600, 600), Image.Resampling.LANCZOS)
    
    return resized_image

def next_image():
    """Display the next image in the List"""
    if window.images:
        current_index = window.images.index(current_image)
        if current_index < len(window.images) - 1:
            display_image(current_index+1)
    else:
        return

def prev_image():
    """Display previous image in the List"""
    if window.images:
        current_index = window.images.index(current_image)
        if current_index > 0:
            display_image(current_index-1)
    else:
        return

window = tk.Tk()
window.geometry("850x650")
window.title("Image Viewer")
window.config(background="#2b2b2b")

window.images = []
image_ext = (".jpeg", ".jpg", ".png", ".gif", ".bmp", ".webp")

image_next = tk.PhotoImage(file='./image-viewer/icons/next.png')
image_prev = tk.PhotoImage(file='./image-viewer/icons/prev.png')

# widgets
frame_bottom = tk.Frame(window, bg="#2b2b2b")

button_open = tk.Button(
    frame_bottom, 
    text="Open Folder", 
    font=("Arial", 14),
    command=load_images, 
    bg="#474747", 
    fg="white",
    borderwidth=0
)

button_next = tk.Button(
    window, 
    image=image_next, 
    command=next_image, 
    bg="#2b2b2b", 
    borderwidth=0,
    highlightthickness=0,
    activebackground="#2b2b2b",
    takefocus=False
)

button_prev = tk.Button(
    window, 
    image=image_prev, 
    command=prev_image, 
    bg="#2b2b2b", 
    borderwidth=0,
    highlightthickness=0,
    activebackground="#2b2b2b",
    takefocus=False
)

# layout
button_prev.pack(side="left")
button_next.pack(side="right")
frame_bottom.pack(side="bottom", anchor="center")
button_open.pack(side="bottom", padx=5,pady=5)

# run
window.mainloop()