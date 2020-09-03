from tkinter import *
from tkinter import ttk

def updatePreferences(options, CONFIG_FILE):
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
    Label(tab1, text="Websites to Scrape").grid(row=0, column=0)
    # Checkbutton(tab1, text="Beatport", var=scrapeBeatport, command=lambda: beatportCheckbox(CONFIG_FILE, config_file)).grid(row=2, column=0, padx=(10, 0), pady=(0, 0), sticky=W)
    # Checkbutton(tab1, text="Discogs", var=scrapeDiscogs, command=lambda: discogsCheckbox(CONFIG_FILE, config_file)).grid(row=3, column=0, padx=(10, 0), pady=(0, 0), sticky=W)
    tab_parent.add(tab2, text="Lorem Ipsum")
    tab_parent.pack(expand=1, fill='both')
    junoCheck = Checkbutton(tab1, text="Juno Download", command=lambda: checkbox(CONFIG_FILE, 'Scrape Junodownload (B)'))
    if options['Scrape Junodownload (B)'].get()==True:
        junoCheck.select()
    beatportCheck = Checkbutton(tab1, text="Beatport", command=lambda: checkbox(CONFIG_FILE, 'Scrape Beatport (B)'))
    if options['Scrape Beatport (B)'].get() == True:
        beatportCheck.select()
    discogsCheck = Checkbutton(tab1, text="Discogs", command=lambda: checkbox(CONFIG_FILE, 'Scrape Discogs (B)'))
    if options['Scrape Discogs (B)'].get() == True:
        discogsCheck.select()
    junoCheck.grid(row=1, column=0, padx=(10, 0), pady=(0, 0), sticky=W)
    beatportCheck.grid(row=2, column=0, padx=(10, 0), pady=(0, 0), sticky=W)
    discogsCheck.grid(row=3, column=0, padx=(10, 0), pady=(0, 0), sticky=W)

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