# stopwatch
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

def timer():

    if window.is_paused:
        return

    time_in_seconds = getattr(window,"time_in_seconds", None)
    if time_in_seconds is not None:
        seconds = int(time_in_seconds) % 60
        minutes = int(time_in_seconds / 60) % 60
        hours = int(time_in_seconds / 3600)
        milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
        label_time.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")
        label_milliseconds.configure(text=f"Milliseconds {milliseconds:03}")
        window.time_in_seconds += 0.001
        window.after(1,timer)

def start():
    window.is_paused = False
    timer()

def pause():
    window.is_paused = True

def stop():
    window.time_in_seconds = 0
    label_time.configure(text="00:00:00")
    label_milliseconds.configure(text=f"ms 000")
    window.is_paused = True

window = tk.Tk()
window.geometry("320x160")
window.configure(bg="black")
window.title("Stopwatch")

window.is_paused = False
window.time_in_seconds = 0

play_icon = tk.PhotoImage(file="./countdown-timer/icons/play.png")
pause_icon = tk.PhotoImage(file="./countdown-timer/icons/pause.png")
stop_icon = tk.PhotoImage(file="./countdown-timer/icons/stop.png")

label_time = tk.Label(window, bg="black", fg="#00FF00", text="00:00:00",
                      font=("Arial",48, "bold"))
label_time.pack()
label_milliseconds = tk.Label(window, bg="black", fg="#00FF00", text="Milliseconds 000",
                      font=("Arial",16, "bold"))
label_milliseconds.pack()

frame_buttons = tk.Frame(window, bg="black")
frame_buttons.pack()


start_time_button = tk.Button(frame_buttons,image=play_icon,command=start)
start_time_button.pack(side="right",padx=5,pady=5)

pause_time_button = tk.Button(frame_buttons,image=pause_icon,command=pause)
pause_time_button.pack(side="right",padx=5,pady=5)

clear_time_button = tk.Button(frame_buttons,image=stop_icon,command=stop)
clear_time_button.pack(side="right",padx=5,pady=5)

window.mainloop()