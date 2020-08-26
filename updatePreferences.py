from tkinter import *
from tkinter import ttk

def updatePreferences():
    window = Tk()
    window.title("Preferences Window")
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (500 / 2)
    y = (hs / 2) - (400 / 2)
    window.geometry('%dx%d+%d+%d' % (500, 300, x, y))
    tab_parent = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_parent)
    tab2 = ttk.Frame(tab_parent)
    tab_parent.add(tab1, text="Web Scrape Settings")
    tab_parent.add(tab2, text="Lorem Ipsum")
    tab_parent.pack(expand=1, fill='both')