# A simple text editor with a dark and a light mode toggle and a font-size 
# slider. Files can be loaded and saved via menubar
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import messagebox

filepath = ""

def load_file():
    """Load a file and display its contents in the text-area"""
    global filepath
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        try:
            with open(filepath, 'r', encoding='UTF-8') as file:
                content = file.read()
                text_area.delete("1.0", tk.END)
                text_area.insert(tk.INSERT, content)
            window.title(f"Text Editor - {filepath}")
        except UnicodeDecodeError:
            messagebox.showerror(title="Decoding Error", message="Error decoding the file. Make sure the loaded file is in UTF-8 encoding.")
        except Exception as e:
            messagebox.showerror(title="Error", message=f"An Error reading the file occured: {e}")

def save_as():
    """Save current content of the text area via filedialog"""
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    try:
        with open(filepath, 'w', encoding='UTF-8') as file:
            content = text_area.get('1.0', tk.END)
            file.write(content)
            messagebox.showinfo(title="File Dialog", message="File successfully saved!")
    except Exception as e:
        messagebox.showerror(title="File Save Error", message=f"An error occured saving the file: {e}")

def save_file():
    """Save content of text area to current opened file. If no file has been
    opened a filedialog opens"""
    global filepath
    if not filepath:
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        try:
            with open(filepath, 'w', encoding='UTF-8') as file:
                content = text_area.get('1.0', tk.END)
                file.write(content)
                messagebox.showinfo(title="File Dialog", message="File successfully saved!")
        except Exception as e:
            messagebox.showerror(title="File Save Error", message=f"An error occured saving the file: {e}")
    

def set_mode():
    """Switches the visual mode of the app from dark to light and vice versa"""
    if toggle_state.get():
        ttk.Style(theme="sandstone")
        label_dark.config(image=dark_image)
        label_light.config(image=light_image)
        file_menu.entryconfig(0, image=open_image)
        file_menu.entryconfig(1, image=save_image)
        file_menu.entryconfig(2, image=save_as_image)
        file_menu.entryconfig(4, image=exit_image)
    else:
        ttk.Style(theme="darkly")
        label_dark.config(image=dark_image_light)
        label_light.config(image=light_image_light)
        file_menu.entryconfig(0, image=open_image_light)
        file_menu.entryconfig(1, image=save_image_light)
        file_menu.entryconfig(2, image=save_as_image_light)
        file_menu.entryconfig(4, image=exit_image_light)

def update_fontsize(size):
    """Change the fontsize in the text area"""
    size = int(float(size))
    text_area.config(font=("Arial", size))
    label_font_size.config(text=size)

window = ttk.Window(themename="darkly")
window.title("Text Editor")
window.geometry("800x600")

open_image = ttk.PhotoImage(file="./text-editor/icons/folder-open.png")
save_image = ttk.PhotoImage(file="./text-editor/icons/disk.png")
save_as_image = ttk.PhotoImage(file="./text-editor/icons/save-as.png")
exit_image = ttk.PhotoImage(file="./text-editor/icons/leave.png")
dark_image = ttk.PhotoImage(file="./text-editor/icons/dark-mode.png")
light_image = ttk.PhotoImage(file="./text-editor/icons/light-mode.png")

open_image_light = ttk.PhotoImage(file="./text-editor/icons/folder-open_light.png")
save_image_light = ttk.PhotoImage(file="./text-editor/icons/disk_light.png")
save_as_image_light = ttk.PhotoImage(file="./text-editor/icons/save-as_light.png")
exit_image_light = ttk.PhotoImage(file="./text-editor/icons/leave_light.png")
dark_image_light = ttk.PhotoImage(file="./text-editor/icons/dark-mode_light.png")
light_image_light = ttk.PhotoImage(file="./text-editor/icons/light-mode_light.png")

#======================= toggle mode feature ========================#
frame_modes = ttk.Frame(window, width=100, height=20)
frame_modes.pack(side="top",padx=2,pady=(6,0))

toggle_state = tk.BooleanVar()

label_dark = ttk.Label(master=frame_modes, image=dark_image_light)
label_dark.grid(row=0,column=0)
button_toggle = ttk.Checkbutton(master=frame_modes, bootstyle="light-round-toggle", command=set_mode, variable=toggle_state)
button_toggle.grid(row=0, column=1, padx=(7,4))
label_light = ttk.Label(master=frame_modes, image=light_image_light)
label_light.grid(row=0,column=2)

#============================ menubar ==============================#
menubar = ttk.Menu(window)
window.config(menu=menubar)

file_menu = ttk.Menu(menubar, tearoff=0, font=("Arial", 12))
menubar.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label=" Open", image=open_image_light, compound="left", command=load_file)
file_menu.add_command(label=" Save", image=save_image_light, compound="left", command=save_file)
file_menu.add_command(label=" Save As", image=save_as_image_light, compound="left", command=save_as)
file_menu.add_separator()
file_menu.add_command(label=" Exit", image=exit_image_light, compound="left", command=quit)

#================== main text area with scrollbar ==================#
frame_main = ttk.Frame(window)

scrollbar = ttk.Scrollbar(frame_main, orient='vertical',bootstyle="info-round")
scrollbar.pack(side="right", fill='y', pady=10, padx=(0,8))

text_area = ttk.Text(frame_main, bg="white", fg="dark gray", font=("Arial", 12), yscrollcommand=scrollbar.set)
text_area.pack(side="bottom", padx=8, pady=8, expand=True, fill="both")

scrollbar.config(command=text_area.yview)

#======================== font-size-slider ==========================#
frame_bottom = ttk.Frame(window, width=200, height=20)
frame_bottom.pack(side="bottom")

label_font_size = tk.Label(frame_bottom, text="12", font=("Arial", 8), compound="left")
label_font_size.grid(row=0,column=1, padx=5)

font_scale = ttk.Scale(
    frame_bottom, 
    from_=8, 
    to=24, 
    length=150, 
    orient=ttk.HORIZONTAL,
    command=update_fontsize,)

font_scale.set(12)
font_scale.grid(row=0, column=0)

frame_main.pack(expand=True, fill="both")

window.mainloop()