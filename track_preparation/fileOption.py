from tkinter import filedialog
from tkinter.tix import *
import os
import getpass
from PIL import Image, ImageTk

#import classes
from classes.AudioClass import AudioTrack
from classes.scrollbarClass import ScrollableFrame

#import methods
from track_preparation.retrieveInfo import retrieveInfo
from track_scraping.searchTags import searchTags

def fileOption(window, options, imageCounter, CONFIG_FILE):
    window.lift()
    directories = filedialog.askopenfilenames(parent=window, title="Select File")
    if directories != '':
        window.destroy()
        imageSelection = 0
        results = ''
        webScrapingWindow = Toplevel()
        frame = ScrollableFrame(webScrapingWindow)
        frame.grid(row=0, column=0)
        webScrapingWindow.lift()
        webScrapingWindow.title("Web Scraping Display")
        ws = webScrapingWindow.winfo_screenwidth()  # width of the screen
        hs = webScrapingWindow.winfo_screenheight()  # height of the screen
        x = (ws / 2) - (700 / 2)
        y = (hs / 2) - (750 / 2)
        webScrapingWindow.geometry('%dx%d+%d+%d' % (700, 650, x, y))
        Label(frame.scrollable_frame, text="Beginning web scraping procedure...", wraplength=300, justify='left').pack(anchor='w')
        row = 0
        characters = 0
        for directory in directories:
            var = os.path.basename(directory)
            directory = os.path.dirname(directory)
            #handle FLAC files
            if var.endswith('.flac'):
                row+=1
                audio, var = retrieveInfo(var, directory, frame, webScrapingWindow, options)
                if audio:
                    track = AudioTrack(audio)
                    finalResults, webScrapingWindow, characters, imageCounter, imageSelection = searchTags(track, audio, var, frame, webScrapingWindow, characters, options, imageCounter)
                    results += finalResults + '\n'
        finalReportWindow = Toplevel()
        webScrapingWindow.lift()
        finalReportWindow.lift()
        finalReportWindow.title("Final Report")
        finalReportWindow.columnconfigure(0, weight=1)
        ws = finalReportWindow.winfo_screenwidth()  # width of the screen
        hs = finalReportWindow.winfo_screenheight()  # height of the screen
        y = (hs / 2) - (200+((row-1)*75)/ 2)
        if characters <= 40:
            x = (ws / 2) - (430 / 2)
            finalReportWindow.geometry('%dx%d+%d+%d' % (450, 250+((row-1)*75), x, y))
            if options["Reverse Image Search (B)"].get() == True and imageCounter >= 1:
                y = (hs / 2) - ((550 + ((row - 1) * 75)) / 2)
                finalReportWindow.geometry('%dx%d+%d+%d' % (430, 450 + ((row - 1) * 75), x, y))
        else:
            x = (ws / 2) - ((430 + (characters * 1.5)) / 2)
            finalReportWindow.geometry('%dx%d+%d+%d' % (450 + (characters*1.5), 250 + ((row - 1) * 75), x, y))
            if options["Reverse Image Search (B)"].get() == True and imageCounter >= 1:
                y = (hs / 2) - ((550 + ((row - 1) * 75)) / 2)
                finalReportWindow.geometry('%dx%d+%d+%d' % (430 + (characters * 1.5), 450 + ((row - 1) * 75), x, y))
        if options["Reverse Image Search (B)"].get()==True and imageCounter >= 1:
            Label(finalReportWindow, text="Final Report", font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(15, 0))
            Label(finalReportWindow, text=results).pack(side="top")
            #load image
            fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageSelection) + ".jpg")
            fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(fileImageImport)
            fileImage = Label(finalReportWindow, image=photo)
            fileImage.image = photo
            fileImage.pack(side="top", padx=(10, 10))
            #load button and checkbox
            Button(finalReportWindow, text='OK', command=lambda: completeSearch(finalReportWindow, webScrapingWindow, options)).pack(side="top", pady=(15, 10))
            Checkbutton(finalReportWindow, text="Close scraping window", var=options["Close Scraping Window (B)"], command=lambda: closeScrapingWindowSelection(CONFIG_FILE)).pack(side="top")
            finalReportWindow.protocol('WM_DELETE_WINDOW', lambda: closePopup(finalReportWindow, webScrapingWindow))
        else:
            Label(finalReportWindow, text="Final Report", font=("TkDefaultFont", 9, 'bold')).grid(row=0, column=0, pady=(15,0))
            Label(finalReportWindow, text=results).grid(row=1, column=0)
            Button(finalReportWindow, text='OK', command=lambda: completeSearch(finalReportWindow, webScrapingWindow, options)).grid(row=2, column=0, pady=(0, 5))
            Checkbutton(finalReportWindow, text="Close scraping window", var=options["Close Scraping Window (B)"], command=lambda: closeScrapingWindowSelection(CONFIG_FILE)).grid(row=3, column=0)
            finalReportWindow.protocol('WM_DELETE_WINDOW', lambda: closePopup(finalReportWindow, webScrapingWindow))

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