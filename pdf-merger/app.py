# Small app to merge pdf Files with a GUI. The User can specify a path for the
# files to be merged and provide a filename for the output file. There is some
# logic to catch invalid path, no pdf files in path and a default fallback if
# no filename is specified. The merger script can be run as standalone from a
# terminal

import tkinter as tk
from merger import merge_pdf
import ttkbootstrap as ttk

def on_entry_click(event):
    """Deletes the Placeholder Text, changes font to green normal and
    shows a blinking cursor"""
    widget = event.widget
    if widget.get() == "Enter path" or widget.get() == "Output filename":
        widget.delete(0,"end")
        widget.config(fg="#00FF00", font=("Arial",12))
    widget.config(insertbackground="#00FF00")

def on_focus_out(event):
    """Sets the Entry back to default"""
    widget = event.widget
    if widget.get() == "":
        if widget == entry_path:
            widget.insert(0,"Enter path")
        elif widget == entry_filename:
            widget.insert(0,"Output filename")
        widget.config(fg="gray", font=("Arial",12,"italic"))

def merge_request():
    """Calls main function from merger.py. Simple checks if a filename is
    provided. If not defaults to main function behavior"""
    path = entry_path.get()
    filename = entry_filename.get()
    if filename == "Output filename" or filename == "":
        merge_pdf(path)
    else:
        merge_pdf(path,filename)

window = ttk.Window(themename="darkly",title="PDF Merger")
window.geometry("300x180")

label_title = tk.Label(window,text="PDF Merger",font=("Arial",20,"bold"))
label_title.pack()

entry_path = tk.Entry(window,font=("Arial",12, "italic"),fg="gray",bg="black",width=300,
                      justify=tk.CENTER)
entry_path.insert(0,"Enter path")
entry_path.bind('<FocusIn>', on_entry_click)
entry_path.bind('<FocusOut>', on_focus_out)
entry_path.pack()

label_path = tk.Label(window,fg="gray",font=("Arial",12,"italic"),
                      text="path to your file",pady=5)
label_path.pack()

entry_filename = tk.Entry(window,font=("Arial",12, "italic"),fg="gray",bg="black",width=300,
                          justify=tk.CENTER)
entry_filename.insert(0,"Output filename")
entry_filename.bind('<FocusIn>', on_entry_click)
entry_filename.bind('<FocusOut>', on_focus_out)
entry_filename.pack()

label_filename = tk.Label(window,fg="gray",font=("Arial",12,"italic"),
                      text="name of the merged pdf-file",pady=5)
label_filename.pack()

merge_button = tk.Button(window,text="Merge Files",command=merge_request)
merge_button.pack()

window.mainloop()