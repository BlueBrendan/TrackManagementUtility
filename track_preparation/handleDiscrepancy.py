from tkinter import Toplevel, Button, Label, Frame

#global variables
file = False
tag = False

def handleArtistTitleDiscrepancy(fileArtist, tagArtist, fileTitle, tagTitle, webScrapingWindow):
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
        file = False
        return "file"
    elif tag == True:
        tag = False
        return "tag"

def handleTitleDiscrepancy(fileTitle, tagTitle, webScrapingWindow):
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
        file=False
        return "file"
    elif tag==True:
        tag=False
        return "tag"

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