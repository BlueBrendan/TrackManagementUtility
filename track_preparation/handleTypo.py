from mutagen.flac import FLAC
from tkinter import Toplevel, Label, Button, messagebox
import os

#handleTypo handles popup interaction that happens when potential typos/spelling errors are found
# If the user identifies the name as a typo, the file will be renamed and artist tag will be reassigned

#global variable
change = False

def handleTypo(artist, newArtist, title, newTitle, webScrapingWindow, directory, filename, extension, format, type):
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
    popup.columnconfigure(1, weight=1)
    popup.columnconfigure(2, weight=1)
    Label(popup, text="A potential typo was found in the artist name. Change\n\n" + str(artist) + " - " + str(title) + "\nto\n" + str(newArtist) + " - " + str(newTitle) + "?").grid(row=0, column=1, columnspan=2, pady=(10, 0))
    Button(popup, text='Yes', command=lambda: setChange(popup, webScrapingWindow)).grid(row=1, column=1, pady=(20, 10))
    Button(popup, text='No', command=lambda: closePopup(popup, webScrapingWindow)).grid(row=1, column=2)
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())
    popup.wait_window()
    if change:
        artist = newArtist
        title = newTitle
        rename(directory, filename, artist, title, extension, format)
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

def rename(directory, filename, artist, title, extension, format):
    if format == "Artist - Title":
        try:os.rename(directory + '/' + filename, str(directory) + '/' + str(artist) + ' - ' + str(title) + extension)
        except PermissionError:messagebox.showinfo("Permission Error", "File cannot be renamed, it may still be open")
    elif format == "Title":
        try:os.rename(directory + '/' + filename, str(directory) + '/' + str(title) + extension)
        except PermissionError:messagebox.showinfo("Permission Error", "File cannot be renamed, it may still be open")