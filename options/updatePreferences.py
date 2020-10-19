import tkinter as tk
from tkinter import ttk
import getpass

# import methods
from options.webScrapingTab import webScrapingTab
from options.taggingTab import taggingTab
from options.namingTab import namingTab

#global variables
global tagList
global CONFIG

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"
#invalid selection color
invalid_bg = "#801212"

def updatePreferences(options, CONFIG_FILE, root):
    global tagList
    global CONFIG
    CONFIG = CONFIG_FILE
    window = tk.Toplevel(master=root)
    window.title("Preferences Window")
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (750 / 2)
    y = (hs / 2) - (385 / 2)
    window.geometry('%dx%d+%d+%d' % (750, 350, x, y))
    window.configure(bg=bg)
    tab_parent = ttk.Notebook(window)

    #Web Scraping Tab
    webScrapingTab(tab_parent, options, CONFIG_FILE)
    #Tagging Tab
    taggingTab(tab_parent, options, CONFIG_FILE)
    #Naming Tab
    namingTab(tab_parent, options, CONFIG_FILE)
    window.iconbitmap(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/favicon.ico")
    root.mainloop()

