import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

# import methods
from options.webScrapingTab import webScrapingTab
from options.taggingTab import taggingTab
from options.namingTab import namingTab
from options.comparisonTab import comparisonTab
from commonOperations import resource_path

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
    y = (hs / 2) - (407 / 2)
    window.geometry('%dx%d+%d+%d' % (750, 370, x, y))
    window.configure(bg=bg)
    tab_parent = ttk.Notebook(window)
    s = ttk.Style()
    try:
        s.theme_create("Track Management Utility", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": secondary_bg}},
        "TNotebook.Tab": {"configure": {"padding": [13, 5], "font": ('Proxima Nova Rg', '11'), "background": bg, 'foreground': 'white'}, }})
    except: pass
    s.theme_use("Track Management Utility")

    # web scraping tab
    webScrapingTab(tab_parent, options, CONFIG_FILE)
    # tagging tab
    taggingTab(tab_parent, options, CONFIG_FILE)
    # naming tab
    namingTab(tab_parent, options, CONFIG_FILE)
    # drive comparison tab
    comparisonTab(tab_parent, options, CONFIG_FILE)
    window.iconbitmap(resource_path('favicon.ico'))
    root.mainloop()

