from tkinter.tix import *
import getpass
from PIL import Image, ImageTk

#import methods
from track_preparation.fileOption import fileOption
from track_preparation.directoryOption import directoryOption

#global variables
imageCounter = 0

#driver code
def selectFileOrDirectory(options, CONFIG_FILE):
    global imageCounter
    window = Toplevel()
    window.title("Scan Tags Selection")
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (520 / 2)
    y = (hs / 2) - (400 / 2)
    window.geometry('%dx%d+%d+%d' % (520, 300, x, y))
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)
    Label(window, text="What type of item do you want to search for?").grid(row=0, column=1, columnspan=2, pady=(10, 35))
    #load file icon
    fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Images/fileIcon.png")
    fileImageImport = fileImageImport.resize((150, 150), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(fileImageImport)
    fileImage = Label(window, image=photo)
    fileImage.image = photo
    fileImage.grid(row=1, column=1)
    #load directory icon
    directoryImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Images/folderIcon.png")
    directoryImageImport = directoryImageImport.resize((150,150), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(directoryImageImport)
    directoryImage = Label(window, image=photo)
    directoryImage.image = photo
    directoryImage.grid(row=1, column=2)
    Button(window, text="Files", command=lambda: scanTagsOnline("file", window, options, imageCounter, CONFIG_FILE)).grid(row=2, column=1, pady=(5, 3))
    Button(window, text="Directories", command=lambda: scanTagsOnline("directory", window, options, imageCounter, CONFIG_FILE)).grid(row=2,column=2, pady=(5, 3))

def scanTagsOnline(type, window, options, imageCounter, CONFIG_FILE):
    if type=="file":
        fileOption(window, options, imageCounter, CONFIG_FILE)
    elif type=="directory":
        #scan for a directory
        directoryOption(window, options, imageCounter)




