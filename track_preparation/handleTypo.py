from mutagen.flac import FLAC
from tkinter import Toplevel, Label, Button, messagebox, Frame
import os

#handleTypo handles popup interaction that happens when potential typos/spelling errors are found
# If the user identifies the name as a typo, the file will be renamed and artist tag will be reassigned

#global variable
change = False
file = False
tag = False

def handleArtistTitleDiscrepancy(fileArtist, tagArtist, fileTitle, tagTitle, audio, filename, directory, webScrapingWindow):
    global file
    global tag
    popup = Toplevel()
    popup.title("Tag Filename Mismatch - Title")
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (450 / 2)
    y = (hs / 2) - (280 / 2)
    if len(fileTitle) <= 30:
        popup.geometry('%dx%d+%d+%d' % (450, 180, x, y))
    else:
        x = (ws / 2) - ((450 + (len(fileTitle) * 1.5)) / 2)
        popup.geometry('%dx%d+%d+%d' % (450 + (len(fileTitle) * 1.5), 180, x, y))
    Label(popup, text="The title and artist in filename confilct with their corresponding tags.\nWhich artist and title should be used?\n").pack(pady=(20, 5))
    Label(popup, text="File Name: " + fileArtist + " - " + fileTitle + "\nTag Name: " + tagArtist + " - " + tagTitle, justify="left").pack()
    buttons = Frame(popup)
    buttons.pack(side="top")
    Button(buttons, text='File', command=lambda: selectFile(popup, webScrapingWindow)).pack(pady=(15, 10), padx=(10, 30), side="left")
    Button(buttons, text='Tag', command=lambda: selectTag(popup, webScrapingWindow)).pack(pady=(15, 10), padx=(30, 10), side="left")
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())
    popup.wait_window()
    if file == True:
        audio['artist'] = fileArtist
        audio['title'] = fileTitle
        audio.save()
        file = False
    elif tag == True:
        extension = filename[filename.rfind('.'):]
        os.rename(directory + '/' + filename, str(directory) + '/' + str(tagArtist) + " - " + str(tagTitle) + extension)
        filename = str(tagArtist) + " - " + str(tagTitle) + extension
        audio = FLAC(str(directory) + '/' + filename)
        tag = False
    return audio, filename

def handleTitleDiscrepancy(fileTitle, tagTitle, audio, filename, directory, webScrapingWindow):
    global file
    global tag
    popup = Toplevel()
    popup.title("Tag Filename Mismatch - Title")
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (450 / 2)
    y = (hs / 2) - (280 / 2)
    if len(fileTitle) <= 30:
        popup.geometry('%dx%d+%d+%d' % (450, 180, x, y))
    else:
        x = (ws / 2) - ((450 + (len(fileTitle) * 1.5)) / 2)
        popup.geometry('%dx%d+%d+%d' % (450 + (len(fileTitle) * 1.5), 180, x, y))
    Label(popup, text="The title in the filename conflicts with the title tag.\n Which title should be used?").pack(pady=(20, 5))
    Label(popup, text="File: " + fileTitle + "\nTag: " + tagTitle).pack()
    buttons = Frame(popup)
    buttons.pack(side="top")
    Button(buttons, text='File', command=lambda: selectFile(popup, webScrapingWindow)).pack(pady=(15, 10), padx=(10, 30), side="left")
    Button(buttons, text='Tag', command=lambda: selectTag(popup, webScrapingWindow)).pack(pady=(15, 10), padx=(30, 10), side="left")
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())
    popup.wait_window()
    if file==True:
        audio['title'] = fileTitle
        audio.save()
        file=False
    elif tag==True:
        extension = filename[filename.rfind('.'):]
        os.rename(directory + '/' + filename, str(directory) + '/' + str(tagTitle) + extension)
        filename = str(tagTitle) + extension
        audio = FLAC(str(directory) + '/' + filename)
        tag=False
    return audio, filename

def selectFile(popup, webScrapingWindow):
    global file
    file = True
    popup.destroy()
    webScrapingWindow.lift()

def selectTag(popup, webScrapingWindow):
    global tag
    tag = True
    popup.destroy()
    webScrapingWindow.lift()

def handleTypo(audio, artist, newArtist, title, newTitle, webScrapingWindow, directory, filename, extension, format, type):
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
        audio, filename = rename(directory, filename, artist, title, extension, format)
    return artist, title, audio, filename

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
        try:
            os.rename(directory + '/' + filename, str(directory) + '/' + str(artist) + ' - ' + str(title) + extension)
            filename = str(artist) + ' - ' + str(title) + extension
            audio = FLAC(str(directory) + '/' + str(artist) + ' - ' + str(title) + extension)
            audio['artist'] = artist
            audio['title'] = title
            audio.save()
            return audio, filename
        except PermissionError:messagebox.showinfo("Permission Error", "File cannot be renamed, it may still be open")
    elif format == "Title":
        try:
            os.rename(directory + '/' + filename, str(directory) + '/' + str(title) + extension)
            filename = str(title) + extension
            audio = FLAC(str(directory) + '/' + str(title) + extension)
            audio['artist'] = artist
            audio['title'] = title
            audio.save()
            return audio, filename
        except PermissionError:messagebox.showinfo("Permission Error", "File cannot be renamed, it may still be open")