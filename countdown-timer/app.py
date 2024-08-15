# A countdown Timer app with a stop and pause function. countdown_timer() is
# the main function that controls the value of the timer. This function is controlled
# by the window attribute is_paused. The value of the timer is also handled as a
# window attribute (window.time_in_seconds)

import tkinter as tk

def countdown_timer():
    """The functions gets the time_in_seconds from the window attribute, converts
    it to a string and configures the label to use this string. The funcion is called
    every second by window.after() to actualize the string"""
    if window.is_paused:
        return
    
    time_in_seconds = getattr(window,"time_in_seconds", None)
    if time_in_seconds is not None and time_in_seconds > 0:
        seconds = time_in_seconds % 60
        minutes = int(time_in_seconds / 60) % 60
        hours = int(time_in_seconds / 3600)
        label_time.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")
        window.time_in_seconds -= 1
        window.after(1000,countdown_timer)
    else:
        label_time.configure(text="00:00:00")

def set_timer():
    """Creates a new child window with an entry field and a submit button. When
    the Button is pressed the submit_time function is called and countdown_time, and
    the window itself are passed over to that function"""
    set_timer_window = tk.Toplevel(window)
    set_timer_window.geometry("220x100")
    set_timer_window.resizable(False,False)

    countdown_time = tk.IntVar()
    set_timer_label = tk.Label(set_timer_window,text="Enter time in seconds: ",
                               font=("Arial",16))
    set_timer_label.pack()
    set_timer_entry = tk.Entry(set_timer_window, justify="center",font=("Arial",24),
                               textvariable=countdown_time)
    set_timer_entry.pack()
    submit_button = tk.Button(set_timer_window, text="Submit", 
                              command=lambda: submit_time(countdown_time,set_timer_window))
    submit_button.pack()

def submit_time(countdown_time,set_timer_window):
    """Gets the countdown_time and the child window from set_timer and sets
    the label of the main window to the entered timer value. Closes the dialog
    window afterwards"""
    time_in_seconds = countdown_time.get()
    seconds = time_in_seconds % 60
    minutes = int(time_in_seconds / 60) % 60
    hours = int(time_in_seconds / 3600)

    label_time.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")
    window.time_in_seconds = time_in_seconds
    window.is_paused = False
    set_timer_window.destroy()

def start_timer():
    """Starts the timer"""
    window.is_paused = False
    countdown_timer()

def pause_timer():
    """Pauses the timer"""
    window.is_paused = True

def clear_timer():
    """Clears the timer. Resets Label"""
    window.time_in_seconds = 0
    label_time.configure(text="00:00:00")
    window.is_paused = False

window = tk.Tk()
window.geometry("320x120")
window.title("Countdown-Timer")
window.configure(bg="black")

window.time_in_seconds = 0
window.is_paused = False

play_icon = tk.PhotoImage(file="./countdown-timer/icons/play.png")
pause_icon = tk.PhotoImage(file="./countdown-timer/icons/pause.png")
stop_icon = tk.PhotoImage(file="./countdown-timer/icons/stop.png")

label_time = tk.Label(window, bg="black", fg="#00FF00", text="00:00:00",
                      font=("Arial",48, "bold"))
label_time.pack()

frame_buttons = tk.Frame(window, bg="black")
frame_buttons.pack(side="bottom")

set_time_button = tk.Button(frame_buttons,text="Set Timer",command=set_timer,font=("Arial",16))
set_time_button.pack(side="left",padx=5,pady=5)

start_time_button = tk.Button(frame_buttons,image=play_icon,command=start_timer)
start_time_button.pack(side="right",padx=5,pady=5)

pause_time_button = tk.Button(frame_buttons,image=pause_icon,command=pause_timer)
pause_time_button.pack(side="right",padx=5,pady=5)

clear_time_button = tk.Button(frame_buttons,image=stop_icon,command=clear_timer)
clear_time_button.pack(side="right",padx=5,pady=5)

window.mainloop()