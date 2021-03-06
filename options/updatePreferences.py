import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

# import methods
from options.webScrapingTab import webScrapingTab
from options.taggingTab import taggingTab
from options.namingTab import namingTab
from options.comparisonTab import comparisonTab
from commonOperations import resource_path

# global variables

bg = "#282f3b" # main bg color
secondary_bg = "#364153" # secondary color
invalid_bg = "#801212" # invalid selection color

def updatePreferences(options, CONFIG_FILE, root):
    window = tk.Toplevel(master=root)
    window.title("Preferences Window")
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (780 / 2)
    y = (hs / 2) - (407 / 2)
    window.geometry('%dx%d+%d+%d' % (780, 370, x, y))
    window.configure(bg=bg)
    tab_parent = ttk.Notebook(window)
    s = ttk.Style()
    try:
        s.theme_create("Track Management Utility", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": secondary_bg, 'borderwidth': 0}},
        "TNotebook.Tab": {"configure": {"padding": [13, 5], "font": ('Proxima Nova Rg', '11'), "background": secondary_bg, 'foreground': 'white', 'borderwidth': 1}, "map": {"background": [("selected", bg)], "expand": [("selected", [1, 1, 1, 0])] } } } )
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

