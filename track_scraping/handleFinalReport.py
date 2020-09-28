import tkinter as tk
from tkinter.tix import *
from PIL import Image, ImageTk
import getpass
import os

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

def handleFinalReport(finalResults, directories, characters, imageCounter, imageSelections, thumbnails, webScrapingWindow, options, CONFIG_FILE):
        finalReportWindow = tk.Toplevel()
        finalReportWindow.title("Final Report")
        finalReportWindow.configure(bg=bg)
        ws = finalReportWindow.winfo_screenwidth()  # width of the screen
        hs = finalReportWindow.winfo_screenheight()  # height of the screen
        y = (hs / 2) - (605 / 2)
        x = (ws / 2) - (550 / 2)
        finalReportWindow.geometry('%dx%d+%d+%d' % (550, 550, x, y))
        if characters > 40:
            x = (ws / 2) - ((550 + (characters * 1.5)) / 2)
            finalReportWindow.geometry('%dx%d+%d+%d' % (550 + (characters * 1.5), 550, x, y))
        tk.Label(finalReportWindow, text="Final Report", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="top", pady=(25, 10))
        for i in range(len(finalResults)):
            tk.Label(finalReportWindow, text=finalResults[i] + '\n', font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="top")
            # load non-thumbnailimage
            if options["Reverse Image Search (B)"].get() == True and imageCounter >= 1 and imageSelections[i] != 'THUMB':
                fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageSelections[i]) + ".jpg")
                width, height = fileImageImport.size
                fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(fileImageImport)
                fileImage = tk.Label(finalReportWindow, image=photo, bg=bg)
                fileImage.image = photo
                fileImage.pack(side="top", padx=(10, 10))
                #resolution
                tk.Label(finalReportWindow, text=str(width) + "x" + str(height), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="top", pady=(5, 10))
            #load thumbnail image
            else:
                if thumbnails[i] == 'NA': tk.Label(finalReportWindow, text="No Artwork Found", font=("Proxima Nova Rg", 11)).pack(side="top", pady=(5,20))
                else:
                    fileImageImport = thumbnails[i]
                    width, height = fileImageImport.size
                    fileImageImport = thumbnails[i].resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(fileImageImport)
                    fileImage = tk.Label(finalReportWindow, image=photo, bg=bg)
                    fileImage.image = photo
                    fileImage.pack(side="top", padx=(10, 10))
                    # resolution
                    tk.Label(finalReportWindow, text=str(width) + "x" + str(height), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="top", pady=(5, 20))
        # load button and checkbox
        tk.Button(finalReportWindow, text='OK', command=lambda: completeSearch(finalReportWindow, webScrapingWindow, options), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side=TOP, pady=(15, 15))
        closeWindowButtonFrame = tk.Frame(finalReportWindow, bg=bg)
        closeWindowButtonFrame.pack()
        tk.Checkbutton(closeWindowButtonFrame, var=options["Close Scraping Window (B)"], command=lambda: closeScrapingWindowSelection(CONFIG_FILE), bg=bg).pack(side="left", pady=(0,10))
        tk.Label(closeWindowButtonFrame, text="Close scraping window", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left", pady=(0,10))
        finalReportWindow.protocol('WM_DELETE_WINDOW', lambda: closePopup(finalReportWindow, webScrapingWindow))
        finalReportWindow.lift()

#handle subdirectory selection
def closeScrapingWindowSelection(CONFIG_FILE):
    config_file = open(CONFIG_FILE, 'r').read()
    #if true, turn option to false
    term = "Close Scraping Window (B)"
    if config_file[config_file.index(term) + len(term)+1:config_file.index('\n', config_file.index(term) + len(term))]=="True":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term)+1:config_file.index(':', config_file.index(term))+1]) + "True", str(str(config_file[config_file.index(term)+1:config_file.index(':', config_file.index(term))+1])) + "False"))
        file.close()
    #if false, turn option to true
    elif config_file[config_file.index(term) + len(term)+1:config_file.index('\n', config_file.index(term) + len(term))]=="False":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term)+1:config_file.index(':', config_file.index(term)) + 1]) + "False", str(str(config_file[config_file.index(term)+1:config_file.index(':', config_file.index(term)) + 1])) + "True"))
        file.close()

def completeSearch(finalReportWindow, webScrapingWindow, options):
    finalReportWindow.destroy()
    webScrapingWindow.lift()
    if options["Close Scraping Window (B)"].get() != False:
        webScrapingWindow.destroy()
    # delete all images in temp if both revese image search and delete stored image options are both true
    if options["Reverse Image Search (B)"].get() == True and options["Delete Stored Images (B)"].get() == True:
        images = os.listdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/")
        for image in images:
            os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(image))

def closePopup(popup, webScrapingWindow):
    popup.destroy()
    webScrapingWindow.lift()