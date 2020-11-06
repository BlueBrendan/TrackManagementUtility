import tkinter as tk
from tkinter.tix import *
from tkinter import messagebox

# import methods
from options.checkboxHandling import checkbox
from commonOperations import resource_path

# global variables
# main bg color
bg = "#282f3b"
# secondary color
secondary_bg = "#364153"
# invalid selection color
invalid_bg = "#801212"
optionsDict = {}

def namingTab(tab_parent, options, CONFIG_FILE):
    tab3 = tk.Frame(tab_parent, bg=bg)
    tab_parent.add(tab3, text="Naming")
    leftPane = Frame(tab3, bg=bg)
    leftPane.pack(padx=(5, 0), side="left", anchor="nw")
    tk.Label(leftPane, text="Keywords", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(20, 0), pady=(20, 5), anchor="w")
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

    capitalizedListbox = tk.Listbox(leftListboxContainer, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, highlightbackground="black", highlightcolor="grey", selectbackground=bg, activestyle="none")
    uncapitalizedListbox = tk.Listbox(rightListboxContainer, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, highlightbackground="black", highlightcolor="grey", selectbackground=bg, activestyle="none")

    # populate listboxes
    for keyword in options["Always Capitalize (L)"]: capitalizedListbox.insert(END, keyword)
    for keyword in options["Never Capitalize (L)"]:
        uncapitalizedListbox.insert(END, keyword)
    capitalizedListbox.pack(padx=(30, 5), pady=(5, 5))
    capitalizeAdd = tk.Button(leftListboxControls, text="Add", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, width=5, command=lambda: addKeywordPrompt("Always Capitalize (L)", "Never Capitalize (L)", capitalizedListbox, options))
    capitalizeAdd.pack(side="left", padx=(25, 20))
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
    tk.Label(rightPane, text="Audio Formatting", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(30, 0), pady=(20, 5), anchor="w")

    # frame for scan filename and tags checkbutton
    scanButtonFrame = tk.Frame(rightPane, bg=bg)
    scanButtonFrame.pack(anchor="w")
    scanFilenameTags = tk.Checkbutton(scanButtonFrame, variable=options["Scan Filename and Tags (B)"], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Scan Filename and Tags (B)', optionsDict, options), bg=bg)
    scanFilenameTags.pack(padx=(30, 0), side="left")
    tk.Label(scanButtonFrame, text="Scan Filename and Tags", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    optionsDict['Scan Filename and Tags (B)'] = scanFilenameTags

    # frame for numbering prefix checkbutton
    prefixButtonFrame = tk.Frame(rightPane, bg=bg)
    prefixButtonFrame.pack(anchor="w")
    numberingPrefix = tk.Checkbutton(prefixButtonFrame, variable=options["Check for Numbering Prefix (B)"], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, "Check for Numbering Prefix (B)", optionsDict, options), bg=bg)
    numberingPrefix.pack(padx=(40, 0), side="left")
    tk.Label(prefixButtonFrame, text="Check for Numbering Prefix", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    optionsDict['Check for Numbering Prefix (B)'] = numberingPrefix

    # frame for hyphen checkbutton
    hyphenButtonFrame = tk.Frame(rightPane, bg=bg)
    hyphenButtonFrame.pack(anchor="w")
    hyphenCheck = tk.Checkbutton(hyphenButtonFrame, variable=options["Check for Extraneous Hyphens (B)"], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, "Check for Extraneous Hyphens (B)", optionsDict, options), bg=bg)
    hyphenCheck.pack(padx=(40, 0), side="left")
    tk.Label(hyphenButtonFrame, text="Check for Extraneous Hyphens", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    optionsDict['Check for Extraneous Hyphens (B)'] = hyphenCheck

    # frame for underscore checkbutton (not yet implemented)
    # underscoreFrame = tk.Frame(rightPane, bg=bg)
    # underscoreFrame.pack(anchor="w")
    # underscoreCheck = tk.Checkbutton(underscoreFrame, variable=options["Check for Underscores (B)"], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, "Check for Underscores (B)", optionsDict, options), bg=bg)
    # underscoreCheck.pack(padx=(40, 0), side="left")
    # tk.Label(underscoreFrame, text="Check for Underscores", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    # optionsDict['Check for Underscores (B)'] = underscoreCheck

    # frame for capitalization checkbutton
    capitalizationButtonFrame = tk.Frame(rightPane, bg=bg)
    capitalizationButtonFrame.pack(anchor="w")
    capitalizationCheck = tk.Checkbutton(capitalizationButtonFrame, variable=options["Check for Capitalization (B)"], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, "Check for Capitalization (B)", optionsDict, options), bg=bg)
    capitalizationCheck.pack(padx=(40, 0), side="left")
    optionsDict['Check for Capitalization (B)'] = capitalizationCheck
    tk.Label(capitalizationButtonFrame, text="Check for Capitalization", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    # frame for file format
    formatFrame = tk.Frame(rightPane, bg=bg)
    formatFrame.pack(anchor="w")
    tk.Label(formatFrame, text="File Format", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(30, 0), pady=(20, 5), anchor="w")

    # frame for dynamic radio button
    dynamicButtonFrame = tk.Frame(formatFrame, bg=bg)
    dynamicButtonFrame.pack(anchor="w")
    tk.Radiobutton(dynamicButtonFrame, variable=options["Audio naming format (S)"], value="Dynamic", command=lambda: namingRadiobutton(CONFIG_FILE, 'Audio naming format (S)', "Dynamic"), activebackground=bg, selectcolor=bg, bg=bg, fg="white").pack(padx=(40, 0), side="left")
    tk.Label(dynamicButtonFrame, text="Dynamic", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    # frame for artist-title radio button
    artistTitleButtonFrame = tk.Frame(formatFrame, bg=bg)
    artistTitleButtonFrame.pack(anchor="w")
    tk.Radiobutton(artistTitleButtonFrame, variable=options["Audio naming format (S)"], value="Artist - Title", command=lambda: namingRadiobutton(CONFIG_FILE, 'Audio naming format (S)', "Artist - Title"), activebackground=bg, selectcolor=bg, bg=bg, fg="white").pack(padx=(40, 0), side="left")
    tk.Label(artistTitleButtonFrame, text="Artist - Title", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    # frame for title radio button
    titleButtonFrame = tk.Frame(formatFrame, bg=bg)
    titleButtonFrame.pack(anchor="w")
    tk.Radiobutton(formatFrame, variable=options["Audio naming format (S)"], value="Title", command=lambda: namingRadiobutton(CONFIG_FILE, 'Audio naming format (S)', "Title"), activebackground=bg, selectcolor=bg, bg=bg, fg="white").pack(padx=(40, 0), side="left")
    tk.Label(formatFrame, text="Title", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    if options["Scan Filename and Tags (B)"].get() == False:
        numberingPrefix.config(state=DISABLED)
        hyphenCheck.config(state=DISABLED)
        capitalizationCheck.config(state=DISABLED)

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
        messagebox.showinfo(parent=popup, title="Error", message=userInput.get().lower() + " is already in the list, you cretin")
        userInput.set("")
    elif userInput.get().lower() in (string.lower() for string in options[alternateTerm]):
        messagebox.showinfo(parent=popup, title="Error", message=userInput.get().lower() + " is already in the other list; keywords cannot be stored in both lists")
        userInput.set("")
    else:
        CONFIG_FILE = resource_path('Settings.txt')
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

#update button according to user input (adding keyword)
def updateInput(input, button):
    if len(input.get()) > 0: button.config(state=NORMAL)
    else: button.config(state=DISABLED)

#remove keyword from list and settings file
def deleteKeyword(term, listbox, index, select, options):
    CONFIG_FILE = resource_path('Settings.txt')
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    originalListValues = options[term]
    newListValues = originalListValues
    originalListValues = ", ".join(originalListValues)
    newListValues.remove(listbox.get(index))
    newListValues.sort()
    newListValues = ", ".join(newListValues)
    with open(CONFIG_FILE, 'wt') as file:
        file.write(config_file.replace(term + ":" + originalListValues, term + ":" + newListValues))
    file.close()
    # remove from listbox
    listbox.delete(index, index)
    #disable delete button
    select.config(state=DISABLED)

def namingRadiobutton(CONFIG_FILE, term, value):
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    if config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] != value:
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term):config_file.index('\n', config_file.index(term) + len(term))]), str(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term)) + 1])) + value))
        file.close()