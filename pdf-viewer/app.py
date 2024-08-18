# a simple pdf-reader using the pymupdf library. loads and displays the content
# of a pdf. can go to pages by button, scrollwheel or entering a number into
# an entrybox
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as ttk
from pathlib import Path
import pymupdf
from PIL import Image, ImageTk

def open_file():
    """Open a pdf file and display the first page"""
    global doc
    filepath = filedialog.askopenfile(
        initialdir=f"{Path.home()}/Documents", 
        defaultextension=".pdf", 
        filetypes=[("PDF-Documents", ".pdf"), ("All files", ".")]
    )
    doc = pymupdf.open(filepath)
    label_page_count.configure(text=f"/ {doc.page_count}")
    display_page(0)

def display_page(page):
    """Display the given page of a pdf file"""
    page = doc[page]
    pix = page.get_pixmap()
    mode = "RGBA" if pix.alpha else "RGB"
    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
    tkimg = ImageTk.PhotoImage(img)

    if hasattr(window, 'label_page'):
        window.label_page.config(image=tkimg)
        window.label_page.image = tkimg
    else:
        window.label_page = tk.Label(window, image=tkimg)
        window.label_page.image = tkimg
        window.label_page.pack(side="top", fill=tk.BOTH, expand=True)

def next_page():
    """Display the next page"""
    global page_number
    current_page = page_number.get()
    if doc and current_page < (doc.page_count -1):
        display_page(current_page +1)
        page_number.set(current_page +1)
    pass

def prev_page():
    """Display the previous page"""
    global page_number
    current_page = page_number.get()
    if doc and current_page > 0:
        display_page(current_page -1)
        page_number.set(current_page -1)

def go_to_page(event):
    """Get the entry value on a return-pressed event and display this page"""
    page_to_go = page_number.get()
    if page_to_go < 0 or page_to_go > doc.page_count:
        messagebox.showerror(title="PDF Viewer Error", message="The page does not exist")
    else:
        display_page(page_to_go)

window = ttk.Window()
window.geometry("800x950")
window.title("PDF Viewer")
doc = []

image_next = tk.PhotoImage(file='./pdf-viewer/icons/next.png')
image_prev = tk.PhotoImage(file='./pdf-viewer/icons/prev.png')

# widgets
frame_bottom = ttk.Frame(window)
frame_top = ttk.Frame(window, width=200, height=24)

page_number = tk.IntVar(value=0)
entry_page = tk.Entry(frame_top, textvariable=page_number, width=6, justify="center")

page_count = tk.StringVar(value=0)
label_page_count = tk.Label(frame_top, text="/ 0")

button_open = tk.Button(
    frame_bottom, 
    text="Open Folder", 
    font=("Arial", 14),
    command=open_file, 
    bg="#474747", 
    fg="white"
)

button_next = ttk.Button(
    window, 
    image=image_next, 
    command=next_page, 
    bootstyle='secondary-outline', 
    takefocus=False
)

button_prev = ttk.Button(
    window, 
    image=image_prev, 
    command=prev_page, 
    bootstyle='secondary-outline', 
    takefocus=False
)

#layout
frame_top.pack(side="top")
entry_page.pack(side="left", padx=2)
label_page_count.pack(side="right")
button_prev.pack(side="left")
button_next.pack(side="right")

frame_bottom.pack(side="bottom", anchor="center", pady=5)
button_open.pack()

# events
window.bind("<MouseWheel>", lambda event: prev_page() if event.delta > 0 else next_page())
entry_page.bind("<Return>", go_to_page)

# run
window.mainloop()