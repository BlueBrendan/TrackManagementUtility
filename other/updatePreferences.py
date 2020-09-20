import tkinter as tk
from tkinter import ttk
from tkinter.tix import *

#global variables
global tagList
global CONFIG

def updatePreferences(options, CONFIG_FILE, root):
    global tagList
    global CONFIG
    CONFIG = CONFIG_FILE
    window = tk.Toplevel(master=root)
    window.title("Preferences Window")
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (600 / 2)
    y = (hs / 2) - (330 / 2)
    window.geometry('%dx%d+%d+%d' % (600, 300, x, y))
    tab_parent = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_parent)

    #Web Scraping Tab
    tab_parent.pack(expand=1, fill='both')
    tab_parent.add(tab1, text="Scraping")
    #website settings
    tk.Label(tab1, text="Web Scraping", font=("TkDefaultFont", 9, 'bold')).pack(padx=(5, 0), pady=(10,5), anchor="w")
    tk.Checkbutton(tab1, text="Juno Download", variable=options['Scrape Junodownload (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Scrape Junodownload (B)', [])).pack(padx=(10, 0), anchor="w")
    tk.Checkbutton(tab1, text="Beatport", variable=options['Scrape Beatport (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Scrape Beatport (B)', [])).pack(padx=(10, 0), anchor="w")
    tk.Checkbutton(tab1, text="Discogs", variable=options['Scrape Discogs (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Scrape Discogs (B)', [])).pack(padx=(10, 0), anchor="w")

    #image scraping settings
    tk.Label(tab1, text="Image Scraping", font=("TkDefaultFont", 9, 'bold')).pack(padx=(5, 0),pady=(15,5), anchor="w")
    imageSuboptions = []
    deleteImages = tk.Checkbutton(tab1, text="Delete Stored Images after Completion", variable=options['Delete Stored Images (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Delete Stored Images (B)', []))
    if options["Reverse Image Search (B)"].get()==False:
        deleteImages.config(state=DISABLED)
    imageSuboptions.append(deleteImages)
    #wait time
    waitTimeText = tk.Label(tab1, text="Image Load Wait Time (s)")
    time = StringVar(value=options["Image Load Wait Time (I)"].get())
    time.trace("w", lambda name, index, mode, time=time: entrybox(CONFIG_FILE, "Image Load Wait Time (I)", time))

    waitTime = tk.Entry(tab1, width=5, textvariable=time, validate="key")
    validate = (waitTime.register(checkInt))
    waitTime.configure(validatecommand=(validate, '%S'))

    # waitTime.insert(0, options["Image Load Wait Time (I)"].get())
    if options["Reverse Image Search (B)"].get()==False:
        deleteImages.config(state=DISABLED)
    imageSuboptions.append(waitTime)
    tk.Checkbutton(tab1, text="Reverse Image Search with Selenium", variable=options['Reverse Image Search (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Reverse Image Search (B)',imageSuboptions)).pack(padx=(10, 0), anchor="w")
    deleteImages.pack(padx=(10, 0), anchor="w")
    waitTimeText.pack(padx=(10, 0), pady=(5,0), anchor="w")
    waitTime.pack(padx=(15, 0), anchor="w")

    #Tag Settings Tab
    tab2 = ttk.Frame(tab_parent)
    tab_parent.add(tab2, text="Tagging")
    tagFrame = Frame(tab2)
    tagFrame.pack(side="left", anchor="nw", padx=(5,0))
    tk.Label(tagFrame, text="Tags", font=("TkDefaultFont", 9, 'bold')).pack(padx=(5, 0), pady=(10, 5), anchor="w")
    tagList = options["Selected Tags (L)"]

    #top row of tagFrame
    tagFrameTopRow = Frame(tagFrame)
    tagFrameTopRow.pack()
    #container for unselected tags
    leftListbox = Frame(tagFrameTopRow)
    leftListbox.pack(side="left")
    #container for listbox button controls
    listboxButtons = Frame(tagFrameTopRow)
    listboxButtons.pack(side="left")
    #container for selected listbox tags
    rightListbox = Frame(tagFrameTopRow)
    rightListbox.pack(side="left")
    #Default Tag settings
    tk.Label(leftListbox, text="Unselected Tags").pack()
    unselectedListbox = tk.Listbox(leftListbox)

    tk.Label(rightListbox, text="Selected Tags").pack()
    selectedListbox = tk.Listbox(rightListbox)
    comprehensiveList = ['Artist', 'Album', 'Album Artist', 'BPM', 'Comment', 'Compilation', 'Copyright', 'Discnumber', 'Genre', 'Key','Release Date', 'Title', 'ReplayGain']
    #insert all tags in unselectedListbox
    for tag in comprehensiveList:
        if tag not in options['Selected Tags (L)']:
            unselectedListbox.insert(END, tag)
    #insert all selected tags into selectedListbox and remove from unselectedListbox
    for tag in options['Selected Tags (L)']:
        selectedListbox.insert(END, tag)
    unselectedListbox.pack(padx=(5,5), pady=(5,5))

    select = tk.Button(listboxButtons, text="Select", width=7, state=DISABLED)
    select.pack(side="top")
    deselect = tk.Button(listboxButtons, text="Deselect", width=7, state=DISABLED)
    deselect.pack(side="top")
    selectedListbox.pack(padx=(5,0), pady=(5,5))
    unselectedListbox.bind('<<ListboxSelect>>', lambda event, firstListbox=unselectedListbox, secondListbox=selectedListbox, list=tagList, select=select, deselect=deselect: tag(firstListbox, secondListbox, list, select, deselect))
    selectedListbox.bind('<<ListboxSelect>>', lambda event, firstListbox=selectedListbox, secondListbox=unselectedListbox, list=tagList, select=select, deselect=deselect: tag(firstListbox, secondListbox, list, select, deselect))


    # bottom row of tagFrame
    tagFrameBottomRow = Frame(tagFrame)
    tagFrameBottomRow.pack(side="left")
    tk.Checkbutton(tagFrameBottomRow, text="Delete Unselected Tags from File", variable=options["Delete Unselected Tags (B)"], command=lambda: checkbox(CONFIG_FILE, 'Delete Unselected Tags (B)', [])).pack(padx=(5, 0), side="left")

    # replayGain settings
    replayGainFrame = Frame(tab2)
    replayGainFrame.pack(side="right", anchor="nw", padx=(0,5))
    tk.Label(replayGainFrame, text="ReplayGain", font=("TkDefaultFont", 9, 'bold')).pack(padx=(5, 0), pady=(10, 5), anchor="w")
    replayGainSuboptions = []
    calculateReplayGain = tk.Checkbutton(replayGainFrame, text="Override Existing ReplayGain value", variable=options['Overwrite existing ReplayGain value (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Overwrite existing ReplayGain value (B)', []))
    if options['Calculate ReplayGain (B)'].get()==False:
        calculateReplayGain.config(state=DISABLED)
    replayGainSuboptions.append(calculateReplayGain)
    tk.Checkbutton(replayGainFrame, text="Calculate ReplayGain", variable=options['Calculate ReplayGain (B)'], onvalue=True, offvalue=False,command=lambda: checkbox(CONFIG_FILE, 'Calculate ReplayGain (B)', replayGainSuboptions)).pack(padx=(10, 0), anchor="w")
    calculateReplayGain.pack(padx=(10, 0), anchor="w")

    #Others Tab
    tab3 = ttk.Frame(tab_parent)
    tab_parent.add(tab3, text="Other")
    leftPane = Frame(tab3)
    leftPane.pack(padx=(5,0), side="left", anchor="nw")
    topLeftComponent = Frame(leftPane)
    topLeftComponent.pack()
    tk.Label(topLeftComponent, text="File Format").pack(padx=(5, 0), pady=(10,5), anchor="w")
    tk.Radiobutton(topLeftComponent, text="Artist - Title", variable=options["Audio naming format (S)"], value="Artist - Title", command=lambda: namingRadiobutton(CONFIG_FILE, 'Audio naming format (S)', "Artist - Title")).pack(padx=(10, 0), anchor="w")
    tk.Radiobutton(topLeftComponent, text="Title", variable=options["Audio naming format (S)"], value="Title", command=lambda: namingRadiobutton(CONFIG_FILE, 'Audio naming format (S)', "Title")).pack(padx=(10, 0), anchor="w")

    rightPane = Frame(tab3)
    rightPane.pack(padx=(0,50), side="right", anchor="nw")
    tk.Label(rightPane, text="Audio Formatting").pack(padx=(5, 0), pady=(10, 5), anchor="w")
    typoSuboptions = []
    numberingPrefix = tk.Checkbutton(rightPane, text="Check for Numbering Prefix", variable=options["Check for Numbering Prefix (B)"], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, "Check for Numbering Prefix (B)", []))
    typoSuboptions.append(numberingPrefix)
    hyphenCheck = tk.Checkbutton(rightPane, text="Check for Extraneous Hyphens", variable=options["Check for Extraneous Hyphens (B)"], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, "Check for Extraneous Hyphens (B)", []))
    typoSuboptions.append(hyphenCheck)
    capitalizationCheck = tk.Checkbutton(rightPane, text="Check for Capitalization", variable=options["Check for Capitalization (B)"], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, "Check for Capitalization (B)", []))
    typoSuboptions.append(capitalizationCheck)

    if options["Scan Filename and Tags (B)"].get()==False:
        numberingPrefix.config(state=DISABLED)
        hyphenCheck.config(state=DISABLED)
        capitalizationCheck.config(state=DISABLED)
    tk.Checkbutton(rightPane, text="Scan Filename and Tags", variable=options["Scan Filename and Tags (B)"], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Scan Filename and Tags (B)', typoSuboptions)).pack(padx=(10, 0), anchor="w")
    numberingPrefix.pack(padx=(15, 0), anchor="w")
    hyphenCheck.pack(padx=(15, 0), anchor="w")
    capitalizationCheck.pack(padx=(15, 0), anchor="w")
    root.mainloop()

def checkbox(CONFIG_FILE, term, suboptions):
    config_file = open(CONFIG_FILE, 'r').read()
    # if true, turn option to false
    if config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] == "True":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1]) + "True",str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + "False"))
        file.close()
        if len(suboptions) > 0:
            #disable all provided suboptions
            for suboption in suboptions:
                suboption.configure(state=DISABLED)
    # if false, turn option to true
    elif config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] == "False":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1]) + "False",str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + "True"))
        file.close()
        if len(suboptions) > 0:
            #enable all provided suboptions
            for suboption in suboptions:
                suboption.configure(state=NORMAL)

def namingRadiobutton(CONFIG_FILE, term, value):
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    if config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] != value:
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term):config_file.index('\n', config_file.index(term) + len(term))]), str(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term)) + 1])) + value))
        file.close()

def entrybox(CONFIG_FILE, term, value):
    if value.get() == '':
        value.set(0)
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    with open(CONFIG_FILE, 'wt') as file:
        file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]), str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + str(value.get())))
    file.close()

#handle listbox click interaction
def selectTag(firstListbox, secondListbox, list, select, deselect):
    if len(firstListbox.curselection()) > 0:
        index = int(firstListbox.curselection()[0])
        tag = firstListbox.get(index)
        if tag in list:
            select.configure(state=DISABLED)
            deselect.configure(state=NORMAL, command=lambda: disableTag(firstListbox, secondListbox, tag, index, list, deselect))
        else:
            select.configure(state=NORMAL, command=lambda: enableTag(firstListbox, secondListbox, tag, index, list, select))
            deselect.configure(state=DISABLED)

def enableTag(firstListbox, secondListbox, tag, index, list, button):
    #first listbox is the unselected listbox, second listbox is the selected listbox
    global tagList, CONFIG
    config_file = open(CONFIG, 'r').read()
    firstListbox.delete(index, index)
    secondListbox.insert(END, tag)
    list.append(tag)
    list.sort()
    tagList = list
    button.configure(state=DISABLED)

    term = "Selected Tags (L)"
    originalListValues = str(config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))])
    newListValues = ''
    for tag in list:
        newListValues += tag + ', '
    newListValues = newListValues[:-2]
    with open(CONFIG, 'wt') as file:
        file.write(config_file.replace(str(originalListValues), str(newListValues)))
    file.close()

def disableTag(firstListbox, secondListbox, tag, index, list, button):
    # first listbox is the selected listbox, second listbox is the unselected listbox
    global tagList, CONFIG
    config_file = open(CONFIG, 'r').read()
    firstListbox.delete(index, index)
    secondListbox.insert(END, tag)
    list.remove(tag)
    list.sort()
    tagList = list
    button.configure(state=DISABLED)

    term = "Selected Tags (L)"
    originalListValues = str(config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))])
    newListValues = ''
    for tag in list:
        newListValues += tag + ', '
    newListValues = newListValues[:-2]
    with open(CONFIG, 'wt') as file:
        file.write(config_file.replace(str(originalListValues), str(newListValues)))
    file.close()
#check if input is an integer, reject if not
def checkInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

