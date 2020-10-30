import tkinter as tk
from tkinter.tix import *

# import methods
from options.checkboxHandling import checkbox

# global variables
# main bg color
bg = "#282f3b"
# secondary color
secondary_bg = "#364153"
# invalid selection color
invalid_bg = "#801212"
optionsDict = {}

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
    unselectedListbox = tk.Listbox(leftListbox, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, highlightbackground="black", highlightcolor="grey", selectbackground=bg, activestyle="none")

    tk.Label(rightListbox, text="Selected Tags", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack()
    selectedListbox = tk.Listbox(rightListbox, font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, highlightbackground="black", highlightcolor="grey", selectbackground=bg, activestyle="none")
    comprehensiveList = ['Artist', 'Album', 'Album Artist', 'BPM', 'Comment', 'Compilation', 'Copyright', 'Discnumber', 'Genre', 'Key', 'Release_Date', 'Title', 'ReplayGain']

    # insert tags in their corresponding listbox
    for tag in comprehensiveList:
        if tag not in options['Selected Tags (L)']:
            #remove underscore
            if tag == "Release_Date": unselectedListbox.insert(END, "Release Date")
            else: unselectedListbox.insert(END, tag)
        else:
            if tag == "Release_Date": selectedListbox.insert(END, "Release Date")
            else: selectedListbox.insert(END, tag)
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
    deleteUnselected = tk.Checkbutton(tagCheckboxFrame, variable=options["Delete Unselected Tags (B)"], activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Delete Unselected Tags (B)', optionsDict, options), bg=bg)
    deleteUnselected.pack(padx=(20, 0), pady=(20, 0), side="left")
    tk.Label(tagCheckboxFrame, text="Delete Unselected Tags from File", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(pady=(20, 0), side="left")
    optionsDict['Delete Unselected Tags (B)'] = deleteUnselected

#handle listbox click interaction
def selectTag(firstListbox, secondListbox, list, select, deselect):
    if len(firstListbox.curselection()) > 0:
        index = int(firstListbox.curselection()[0])
        tag = firstListbox.get(index)
        tag = tag.replace(' ', "_")
        #lock1 artist and title tags
        if tag == "Artist" or tag=="Title":
            firstListbox.config(selectbackground=invalid_bg)
            select.config(state=DISABLED)
            deselect.config(state=DISABLED)
        else:
            firstListbox.config(selectbackground=bg)
            if tag in list:
                select.config(state=DISABLED)
                deselect.config(state=NORMAL, command=lambda: disableTag(firstListbox, secondListbox, tag, index, list, deselect))
            else:
                select.config(state=NORMAL, command=lambda: enableTag(firstListbox, secondListbox, tag, index, list, select))
                deselect.config(state=DISABLED)

def enableTag(firstListbox, secondListbox, tag, index, list, button):
    #first listbox is the unselected listbox, second listbox is the selected listbox
    global tagList, CONFIG
    config_file = open(CONFIG, 'r').read()
    firstListbox.delete(index, index)
    if tag == "Release_Date": secondListbox.insert(END, "Release Date")
    else: secondListbox.insert(END, tag)
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
    if tag == "Release_Date": secondListbox.insert(END, "Release Date")
    else: secondListbox.insert(END, tag)
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