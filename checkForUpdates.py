from tkinter import *

def checkForUpdates():
    window = Toplevel()
    window.title("Updates")
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (400 / 2)
    y = (hs / 2) - (280 / 2)
    window.geometry('%dx%d+%d+%d' % (400, 180, x, y))
    window.columnconfigure(1,weight=1)
    window.rowconfigure(1, weight=1)
    Label(window, text="No new updates found").grid(row=1, column=1, pady=(30,10))
    Label(window, text="Track Management Utility is developed by Brendan Chou\n(Like Brandon, but mispelled)", font=("TkDefaultFont", 8)).grid(row=2, column=1, pady=(0,10))
