from tkinter import Toplevel, Label, Button, Frame

#handleTypo handles popup interaction that happens when potential typos/spelling errors are found
# If the user identifies the name as a typo, handleTypo will return new artist and title parameters that are used to initiate the audio file in its respective format

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

#global variable
change = False

def handleTypo(artist, newArtist, title, newTitle, type):
    global change
    popup = Toplevel()
    popup.title("Potential Typo - " + type)
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (450 / 2)
    y = (hs / 2) - (352 / 2)
    popup.geometry('%dx%d+%d+%d' % (450, 320, x, y))
    popup.configure(bg=bg)
    if len(str(artist) + " - " + str(title)) > 50:
        x = (ws / 2) - ((450 + (len(str(artist) + " - " + str(title)) * 1.5)) / 2)
        popup.geometry('%dx%d+%d+%d' % (450 + (len(str(artist) + " - " + str(title)) * 1.5), 250, x, y))
    Label(popup, text="A potential typo/error was found. \nAccept or reject the proposed filename\n", font=("Proxima Nova Rg", 14), fg="white", bg=bg).pack(pady=(20, 10))
    # pack a label for each individual word in the current filename
    Label(popup, text="Current filename", font=("Proxima Nova Rg", 12), fg="white", bg=bg).pack()
    currentFilename = (str(artist) + " - " + str(title)).split(' ')
    currentFilenameContainer = Label(popup, justify="left",  fg="white", bg=bg)
    currentFilenameContainer.pack(pady=(0,25))
    currentFilenameDict = {}
    for i in range(len(currentFilename)):
        currentFilenameDict[i] = Label(currentFilenameContainer, text=currentFilename[i], borderwidth=-2, font=("Proxima Nova Rg", 11), fg="white", bg=bg)
        currentFilenameDict[i].pack(side="left")
        if i != len(currentFilename) - 1: Label(currentFilenameContainer, text='', borderwidth=-2, fg="white", bg=bg).pack(side="left")

    #pack a label for each individual word in the proposed filename
    Label(popup, text="Proposed filename", font=("Proxima Nova Rg", 12), fg="white", bg=bg).pack(pady=(10, 0))
    newFilename = (str(newArtist) + " - " + str(newTitle)).split(' ')
    newFilenameContainer = Label(popup, justify="left",  fg="white", bg=bg)
    newFilenameContainer.pack(pady=(0, 10))
    newFilenameDict = {}
    for i in range(len(newFilename)):
        newFilenameDict[i] = Label(newFilenameContainer, text=newFilename[i], borderwidth=-2, font=("Proxima Nova Rg", 11), fg="white", bg=bg)
        newFilenameDict[i].pack(side="left")
        if i!=len(newFilename)-1: Label(newFilenameContainer, text='', borderwidth=-2, fg="white", bg=bg).pack(side="left")
        #highlight word if it does not match with the current filename
        if len(currentFilename) == len(newFilename) and currentFilename[i] != newFilename[i]: newFilenameDict[i].configure(fg="black", background="yellow")

    buttons = Frame(popup, bg=bg)
    buttons.pack(side="top")
    Button(buttons, text='Accept', command=lambda: setChange(popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(25, 10), padx=(10, 30), side="left")
    Button(buttons, text='Reject', command=lambda: closePopup(popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(25, 10), padx=(30, 10), side="left")
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())
    popup.wait_window()
    if change:
        artist = newArtist
        title = newTitle
        return artist, title

def setChange(popup):
    global change
    change = True
    popup.destroy()

def closePopup(popup):
    global change
    change = False
    popup.destroy()