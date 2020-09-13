from mutagen.flac import FLAC
from tkinter import Toplevel, Label, Button
import os

#handleTypo handles the popup window that occurs when a number and period is fine in the artist name.
# If the user identifies the name as a typo, the file will be renamed and artist tag will be reassigned

#global variable
changeName = False

def handleTypo(artist, title, var, artistPostfix, webScrapingWindow, audio, directory, frame, window):
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
    Label(popup, text="A potential typo was found in the file name. Rename\n\n" + str(artist) + " - " + str(title) + "\nto\n" + str(artistPostfix) + ' - ' + str(title) + "?").grid(row=0, column=1, columnspan=2, pady=(10, 0))
    Button(popup, text='Yes', command=lambda: resetArtistName(audio, artist, artistPostfix, popup, webScrapingWindow, directory, frame, window)).grid(row=1, column=1, pady=(20, 10))
    Button(popup, text='No', command=lambda: closePopup(popup, webScrapingWindow)).grid(row=1, column=2)
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())
    popup.wait_window()
    if changeName:
        audio = FLAC(str(directory) + '/' + str(artistPostfix) + " - " + str(audio["title"][0]) + ".flac")
        var = str(artistPostfix) + " - " + str(audio["title"][0]) + ".flac"
        audio["artist"] = artistPostfix
        audio.pprint()
        audio.save()
    else:
        audio["artist"] = artist
        audio.pprint()
        audio.save()
    return audio, var

def resetArtistName(audio, artist, artistPostfix, popup, webScrapingWindow, directory, frame, window):
    global changeName
    try:
        os.rename(directory + '/' + str(artist) + " - " + str(audio["title"][0]) + ".flac", str(directory) + '/' + str(artistPostfix) + " - " + str(audio["title"][0]) + ".flac")
        changeName = True
    except PermissionError:
        Label(frame.scrollable_frame, text="The file is open in another application, close it and try again").pack(anchor='w')
        window.update()
    popup.destroy()
    webScrapingWindow.lift()

def closePopup(popup, webScrapingWindow):
    popup.destroy()
    webScrapingWindow.lift()