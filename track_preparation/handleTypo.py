from mutagen.flac import FLAC
from tkinter import Toplevel, Label, Button, messagebox, Frame
import os

#handleTypo handles popup interaction that happens when potential typos/spelling errors are found
# If the user identifies the name as a typo, handleTypo will return new artist and title parameters that are used to initiate the audio file in its respective format

#global variable
change = False

def handleTypo(artist, newArtist, title, newTitle, webScrapingWindow, type):
    global change
    popup = Toplevel()
    popup.title("Potential Typo - " + type)
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (450 / 2)
    y = (hs / 2) - (275 / 2)
    popup.geometry('%dx%d+%d+%d' % (450, 250, x, y))
    if len(str(artist) + " - " + str(title)) > 50:
        x = (ws / 2) - ((450 + (len(str(artist) + " - " + str(title)) * 1.5)) / 2)
        popup.geometry('%dx%d+%d+%d' % (450 + (len(str(artist) + " - " + str(title)) * 1.5), 250, x, y))
    Label(popup, text="A potential typo/error was found. Accept or reject the proposed filename\n").pack(pady=(20, 5))
    # pack a label for each individual word in the current filename
    Label(popup, text="Current filename", font=("TkDefaultFont", 9, 'bold')).pack()
    currentFilename = (str(artist) + " - " + str(title)).split(' ')
    currentFilenameContainer = Label(popup, justify="left")
    currentFilenameContainer.pack(pady=(0,15))
    currentFilenameDict = {}
    for i in range(len(currentFilename)):
        currentFilenameDict[i] = Label(currentFilenameContainer, text=currentFilename[i], borderwidth=-2)
        currentFilenameDict[i].pack(side="left")
        if i != len(currentFilename) - 1: Label(currentFilenameContainer, text='', borderwidth=-2).pack(side="left")

    #pack a label for each individual word in the proposed filename
    Label(popup, text="Proposed filename", font=("TkDefaultFont", 9, 'bold')).pack()
    newFilename = (str(newArtist) + " - " + str(newTitle)).split(' ')
    newFilenameContainer = Label(popup, justify="left")
    newFilenameContainer.pack(pady=(0, 10))
    newFilenameDict = {}
    for i in range(len(newFilename)):
        newFilenameDict[i] = Label(newFilenameContainer, text=newFilename[i], borderwidth=-2)
        newFilenameDict[i].pack(side="left")
        if i!=len(newFilename)-1: Label(newFilenameContainer, text='', borderwidth=-2).pack(side="left")
        #highlight word if it does not match with the current filename
        if len(currentFilename) == len(newFilename) and currentFilename[i] != newFilename[i]: newFilenameDict[i].configure(background="yellow")

    buttons = Frame(popup)
    buttons.pack(side="top")
    Button(buttons, text='Accept', command=lambda: setChange(popup, webScrapingWindow)).pack(pady=(15, 10), padx=(10, 30), side="left")
    Button(buttons, text='Reject', command=lambda: closePopup(popup, webScrapingWindow)).pack(pady=(15, 10), padx=(30, 10), side="left")
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())
    popup.wait_window()
    if change:
        artist = newArtist
        title = newTitle
        return artist, title

def setChange(popup, webScrapingWindow):
    global change
    change = True
    popup.destroy()
    webScrapingWindow.lift()

def closePopup(popup, webScrapingWindow):
    global change
    change = False
    popup.destroy()
    webScrapingWindow.lift()