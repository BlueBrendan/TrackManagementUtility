
import tkinter as tk

#global variables
overwrite = False

def handleReplayGain(oldRGvalue, newRGvalue, webScrapingWindow):
    global overwrite
    window = tk.Toplevel()
    window.title("ReplayGain Conflict")
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (400 / 2)
    y = (hs / 2) - (132 / 2)
    window.geometry('%dx%d+%d+%d' % (400, 120, x, y))
    tk.Label(window, text="Existing ReplayGain value detected. Replace " + str(oldRGvalue) + " with " + str(newRGvalue) + " dB?", wraplength=370).pack(side="top", pady=(20,15))
    buttons = tk.Frame(window)
    buttons.pack(side="top")
    tk.Button(buttons, text="Yes", command=lambda: setTrue(window, webScrapingWindow)).pack(side="left", padx=(15, 20), pady=(10, 0))
    tk.Button(buttons, text="No", command=lambda: closePopup(window, webScrapingWindow)).pack(side="left", padx=(20, 15), pady=(10, 0))
    window.wait_window()
    if overwrite:
        return "overwrite"

def setTrue(window, webScrapingWindow):
    global overwrite
    overwrite = True
    window.destroy()
    webScrapingWindow.lift()

def closePopup(window, webScrapingWindow):
    window.destroy()
    webScrapingWindow.lift()