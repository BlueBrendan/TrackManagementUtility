import tkinter as tk
import getpass

#handleTypo handles popup interaction that happens when potential typos/spelling errors are found
# If the user identifies the name as a typo, handleTypo will return new artist and title parameters that are used to initiate the audio file in its respective format

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

#global variable
change = False
capitalize = False
uncapitalize = False
word = ''

def handleTypo(artist, newArtist, title, newTitle, type, options):
    global change, word, capitalize, uncapitalize
    popup = tk.Toplevel()
    popup.title("Potential Typo - " + type)
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (450 / 2)
    y = (hs / 2) - (352 / 2)
    popup.geometry('%dx%d+%d+%d' % (450, 320, x, y))
    if type == "Capitalization":
        x = (ws / 2) - (550 / 2)
        popup.geometry('%dx%d+%d+%d' % (550, 320, x, y))
    popup.configure(bg=bg)
    if len(str(artist) + " - " + str(title)) > 50:
        x = (ws / 2) - ((450 + (len(str(artist) + " - " + str(title)) * 1.5)) / 2)
        popup.geometry('%dx%d+%d+%d' % (450 + (len(str(artist) + " - " + str(title)) * 1.5), 320, x, y))
        if type == "Capitalization":
            x = (ws / 2) - ((550 + (len(str(artist) + " - " + str(title)) * 1.5)) / 2)
            popup.geometry('%dx%d+%d+%d' % (550 + (len(str(artist) + " - " + str(title)) * 1.5), 320, x, y))
    tk.Label(popup, text="A potential typo/error was found. \nAccept or reject the proposed filename\n", font=("Proxima Nova Rg", 14), fg="white", bg=bg).pack(pady=(20, 10))
    # pack a label for each individual word in the current filename
    tk.Label(popup, text="Current filename", font=("Proxima Nova Rg", 12), fg="white", bg=bg).pack()
    currentFilename = (str(artist) + " - " + str(title)).split(' ')
    currentFilenameContainer = tk.Label(popup, justify="left",  fg="white", bg=bg)
    currentFilenameContainer.pack(pady=(0,25))
    currentFilenameDict = {}
    for i in range(len(currentFilename)):
        currentFilenameDict[i] = tk.Label(currentFilenameContainer, text=currentFilename[i], borderwidth=-2, font=("Proxima Nova Rg", 11), fg="white", bg=bg)
        currentFilenameDict[i].pack(side="left")
        if i != len(currentFilename) - 1: tk.Label(currentFilenameContainer, text='', borderwidth=-2, fg="white", bg=bg).pack(side="left")
    #pack a label for each individual word in the proposed filename
    tk.Label(popup, text="Proposed filename", font=("Proxima Nova Rg", 12), fg="white", bg=bg).pack(pady=(10, 0))
    newFilename = (str(newArtist) + " - " + str(newTitle)).split(' ')
    newFilenameContainer = tk.Label(popup, justify="left",  fg="white", bg=bg)
    newFilenameContainer.pack(pady=(0, 10))
    newFilenameDict = {}
    for i in range(len(newFilename)):
        newFilenameDict[i] = tk.Label(newFilenameContainer, text=newFilename[i], borderwidth=-2, font=("Proxima Nova Rg", 11), fg="white", bg=bg)
        newFilenameDict[i].pack(side="left")
        if i!=len(newFilename)-1: tk.Label(newFilenameContainer, text='', borderwidth=-2, fg="white", bg=bg).pack(side="left")
        #highlight word if it does not match with the current filename; only highlight the first mismatched word
        if len(currentFilename) == len(newFilename) and currentFilename[i] != newFilename[i] and word=='':
            word = str(newFilenameDict[i]["text"])
            currentFilenameDict[i].configure(fg="black", bg="yellow")
            newFilenameDict[i].configure(fg="black", bg="yellow")
    buttons = tk.Frame(popup, bg=bg)
    buttons.pack(side="top")
    tk.Button(buttons, text='Accept', command=lambda: setChange(popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(25, 10), padx=(10, 30), side="left")
    tk.Button(buttons, text='Reject', command=lambda: closePopup(popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(25, 10), padx=(30, 10), side="left")
    if type == "Capitalization":
        tk.Button(buttons, text="Always Accept " + "(" + word + ")", command=lambda: addCapitalizedList(word, popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(25, 10), padx=(30, 10), side="left")
        tk.Button(buttons, text="Always Reject " + "(" + word.lower() + ")", command=lambda: addUncapitalizedList(word, popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(25, 10), padx=(30, 10), side="left")
        popup.wait_window()
        if capitalize: options["Always Capitalize (L)"].append(word.capitalize())
        elif uncapitalize: options["Never Capitalize (L)"].append(word.lower())
        capitalize = False
        uncapitalize = False
        word = ''
    else:
        popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())
        popup.wait_window()
    if change:
        artist = newArtist
        title = newTitle
        return artist, title, options, True
    return artist, title, options, False

def setChange(popup):
    global change
    change = True
    popup.destroy()

def closePopup(popup):
    global change
    change = False
    popup.destroy()

def addCapitalizedList(keyword, popup):
    global change, capitalize, uncapitalize
    change = False
    capitalize = True
    uncapitalize = False
    CONFIG_FILE = r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt"
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    term = "Always Capitalize (L)"
    originalListValues = str(config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))])
    newListValues = originalListValues
    if originalListValues == '': newListValues += keyword.capitalize()
    else:newListValues  += ", " + keyword.capitalize()
    with open(CONFIG_FILE, 'wt') as file:
        file.write(config_file.replace(term + ":" + str(config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]), term + ":" + str(newListValues)))
    file.close()
    popup.destroy()

def addUncapitalizedList(keyword, popup):
    global change, capitalize, uncapitalize
    change = False
    capitalize = False
    uncapitalize = True
    CONFIG_FILE = r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt"
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    term = "Never Capitalize (L)"
    originalListValues = str(config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))])
    newListValues = originalListValues
    if originalListValues == '': newListValues += keyword.lower()
    else:newListValues += ", " + keyword.lower()
    with open(CONFIG_FILE, 'wt') as file:
        file.write(config_file.replace(term + ":" + str(config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]), term + ":" + str(newListValues)))
    file.close()
    popup.destroy()