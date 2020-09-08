from tkinter import *
from tkinter import ttk

def updatePreferences(options, CONFIG_FILE):
    window = Toplevel()
    window.title("Preferences Window")
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (500 / 2)
    y = (hs / 2) - (400 / 2)
    window.geometry('%dx%d+%d+%d' % (500, 300, x, y))
    tab_parent = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_parent)


    #Web Scraping Tab
    tab_parent.add(tab1, text="Web Scraping")
    tab_parent.pack(expand=1, fill='both')

    #website settings
    Label(tab1, text="Websites to Scrape").pack(pady=(10,5), anchor="w")
    junoCheck = Checkbutton(tab1, text="Juno Download", command=lambda: checkbox(CONFIG_FILE, 'Scrape Junodownload (B)'))
    if options['Scrape Junodownload (B)'].get()==True:
        junoCheck.select()
    beatportCheck = Checkbutton(tab1, text="Beatport", command=lambda: checkbox(CONFIG_FILE, 'Scrape Beatport (B)'))
    if options['Scrape Beatport (B)'].get() == True:
        beatportCheck.select()
    discogsCheck = Checkbutton(tab1, text="Discogs", command=lambda: checkbox(CONFIG_FILE, 'Scrape Discogs (B)'))
    if options['Scrape Discogs (B)'].get() == True:
        discogsCheck.select()
    junoCheck.pack(padx=(10, 0), anchor="w")
    beatportCheck.pack(padx=(10, 0), anchor="w")
    discogsCheck.pack(padx=(10, 0), anchor="w")

    #image scraping settings
    Label(tab1, text="Image Scraping").pack(pady=(15,5), anchor="w")
    reverseImageSearchCheck = Checkbutton(tab1, text="Reverse Image Search with Selenium", command=lambda: checkbox(CONFIG_FILE, 'Reverse Image Search (B)'))
    if options['Reverse Image Search (B)'].get() == True:
        reverseImageSearchCheck.select()
    deleteStoredImagesCheck = Checkbutton(tab1, text="Delete Stored Images after Completion", command=lambda: checkbox(CONFIG_FILE, 'Delete Stored Images (B)'))
    if options['Delete Stored Images (B)'].get() == True:
        deleteStoredImagesCheck.select()
    deleteStoredImagesCheck.pack(padx=(10, 0), anchor="w")

    #Tag Settings Tab
    tab2 = ttk.Frame(tab_parent)
    tab_parent.add(tab2, text="Tagging")

    #Others Tab
    tab3 = ttk.Frame(tab_parent)
    tab_parent.add(tab3, text="Other")
    Label(tab3, text="Audio Formatting").pack(pady=(10, 5), anchor="w")
    # var = IntVar()
    # # for format in formats:
    # var.set(1)
    # ttk.Radiobutton(tab3, text="Artist - Title", variable=var, value=1).pack(pady=(5, 5), anchor="w")
    # ttk.Radiobutton(tab3, text="Title", variable=var, value=2).pack(pady=(5, 5), anchor="w")

def test(value):
    print(value)

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