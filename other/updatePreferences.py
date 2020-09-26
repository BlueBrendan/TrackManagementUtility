import tkinter as tk
from tkinter import ttk
from tkinter.tix import *

#global variables
global tagList
global CONFIG

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

def updatePreferences(options, CONFIG_FILE, root):
    global tagList
    global CONFIG
    CONFIG = CONFIG_FILE
    window = tk.Toplevel(master=root)
    window.title("Preferences Window")
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (600 / 2)
    y = (hs / 2) - (385 / 2)
    window.geometry('%dx%d+%d+%d' % (600, 350, x, y))
    window.configure(bg=bg)
    tab_parent = ttk.Notebook(window)
    tab1 = tk.Frame(tab_parent, bg=bg)

    #Web Scraping Tab
    tab_parent.pack(expand=1, fill='both')
    tab_parent.add(tab1, text="Scraping")
    #website settings
    tk.Label(tab1, text="Web Scraping", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(10, 0), pady=(20,5), anchor="w")

    junodownloadFrame = tk.Frame(tab1, bg=bg)
    junodownloadFrame.pack(anchor="w")
    tk.Checkbutton(junodownloadFrame, variable=options['Scrape Junodownload (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Scrape Junodownload (B)', []), bg=bg).pack(padx=(20, 0),side="left")
    tk.Label(junodownloadFrame, text="Junodownload", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    beatportFrame = tk.Frame(tab1, bg=bg)
    beatportFrame.pack(anchor="w")
    tk.Checkbutton(beatportFrame, variable=options['Scrape Beatport (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Scrape Beatport (B)', []), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(beatportFrame, text="Beatport", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    discogsFrame = tk.Frame(tab1, bg=bg)
    discogsFrame.pack(anchor="w")
    tk.Checkbutton(discogsFrame, variable=options['Scrape Discogs (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Scrape Discogs (B)', []), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(discogsFrame, text="Discogs", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    #image scraping settings
    tk.Label(tab1, text="Image Scraping", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(10, 0),pady=(20,5), anchor="w")
    imageSuboptions = []

    # reverse image search
    reverseImageFrame = tk.Frame(tab1, bg=bg)
    reverseImageFrame.pack(anchor="w")
    tk.Checkbutton(reverseImageFrame, variable=options['Reverse Image Search (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Reverse Image Search (B)', imageSuboptions), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(reverseImageFrame, text="Reverse Image Search with Selenium", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    #delete images
    deleteImagesFrame = tk.Frame(tab1, bg=bg)
    deleteImagesFrame.pack(anchor="w")
    deleteImages = tk.Checkbutton(deleteImagesFrame, variable=options['Delete Stored Images (B)'], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Delete Stored Images (B)', []), bg=bg)
    deleteImages.pack(padx=(30, 0), side="left")
    tk.Label(deleteImagesFrame, text="Delete Stored Images after Completion", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    if options["Reverse Image Search (B)"].get()==False:
        deleteImages.config(state=DISABLED)
    imageSuboptions.append(deleteImages)

    #wait time
    waitTimeForm = tk.Frame(tab1, bg=bg)
    waitTimeForm.pack(anchor="w")
    waitTimeText = tk.Label(waitTimeForm, text="Image Load Wait Time (s)", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
    time = StringVar(value=options["Image Load Wait Time (I)"].get())
    time.trace("w", lambda name, index, mode, time=time: entrybox(CONFIG_FILE, "Image Load Wait Time (I)", time))

    waitTime = tk.Entry(waitTimeForm, width=3, textvariable=time, validate="key", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    validate = (waitTime.register(checkInt))
    waitTime.configure(validatecommand=(validate, '%S'))

    # waitTime.insert(0, options["Image Load Wait Time (I)"].get())
    if options["Reverse Image Search (B)"].get()==False:
        deleteImages.config(state=DISABLED)
    imageSuboptions.append(waitTime)
    waitTime.pack(padx=(35, 0), side="left")
    waitTimeText.pack(padx=(10,0), pady=(5,0), side="left")

    #Tag Settings Tab
    tab2 = tk.Frame(tab_parent, bg=bg)
    tab_parent.add(tab2, text="Tagging")
    tagFrame = Frame(tab2, bg=bg)
    tagFrame.pack(side="left", anchor="nw", padx=(5,0))
    tk.Label(tagFrame, text="Tags", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(10, 0), pady=(20, 5), anchor="w")
    tagList = options["Selected Tags (L)"]

    #top row of tagFrame
    tagFrameTopRow = Frame(tagFrame, bg=bg)
    tagFrameTopRow.pack()
    #container for unselected tags
    leftListbox = Frame(tagFrameTopRow, bg=bg)
    leftListbox.pack(side="left")
    #container for listbox button controls
    listboxButtons = Frame(tagFrameTopRow, bg=bg)
    listboxButtons.pack(side="left")
    #container for selected listbox tags
    rightListbox = Frame(tagFrameTopRow, bg=bg)
    rightListbox.pack(side="left")
    #Default Tag settings
    tk.Label(leftListbox, text="Unselected Tags", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack()
    unselectedListbox = tk.Listbox(leftListbox, font=("Proxima Nova Rg", 11),fg="white", bg=secondary_bg)

    tk.Label(rightListbox, text="Selected Tags", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack()
    selectedListbox = tk.Listbox(rightListbox, font=("Proxima Nova Rg", 11),fg="white", bg=secondary_bg)
    comprehensiveList = ['Artist', 'Album', 'Album Artist', 'BPM', 'Comment', 'Compilation', 'Copyright', 'Discnumber', 'Genre', 'Key','Release_Date', 'Title', 'ReplayGain']
    #insert all tags in unselectedListbox
    for tag in comprehensiveList:
        if tag not in options['Selected Tags (L)']:
            unselectedListbox.insert(END, tag)
    #insert all selected tags into selectedListbox and remove from unselectedListbox
    for tag in options['Selected Tags (L)']:
        selectedListbox.insert(END, tag)
    unselectedListbox.pack(padx=(20,5), pady=(5,5))

    select = tk.Button(listboxButtons, text="Select", width=7, state=DISABLED, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    select.pack(side="top")
    deselect = tk.Button(listboxButtons, text="Deselect", width=7, state=DISABLED, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    deselect.pack(side="top")
    selectedListbox.pack(padx=(5,0), pady=(5,5))
    unselectedListbox.bind('<<ListboxSelect>>', lambda event, firstListbox=unselectedListbox, secondListbox=selectedListbox, list=tagList, select=select, deselect=deselect: selectTag(firstListbox, secondListbox, list, select, deselect))
    selectedListbox.bind('<<ListboxSelect>>', lambda event, firstListbox=selectedListbox, secondListbox=unselectedListbox, list=tagList, select=select, deselect=deselect: selectTag(firstListbox, secondListbox, list, select, deselect))

    # bottom row of tagFrame
    tagCheckboxFrame = Frame(tagFrame, bg=bg)
    tagCheckboxFrame.pack(side="left")
    tk.Checkbutton(tagCheckboxFrame, variable=options["Delete Unselected Tags (B)"], command=lambda: checkbox(CONFIG_FILE, 'Delete Unselected Tags (B)', []), bg=bg).pack(padx=(20, 0), pady=(20, 0), side="left")
    tk.Label(tagCheckboxFrame, text="Delete Unselected Tags from File", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(pady=(20, 0), side="left")

    #Others Tab
    tab3 = tk.Frame(tab_parent, bg=bg)
    tab_parent.add(tab3, text="Other")
    leftPane = Frame(tab3, bg=bg)
    leftPane.pack(padx=(5,0), side="left", anchor="nw")
    topLeftComponent = Frame(leftPane, bg=bg)
    topLeftComponent.pack()
    tk.Label(topLeftComponent, text="File Format", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(10, 0), pady=(20,5), anchor="w")
    #frame for first radio button
    artistTitleButtonFrame = tk.Frame(topLeftComponent, bg=bg)
    artistTitleButtonFrame.pack(anchor="w")
    tk.Radiobutton(artistTitleButtonFrame, variable=options["Audio naming format (S)"], value="Artist - Title", command=lambda: namingRadiobutton(CONFIG_FILE, 'Audio naming format (S)', "Artist - Title"), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(artistTitleButtonFrame, text="Artist - Title", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    # frame for second radio button
    titleButtonFrame = tk.Frame(topLeftComponent, bg=bg)
    titleButtonFrame.pack(anchor="w")
    tk.Radiobutton(topLeftComponent, variable=options["Audio naming format (S)"], value="Title", command=lambda: namingRadiobutton(CONFIG_FILE, 'Audio naming format (S)', "Title"), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(topLeftComponent, text="Title", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    rightPane = Frame(tab3, bg=bg)
    rightPane.pack(padx=(0,50), side="right", anchor="nw")
    tk.Label(rightPane, text="Audio Formatting", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(5, 0), pady=(20, 5), anchor="w")
    typoSuboptions = []
    #frame for scan filename and tags checkbutton
    scanButtonFrame = tk.Frame(rightPane, bg=bg)
    scanButtonFrame.pack(anchor="w")
    tk.Checkbutton(scanButtonFrame, variable=options["Scan Filename and Tags (B)"], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, 'Scan Filename and Tags (B)', typoSuboptions), bg=bg).pack(padx=(10, 0), side="left")
    tk.Label(scanButtonFrame, text="Scan Filename and Tags", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    #frame for numbering prefix checkbutton
    prefixButtonFrame = tk.Frame(rightPane, bg=bg)
    prefixButtonFrame.pack(anchor="w")
    numberingPrefix = tk.Checkbutton(prefixButtonFrame, variable=options["Check for Numbering Prefix (B)"], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, "Check for Numbering Prefix (B)", []), bg=bg)
    numberingPrefix.pack(padx=(20, 0), side="left")
    tk.Label(prefixButtonFrame, text="Check for Numbering Prefix", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    typoSuboptions.append(numberingPrefix)
    #frame for hyphen checkbutton
    hyphenButtonFrame = tk.Frame(rightPane, bg=bg)
    hyphenButtonFrame.pack(anchor="w")
    hyphenCheck = tk.Checkbutton(hyphenButtonFrame, variable=options["Check for Extraneous Hyphens (B)"], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, "Check for Extraneous Hyphens (B)", []), bg=bg)
    hyphenCheck.pack(padx=(20, 0), side="left")
    tk.Label(hyphenButtonFrame, text="Check for Extraneous Hyphens", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    typoSuboptions.append(hyphenCheck)
    #frame for capitalization checkbutton
    capitalizationButtonFrame = tk.Frame(rightPane, bg=bg)
    capitalizationButtonFrame.pack(anchor="w")
    capitalizationCheck = tk.Checkbutton(capitalizationButtonFrame, variable=options["Check for Capitalization (B)"], onvalue=True, offvalue=False, command=lambda: checkbox(CONFIG_FILE, "Check for Capitalization (B)", []), bg=bg)
    capitalizationCheck.pack(padx=(20, 0), side="left")
    tk.Label(capitalizationButtonFrame, text="Check for Capitalization", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    typoSuboptions.append(capitalizationCheck)

    if options["Scan Filename and Tags (B)"].get()==False:
        numberingPrefix.config(state=DISABLED)
        hyphenCheck.config(state=DISABLED)
        capitalizationCheck.config(state=DISABLED)
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

