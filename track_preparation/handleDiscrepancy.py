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
    y = (hs / 2) - (275 / 2)
    if len(fileTitle) <= 30:
        popup.geometry('%dx%d+%d+%d' % (450, 250, x, y))
    else:
        x = (ws / 2) - ((450 + (len(fileTitle) * 1.5)) / 2)
        popup.geometry('%dx%d+%d+%d' % (450 + (len(fileTitle) * 1.5), 250, x, y))
    Label(popup, text="The title and artist in filename confilct with their corresponding tags.\nChoose between the file and tag name\n").pack(pady=(20, 5))

    # pack a label for each individual word in the file name
    Label(popup, text="File Name", font=("TkDefaultFont", 9, 'bold')).pack()
    filename = (str(fileArtist) + " - " + str(fileTitle)).split(' ')
    filenameContainer = Label(popup, justify="left")
    filenameContainer.pack(pady=(0, 15))
    filenameDict = {}
    for i in range(len(filename)):
        filenameDict[i] = Label(filenameContainer, text=filename[i], borderwidth=-2)
        filenameDict[i].pack(side="left")
        if i != len(filename) - 1: Label(filenameContainer, text='', borderwidth=-2).pack(side="left")

    # pack a label for each individual word in the tag name
    Label(popup, text="Tag Name", font=("TkDefaultFont", 9, 'bold')).pack()
    tagname = (str(tagArtist) + " - " + str(tagTitle)).split(' ')
    tagnameContainer = Label(popup, justify="left")
    tagnameContainer.pack(pady=(0, 10))
    tagnameDict = {}
    for i in range(len(tagname)):
        tagnameDict[i] = Label(tagnameContainer, text=tagname[i], borderwidth=-2)
        tagnameDict[i].pack(side="left")
        if i != len(tagname) - 1: Label(tagnameContainer, text='', borderwidth=-2).pack(side="left")
        # highlight word if it does not match with the current filename
        if len(filename) == len(tagname) and filename[i] != tagname[i]:
            filenameDict[i].configure(background="yellow")
            tagnameDict[i].configure(background="yellow")

    buttons = Frame(popup)
    buttons.pack(side="top")
    Button(buttons, text='File Name', command=lambda: selectFile(popup, webScrapingWindow)).pack(pady=(15, 10), padx=(10, 30), side="left")
    Button(buttons, text='Tag Name', command=lambda: selectTag(popup, webScrapingWindow)).pack(pady=(15, 10), padx=(30, 10), side="left")
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
    y = (hs / 2) - (275 / 2)
    popup.geometry('%dx%d+%d+%d' % (450, 250, x, y))
    if len(fileTitle) > 30:
        x = (ws / 2) - ((450 + (len(fileTitle) * 1.5)) / 2)
        popup.geometry('%dx%d+%d+%d' % (450 + (len(fileTitle) * 1.5), 250, x, y))
    Label(popup, text="The title in the filename conflicts with the title tag.\n Which title should be used?").pack(pady=(20, 10))

    # pack a label for each individual word in the file name
    Label(popup, text="File Name", font=("TkDefaultFont", 9, 'bold')).pack()
    filename = (str(fileTitle)).split(' ')
    filenameContainer = Label(popup, justify="left")
    filenameContainer.pack(pady=(0, 15))
    filenameDict = {}
    for i in range(len(filename)):
        filenameDict[i] = Label(filenameContainer, text=filename[i], borderwidth=-2)
        filenameDict[i].pack(side="left")
        if i != len(filename) - 1: Label(filenameContainer, text='', borderwidth=-2).pack(side="left")

    # pack a label for each individual word in the tag name
    Label(popup, text="Tag Name", font=("TkDefaultFont", 9, 'bold')).pack()
    tagname = (str(tagTitle)).split(' ')
    tagnameContainer = Label(popup, justify="left")
    tagnameContainer.pack(pady=(0, 10))
    tagnameDict = {}
    for i in range(len(tagname)):
        tagnameDict[i] = Label(tagnameContainer, text=tagname[i], borderwidth=-2)
        tagnameDict[i].pack(side="left")
        if i != len(tagname) - 1: Label(tagnameContainer, text='', borderwidth=-2).pack(side="left")
        # highlight word if it does not match with the current filename
        if len(filename) == len(tagname) and filename[i] != tagname[i]:
            filenameDict[i].configure(background="yellow")
            tagnameDict[i].configure(background="yellow")

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