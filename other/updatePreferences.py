import tkinter as tk
from tkinter import ttk
from tkinter.tix import *

def updatePreferences(options, CONFIG_FILE, root):
    window = tk.Toplevel(master=root)
    window.title("Preferences Window")
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (500 / 2)
    y = (hs / 2) - (330 / 2)
    window.geometry('%dx%d+%d+%d' % (500, 300, x, y))
    tab_parent = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_parent)

    #Web Scraping Tab
    tab_parent.pack(expand=1, fill='both')
    tab_parent.add(tab1, text="Scraping")
    #website settings
    tk.Label(tab1, text="Web Scraping").pack(padx=(5, 0), pady=(10,5), anchor="w")
    tk.Checkbutton(tab1, text="Juno Download", variable=options['Scrape Junodownload (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Scrape Junodownload (B)')).pack(padx=(10, 0), anchor="w")
    tk.Checkbutton(tab1, text="Beatport", variable=options['Scrape Beatport (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Scrape Beatport (B)')).pack(padx=(10, 0), anchor="w")
    tk.Checkbutton(tab1, text="Discogs", variable=options['Scrape Discogs (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Scrape Discogs (B)')).pack(padx=(10, 0), anchor="w")

    #image scraping settings
    tk.Label(tab1, text="Image Scraping").pack(padx=(5, 0),pady=(15,5), anchor="w")
    tk.Checkbutton(tab1, text="Reverse Image Search with Selenium", variable=options['Reverse Image Search (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Reverse Image Search (B)')).pack(padx=(10, 0), anchor="w")
    tk.Checkbutton(tab1, text="Delete Stored Images after Completion", variable=options['Delete Stored Images (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Delete Stored Images (B)')).pack(padx=(10, 0), anchor="w")

    #Tag Settings Tab
    tab2 = ttk.Frame(tab_parent)
    tab_parent.add(tab2, text="Tagging")

    #Others Tab
    tab3 = ttk.Frame(tab_parent)
    tab_parent.add(tab3, text="Other")
    tk.Label(tab3, text="Audio Formatting").pack(padx=(5, 0), pady=(10, 5), anchor="w")
    tk.Checkbutton(tab3, text="Check Artist for Common Typos", variable=options["Check Artist for Typos (B)"], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Check Artist for Typos (B)')).pack(padx=(10, 0), anchor="w")
    tk.Label(tab3, text="Audio Naming Format").pack(padx=(5, 0), pady=(10,5), anchor="w")
    tk.Radiobutton(tab3, text="Artist - Title", variable=options["Audio naming format (S)"], value="Artist - Title", command=lambda: namingRadiobutton(CONFIG_FILE, 'Audio naming format (S)', "Artist - Title")).pack(padx=(10, 0), anchor="w")
    tk.Radiobutton(tab3, text="Title", variable=options["Audio naming format (S)"], value="Title", command=lambda: namingRadiobutton(CONFIG_FILE, 'Audio naming format (S)', "Title")).pack(padx=(10, 0), anchor="w")
    root.mainloop()

def checkbox(CONFIG_FILE, term):
    config_file = open(CONFIG_FILE, 'r').read()
    # if true, turn option to false
    if config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] == "True":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1]) + "True",str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + "False"))
        file.close()
    # if false, turn option to true
    elif config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] == "False":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1]) + "False",str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + "True"))
        file.close()

def namingRadiobutton(CONFIG_FILE, term, value):
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    if config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] != value:
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]), str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + value))
        file.close()