import tkinter as tk
from tkinter import ttk
from tkinter.tix import *
from tkinter import messagebox
import getpass

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

    root.mainloop()

def webScrapingTab(tab_parent, options, CONFIG_FILE):
    # web Scraping Tab
    tab1 = tk.Frame(tab_parent, bg=bg)
    tab_parent.pack(expand=1, fill='both')
    tab_parent.add(tab1, text="Scraping")
    # website settings
    tk.Label(tab1, text="Web Scraping", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(10, 0), pady=(20, 5), anchor="w")
    topComponentFrame = tk.Frame(tab1, bg=bg)
    topComponentFrame.pack(fill=X)
    leftComponentFrame = tk.Frame(topComponentFrame, bg=bg)
    leftComponentFrame.pack(side="left", anchor="nw")
    rightComponentFrame = tk.Frame(topComponentFrame, bg=bg)
    rightComponentFrame.pack(side="left", anchor="nw")

    # website options
    junodownloadFrame = tk.Frame(leftComponentFrame, bg=bg)
    junodownloadFrame.pack(anchor="w")
    tk.Checkbutton(junodownloadFrame, variable=options['Scrape Junodownload (B)'], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Scrape Junodownload (B)', []), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(junodownloadFrame, text="Junodownload", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    beatportFrame = tk.Frame(leftComponentFrame, bg=bg)
    beatportFrame.pack(anchor="w")
    tk.Checkbutton(beatportFrame, variable=options['Scrape Beatport (B)'], onvalue=True, offvalue=False,  activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Scrape Beatport (B)', []), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(beatportFrame, text="Beatport", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    discogsFrame = tk.Frame(leftComponentFrame, bg=bg)
    discogsFrame.pack(anchor="w")
    tk.Checkbutton(discogsFrame, variable=options['Scrape Discogs (B)'], onvalue=True, offvalue=False,  activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Scrape Discogs (B)', []), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(discogsFrame, text="Discogs", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    # web image option
    imageOptions = []
    imageCheckFrame = tk.Frame(rightComponentFrame, bg=bg)
    imageCheckFrame.pack(anchor="w")
    tk.Checkbutton(imageCheckFrame, variable=options["Extract Image from Website (B)"], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, "Extract Image from Website (B)", imageOptions), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(imageCheckFrame, text="Extract Image from Website", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    # image scraping settings
    tk.Label(tab1, text="Image Scraping", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(10, 0), pady=(20, 5), anchor="w")
    imageScrapingSuboptions = []

    # reverse image search
    reverseImageFrame = tk.Frame(tab1, bg=bg)
    reverseImageFrame.pack(anchor="w")
    seleniumCheckbox = tk.Checkbutton(reverseImageFrame, variable=options['Reverse Image Search (B)'], onvalue=True, offvalue=False,  activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Reverse Image Search (B)', imageScrapingSuboptions), bg=bg)
    seleniumCheckbox.pack(padx=(20, 0), side="left")
    tk.Label(reverseImageFrame, text="Reverse Image Search with Selenium", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    if options["Extract Image from Website (B)"].get() == False: seleniumCheckbox.config(state=DISABLED)
    imageOptions.append(seleniumCheckbox)

    # delete images
    deleteImagesFrame = tk.Frame(tab1, bg=bg)
    deleteImagesFrame.pack(anchor="w")
    deleteImages = tk.Checkbutton(deleteImagesFrame, variable=options['Delete Stored Images (B)'], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Delete Stored Images (B)', []), bg=bg)
    deleteImages.pack(padx=(30, 0), side="left")
    tk.Label(deleteImagesFrame, text="Delete Stored Images after Completion", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    if options["Extract Image from Website (B)"].get()==False or options["Reverse Image Search (B)"].get() == False: deleteImages.config(state=DISABLED)
    imageScrapingSuboptions.append(deleteImages)

    # wait time
    waitTimeForm = tk.Frame(tab1, bg=bg)
    waitTimeForm.pack(anchor="w")
    waitTimeText = tk.Label(waitTimeForm, text="Image Load Wait Time (s)", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
    time = StringVar(value=options["Image Load Wait Time (I)"].get())
    time.trace("w", lambda name, index, mode, time=time: entrybox(CONFIG_FILE, "Image Load Wait Time (I)", time))

    waitTime = tk.Entry(waitTimeForm, width=3, textvariable=time, validate="key", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    validate = (waitTime.register(checkInt))
    waitTime.configure(validatecommand=(validate, '%S'))

    if options["Extract Image from Website (B)"].get()==False or options["Reverse Image Search (B)"].get() == False: waitTime.config(state=DISABLED)
    imageScrapingSuboptions.append(waitTime)
    waitTime.pack(padx=(35, 0), side="left")
    waitTimeText.pack(padx=(10, 0), pady=(5, 0), side="left")

def taggingTab(tab_parent, options, CONFIG_FILE):
    # Tag Settings Tab
    tab2 = tk.Frame(tab_parent, bg=bg)
    tab_parent.add(tab2, text="Tagging")
    tagFrame = Frame(tab2, bg=bg)
    tagFrame.pack(side="left", anchor="nw", padx=(5, 0))
    tk.Label(tagFrame, text="Tags", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(10, 0), pady=(20, 5), anchor="w")
    tagList = options["Selected Tags (L)"]

    # top row of tagFrame
    tagFrameTopRow = Frame(tagFrame, bg=bg)
    tagFrameTopRow.pack()
    # container for unselected tags
    leftListbox = Frame(tagFrameTopRow, bg=bg)
    leftListbox.pack(side="left")
    # container for listbox button controls
    listboxButtons = Frame(tagFrameTopRow, bg=bg)
    listboxButtons.pack(side="left")
    # container for selected listbox tags
    rightListbox = Frame(tagFrameTopRow, bg=bg)
    rightListbox.pack(side="left")
    # Default Tag settings
    tk.Label(leftListbox, text="Unselected Tags", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack()
    unselectedListbox = tk.Listbox(leftListbox, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)

    tk.Label(rightListbox, text="Selected Tags", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack()
    selectedListbox = tk.Listbox(rightListbox, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    comprehensiveList = ['Artist', 'Album', 'Album Artist', 'BPM', 'Comment', 'Compilation', 'Copyright', 'Discnumber', 'Genre', 'Key', 'Release_Date', 'Title', 'ReplayGain']
    # insert all tags in unselectedListbox
    for tag in comprehensiveList:
        if tag not in options['Selected Tags (L)']: unselectedListbox.insert(END, tag)
    # insert all selected tags into selectedListbox and remove from unselectedListbox
    for tag in options['Selected Tags (L)']:
        selectedListbox.insert(END, tag)
    unselectedListbox.pack(padx=(20, 5), pady=(5, 5))

    select = tk.Button(listboxButtons, text="Select", width=7, state=DISABLED, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    select.pack(side="top")
    deselect = tk.Button(listboxButtons, text="Deselect", width=7, state=DISABLED, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    deselect.pack(side="top")
    selectedListbox.pack(padx=(5, 0), pady=(5, 5))
    unselectedListbox.bind('<<ListboxSelect>>', lambda event, firstListbox=unselectedListbox, secondListbox=selectedListbox, list=tagList, select=select, deselect=deselect: selectTag(firstListbox, secondListbox, list, select, deselect))
    selectedListbox.bind('<<ListboxSelect>>', lambda event, firstListbox=selectedListbox, secondListbox=unselectedListbox, list=tagList, select=select, deselect=deselect: selectTag(firstListbox, secondListbox, list, select, deselect))

    # bottom row of tagFrame
    tagCheckboxFrame = Frame(tagFrame, bg=bg)
    tagCheckboxFrame.pack(side="left")
    tk.Checkbutton(tagCheckboxFrame, variable=options["Delete Unselected Tags (B)"], activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Delete Unselected Tags (B)', []), bg=bg).pack(padx=(20, 0), pady=(20, 0), side="left")
    tk.Label(tagCheckboxFrame, text="Delete Unselected Tags from File", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(pady=(20, 0), side="left")

def namingTab(tab_parent, options, CONFIG_FILE):
    tab3 = tk.Frame(tab_parent, bg=bg)
    tab_parent.add(tab3, text="Naming")
    leftPane = Frame(tab3, bg=bg)
    leftPane.pack(padx=(5, 0), side="left", anchor="nw")
    tk.Label(leftPane, text="Keywords", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(10, 0), pady=(20, 5), anchor="w")
    # container for capitalized keywords
    leftListboxFrame = tk.Frame(leftPane, bg=bg)
    leftListboxFrame.pack(side="left")
    tk.Label(leftListboxFrame, text="Capitalize", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack()
    leftListboxContainer = tk.Frame(leftListboxFrame, bg=bg)
    leftListboxContainer.pack()
    leftListboxControls = tk.Frame(leftListboxFrame, bg=bg)
    leftListboxControls.pack()

    # container for non-capitalized keywords
    rightListboxFrame = tk.Frame(leftPane, bg=bg)
    rightListboxFrame.pack(side="left")
    tk.Label(rightListboxFrame, text="Uncapitalize", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack()
    rightListboxContainer = tk.Frame(rightListboxFrame, bg=bg)
    rightListboxContainer.pack()
    rightListboxControls = tk.Frame(rightListboxFrame, bg=bg)
    rightListboxControls.pack()

    capitalizedListbox = tk.Listbox(leftListboxContainer, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, highlightbackground="black", highlightcolor="grey")
    uncapitalizedListbox = tk.Listbox(rightListboxContainer, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, highlightbackground="black", highlightcolor="grey")

    # populate listboxes
    for keyword in options["Always Capitalize (L)"]: capitalizedListbox.insert(END, keyword)
    for keyword in options["Never Capitalize (L)"]:
        uncapitalizedListbox.insert(END, keyword)
    capitalizedListbox.pack(padx=(20, 5), pady=(5, 5))
    capitalizeAdd = tk.Button(leftListboxControls, text="Add", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, width=5, command=lambda: addKeywordPrompt("Always Capitalize (L)", "Never Capitalize (L)", capitalizedListbox, options))
    capitalizeAdd.pack(side="left", padx=(15, 20))
    capitalizeDelete = tk.Button(leftListboxControls, text="Delete", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, state=DISABLED)
    capitalizeDelete.pack(side="left", padx=(20, 0))
    uncapitalizedListbox.pack(padx=(20, 5), pady=(5, 5))
    uncapitalizeAdd = tk.Button(rightListboxControls, text="Add", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, width=5, command=lambda: addKeywordPrompt("Never Capitalize (L)", "Always Capitalize (L)", uncapitalizedListbox, options))
    uncapitalizeAdd.pack(side="left", padx=(15, 20))
    uncapitalizeDelete = tk.Button(rightListboxControls, text="Delete", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, state=DISABLED)
    uncapitalizeDelete.pack(side="left", padx=(20, 0))

    #bind listboxes to buttons
    capitalizedListbox.bind('<<ListboxSelect>>', lambda event, listbox=capitalizedListbox, select=capitalizeDelete, deselect=uncapitalizeDelete: selectKeyword(listbox, select, deselect, "Always Capitalize (L)", options))
    uncapitalizedListbox.bind('<<ListboxSelect>>', lambda event, listbox=uncapitalizedListbox, select=uncapitalizeDelete, deselect=capitalizeDelete: selectKeyword(listbox, select, deselect, "Never Capitalize (L)", options))

    rightPane = Frame(tab3, bg=bg)
    rightPane.pack(padx=(0, 50), side="right", anchor="nw")
    tk.Label(rightPane, text="Audio Formatting", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(5, 0), pady=(20, 5), anchor="w")
    typoSuboptions = []

    # frame for scan filename and tags checkbutton
    scanButtonFrame = tk.Frame(rightPane, bg=bg)
    scanButtonFrame.pack(anchor="w")
    tk.Checkbutton(scanButtonFrame, variable=options["Scan Filename and Tags (B)"], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Scan Filename and Tags (B)', typoSuboptions), bg=bg).pack(padx=(10, 0), side="left")
    tk.Label(scanButtonFrame, text="Scan Filename and Tags", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    # frame for numbering prefix checkbutton
    prefixButtonFrame = tk.Frame(rightPane, bg=bg)
    prefixButtonFrame.pack(anchor="w")
    numberingPrefix = tk.Checkbutton(prefixButtonFrame, variable=options["Check for Numbering Prefix (B)"], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, "Check for Numbering Prefix (B)", []), bg=bg)
    numberingPrefix.pack(padx=(20, 0), side="left")
    tk.Label(prefixButtonFrame, text="Check for Numbering Prefix", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    typoSuboptions.append(numberingPrefix)
    # frame for hyphen checkbutton
    hyphenButtonFrame = tk.Frame(rightPane, bg=bg)
    hyphenButtonFrame.pack(anchor="w")
    hyphenCheck = tk.Checkbutton(hyphenButtonFrame, variable=options["Check for Extraneous Hyphens (B)"], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, "Check for Extraneous Hyphens (B)", []), bg=bg)
    hyphenCheck.pack(padx=(20, 0), side="left")
    tk.Label(hyphenButtonFrame, text="Check for Extraneous Hyphens", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    typoSuboptions.append(hyphenCheck)
    # frame for capitalization checkbutton
    capitalizationButtonFrame = tk.Frame(rightPane, bg=bg)
    capitalizationButtonFrame.pack(anchor="w")
    capitalizationCheck = tk.Checkbutton(capitalizationButtonFrame, variable=options["Check for Capitalization (B)"], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, "Check for Capitalization (B)", []), bg=bg)
    capitalizationCheck.pack(padx=(20, 0), side="left")
    tk.Label(capitalizationButtonFrame, text="Check for Capitalization", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    typoSuboptions.append(capitalizationCheck)

    # frame for file format
    formatFrame = tk.Frame(rightPane, bg=bg)
    formatFrame.pack(anchor="w")
    tk.Label(formatFrame, text="File Format", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(10, 0), pady=(20, 5), anchor="w")
    # frame for first radio button
    artistTitleButtonFrame = tk.Frame(formatFrame, bg=bg)
    artistTitleButtonFrame.pack(anchor="w")
    tk.Radiobutton(artistTitleButtonFrame, variable=options["Audio naming format (S)"], value="Artist - Title", command=lambda: namingRadiobutton(CONFIG_FILE, 'Audio naming format (S)', "Artist - Title"), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(artistTitleButtonFrame, text="Artist - Title", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    # frame for second radio button
    titleButtonFrame = tk.Frame(formatFrame, bg=bg)
    titleButtonFrame.pack(anchor="w")
    tk.Radiobutton(formatFrame, variable=options["Audio naming format (S)"], value="Title", command=lambda: namingRadiobutton(CONFIG_FILE, 'Audio naming format (S)', "Title"), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(formatFrame, text="Title", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    if options["Scan Filename and Tags (B)"].get() == False:
        numberingPrefix.config(state=DISABLED)
        hyphenCheck.config(state=DISABLED)
        capitalizationCheck.config(state=DISABLED)

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
    for tag in list: newListValues += tag + ', '
    newListValues = newListValues[:-2]
    with open(CONFIG, 'wt') as file:
        file.write(config_file.replace(str(originalListValues), str(newListValues)))
    file.close()

def selectKeyword(listbox, select, deselect, list, options):
    if len(listbox.curselection()) > 0:
        select.config(state=NORMAL, command=lambda: deleteKeyword(list, listbox, listbox.curselection(), select, options))
        deselect.config(state=DISABLED)

#prompt popup window to add keyword
def addKeywordPrompt(list, alternateList, listbox, options):
    popup = tk.Toplevel()
    popup.title("Add Keyword")
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (400 / 2)
    y = (hs / 2) - (187 / 2)
    popup.geometry('%dx%d+%d+%d' % (400, 170, x, y))
    popup.configure(bg=bg)
    if list == "Always Capitalize (L)": tk.Label(popup, text="Enter the keyword to add to the capitalized list", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(pady=(25, 10))
    elif list == "Never Capitalize (L)": tk.Label(popup, text="Enter the keyword to add to the uncapitalized list", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(pady=(25, 0))
    userInput = StringVar()
    inputWidget = tk.Entry(popup, width=30, textvariable=userInput, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)

    inputWidget.pack(pady=(20, 20))
    buttonFrame = tk.Frame(popup, bg=bg)
    buttonFrame.pack()
    confirmButton = tk.Button(buttonFrame, text="OK", font=("Proxima Nova Rg", 11), fg="white", width=5, bg=bg, state=DISABLED, command=lambda: addKeywordToList(list, alternateList, listbox, userInput, options, popup))
    confirmButton.pack(side="left", padx=(0, 30))
    tk.Button(buttonFrame, text="Cancel", font=("Proxima Nova Rg", 11), fg="white", bg=bg, command=lambda: popup.destroy()).pack(side="left", padx=(30, 0))
    #monitor changes to user input form
    userInput.trace("w", lambda name, index, mode, input=userInput, button=confirmButton: updateInput(input, button))

#add keyword to list
def addKeywordToList(term, alternateTerm, listbox, userInput, options, popup):
    if userInput.get().lower() in (string.lower() for string in options[term]):
        messagebox.showinfo(parent=popup, title="Error", message="The keyword " + userInput.get().lower() + " is already in the list, you cretin")
        userInput.set("")
    elif userInput.get().lower() in (string.lower() for string in options[alternateTerm]):
        messagebox.showinfo(parent=popup, title="Error", message="The keyword " + userInput.get().lower() + " is in the other list; keywords cannot be stored in both lists")
        userInput.set("")
    else:
        CONFIG_FILE = r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt"
        config_file = open(CONFIG_FILE, 'r').read()
        # convert to term
        originalListValues = options[term]
        newListValues = originalListValues
        originalListValues = ", ".join(originalListValues)
        newListValues.append(userInput.get())
        newListValues.sort()
        newListValues = ", ".join(newListValues)
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(term + ":" + originalListValues, term + ":" + newListValues))
        file.close()
        #add to the keywords listbox
        listbox.insert(END, userInput.get())
        popup.destroy()

#remove keyword from list and settings file
def deleteKeyword(term, listbox, index, select, options):
    CONFIG_FILE = r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt"
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    originalListValues = options[term]
    newListValues = originalListValues
    originalListValues = ", ".join(originalListValues)
    newListValues.remove(listbox.get(index))
    newListValues.sort()
    newListValues = ", ".join(newListValues)
    with open(CONFIG, 'wt') as file:
        file.write(config_file.replace(term + ":" + originalListValues, term + ":" + newListValues))
    file.close()
    # remove from listbox
    listbox.delete(index, index)
    #disable delete button
    select.config(state=DISABLED)

#update button according to user input (adding keyword)
def updateInput(input, button):
    if len(input.get()) > 0: button.config(state=NORMAL)
    else: button.config(state=DISABLED)

#check if input is an integer, reject if not
def checkInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

