from mutagen.flac import FLAC
from tkinter import Toplevel, Label, Button
import os

#handleTypo handles the popup window that occurs when a number and period is fine in the artist name.
# If the user identifies the name as a typo, the file will be renamed and artist tag will be reassigned

#global variable
changeName = False

def handleTypo(artist, artistPostfix, title, webScrapingWindow):
    global changeName
    popup = Toplevel()
    popup.title("Potential Typo")
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (450 / 2)
    y = (hs / 2) - (280 / 2)
    if len(str(artist) + " - " + str(title)) <= 30:
        popup.geometry('%dx%d+%d+%d' % (450, 180, x, y))
    else:
        x = (ws / 2) - ((450 + (len(str(artist) + " - " + str(title)) * 1.5)) / 2)
        popup.geometry('%dx%d+%d+%d' % (450 + (len(str(artist) + " - " + str(title)) * 1.5), 180, x, y))
    popup.columnconfigure(1, weight=1)
    popup.columnconfigure(2, weight=1)
    Label(popup, text="A potential typo was found in the artist name. Rename\n\n" + str(artist) + "\nto\n" + str(artistPostfix) + "?").grid(row=0, column=1, columnspan=2, pady=(10, 0))
    Button(popup, text='Yes', command=lambda: resetArtistName(popup, webScrapingWindow)).grid(row=1, column=1, pady=(20, 10))
    Button(popup, text='No', command=lambda: closePopup(popup, webScrapingWindow)).grid(row=1, column=2)
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())
    popup.wait_window()
    if changeName:
        artist = artistPostfix
    return artist

def resetArtistName(popup, webScrapingWindow):
    global changeName
    changeName = True
    popup.destroy()
    webScrapingWindow.lift()

def closePopup(popup, webScrapingWindow):
    popup.destroy()
    webScrapingWindow.lift()