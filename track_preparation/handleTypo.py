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
    y = (hs / 2) - (280 / 2)
    if len(str(artist) + " - " + str(title)) <= 30:
        popup.geometry('%dx%d+%d+%d' % (450, 180, x, y))
    else:
        x = (ws / 2) - ((450 + (len(str(artist) + " - " + str(title)) * 1.5)) / 2)
        popup.geometry('%dx%d+%d+%d' % (450 + (len(str(artist) + " - " + str(title)) * 1.5), 180, x, y))
    Label(popup, text="A potential typo was found in the filename. Change\n\n" + str(artist) + " - " + str(title) + "\nto\n" + str(newArtist) + " - " + str(newTitle) + "?").pack(pady=(20, 5))
    buttons = Frame(popup)
    buttons.pack(side="top")
    Button(buttons, text='Yes', command=lambda: setChange(popup, webScrapingWindow)).pack(pady=(15, 10), padx=(10, 30), side="left")
    Button(buttons, text='No', command=lambda: closePopup(popup, webScrapingWindow)).pack(pady=(15, 10), padx=(30, 10), side="left")
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