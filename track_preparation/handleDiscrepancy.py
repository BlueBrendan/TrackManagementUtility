import tkinter as tk
import getpass

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

#global variables
file = False
tag = False

def handleArtistTitleDiscrepancy(fileArtist, tagArtist, fileTitle, tagTitle):
    global file
    global tag
    popup = tk.Toplevel()
    popup.title("Tag Filename Mismatch - Title")
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (550 / 2)
    y = (hs / 2) - (330 / 2)
    if len(fileTitle) <= 30: popup.geometry('%dx%d+%d+%d' % (550, 300, x, y))
    else:
        x = (ws / 2) - ((450 + (len(fileTitle) * 1.5)) / 2)
        popup.geometry('%dx%d+%d+%d' % (550 + (len(fileTitle) * 1.5), 300, x, y))
    popup.config(bg=bg)
    tk.Label(popup, text="The title and artist in filename conflict with their corresponding tags.\nChoose between the file and tag name\n", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(pady=(20, 10))
    # pack a label for each individual word in the file name
    tk.Label(popup, text="File Name", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack()
    filename = (str(fileArtist) + " - " + str(fileTitle)).split(' ')
    filenameContainer = tk.Label(popup, justify="left", bg=bg)
    filenameContainer.pack(pady=(0, 15))
    filenameDict = {}
    for i in range(len(filename)):
        filenameDict[i] = tk.Label(filenameContainer, text=filename[i], borderwidth=-2,  font=("Proxima Nova Rg", 11), fg="white", bg=bg)
        filenameDict[i].pack(side="left")
        if i != len(filename) - 1: tk.Label(filenameContainer, text='', borderwidth=-2,  font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    # pack a label for each individual word in the tag name
    tk.Label(popup, text="Tag Name",  font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(pady=(20, 0))
    tagname = (str(tagArtist) + " - " + str(tagTitle)).split(' ')
    tagnameContainer = tk.Label(popup, justify="left", bg=bg)
    tagnameContainer.pack(pady=(0, 10))
    tagnameDict = {}
    for i in range(len(tagname)):
        tagnameDict[i] = tk.Label(tagnameContainer, text=tagname[i], borderwidth=-2,  font=("Proxima Nova Rg", 11), fg="white", bg=bg)
        tagnameDict[i].pack(side="left")
        if i != len(tagname) - 1: tk.Label(tagnameContainer, text='', borderwidth=-2,  font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
        # highlight word if it does not match with the current filename
        if len(filename) == len(tagname) and filename[i] != tagname[i]:
            filenameDict[i].configure(fg="black", background="yellow")
            tagnameDict[i].configure(fg="black", background="yellow")
    buttons = tk.Frame(popup, bg=bg)
    buttons.pack(side="top")
    tk.Button(buttons, text='File Name', command=lambda: selectFile(popup),  font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(pady=(25, 10), padx=(10, 30), side="left")
    tk.Button(buttons, text='Tag Name', command=lambda: selectTag(popup),  font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(pady=(25, 10), padx=(30, 10), side="left")
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())
    popup.iconbitmap(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/favicon.ico")
    popup.wait_window()
    if file == True:
        file = False
        return "file"
    elif tag == True:
        tag = False
        return "tag"

def handleTitleDiscrepancy(fileTitle, tagTitle):
    global file
    global tag
    popup = tk.Toplevel()
    popup.title("Tag Filename Mismatch - Title")
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (500 / 2)
    y = (hs / 2) - (330 / 2)
    popup.geometry('%dx%d+%d+%d' % (500, 300, x, y))
    if len(fileTitle) > 30:
        x = (ws / 2) - ((450 + (len(fileTitle) * 1.5)) / 2)
        popup.geometry('%dx%d+%d+%d' % (500 + (len(fileTitle) * 1.5), 300, x, y))
    tk.Label(popup, text="The title in the filename conflicts with the title tag.\n Which title should be used?",  font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(pady=(20, 10))
    popup.config(bg=bg)
    # pack a label for each individual word in the file name
    tk.Label(popup, text="File Name",  font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack()
    filename = (str(fileTitle)).split(' ')
    filenameContainer = tk.Label(popup, justify="left", bg=bg)
    filenameContainer.pack(pady=(0, 15))
    filenameDict = {}
    for i in range(len(filename)):
        filenameDict[i] = tk.Label(filenameContainer, text=filename[i], borderwidth=-2, font=("Proxima Nova Rg", 11), fg="white", bg=bg)
        filenameDict[i].pack(side="left")
        if i != len(filename) - 1: tk.Label(filenameContainer, text='', borderwidth=-2, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    # pack a label for each individual word in the tag name
    tk.Label(popup, text="Tag Name", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(pady=(20, 0))
    tagname = (str(tagTitle)).split(' ')
    tagnameContainer = tk.Label(popup, justify="left", bg=bg)
    tagnameContainer.pack(pady=(0, 10))
    tagnameDict = {}
    for i in range(len(tagname)):
        tagnameDict[i] = tk.Label(tagnameContainer, text=tagname[i], borderwidth=-2, font=("Proxima Nova Rg", 11), fg="white", bg=bg)
        tagnameDict[i].pack(side="left")
        if i != len(tagname) - 1: tk.Label(tagnameContainer, text='', borderwidth=-2, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
        # highlight word if it does not match with the current filename
        if len(filename) == len(tagname) and filename[i] != tagname[i]:
            filenameDict[i].configure(fg="black", background="yellow")
            tagnameDict[i].configure(fg="black", background="yellow")

    buttons = tk.Frame(popup, bg=bg)
    buttons.pack(side="top")
    tk.Button(buttons, text='File', command=lambda: selectFile(popup), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(pady=(25, 10), padx=(10, 30), side="left")
    tk.Button(buttons, text='Tag', command=lambda: selectTag(popup), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(pady=(25, 10), padx=(30, 10), side="left")
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())
    popup.iconbitmap(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/favicon.ico")
    popup.wait_window()
    if file==True:
        file=False
        return "file"
    elif tag==True:
        tag=False
        return "tag"

def selectFile(popup):
    global file
    file = True
    popup.destroy()

def selectTag(popup):
    global tag
    tag = True
    popup.destroy()