from tkinter import filedialog
from tkinter.tix import *
import os
import getpass
from PIL import Image, ImageTk
from io import BytesIO

#import classes
from classes.AudioClass import AudioTrack
from classes.scrollbarClass import ScrollableFrame

#import methods
from track_preparation.retrieveInfo import retrieveInfo
from track_scraping.scrapeWeb import scrapeWeb

def fileOption(window, options, imageCounter, CONFIG_FILE):
    window.lift()
    directories = filedialog.askopenfilenames(parent=window, title="Select File")
    if directories != '':
        window.destroy()
        imageSelections = []
        finalResults = []
        webScrapingWindow = Toplevel()
        frame = ScrollableFrame(webScrapingWindow)
        frame.grid(row=0, column=0)
        webScrapingWindow.lift()
        webScrapingWindow.title("Web Scraping Display")
        ws = webScrapingWindow.winfo_screenwidth()  # width of the screen
        hs = webScrapingWindow.winfo_screenheight()  # height of the screen
        x = (ws / 2) - (700 / 2)
        y = (hs / 2) - (715 / 2)
        webScrapingWindow.geometry('%dx%d+%d+%d' % (700, 650, x, y))
        Label(frame.scrollable_frame, text="Beginning web scraping procedure...", wraplength=300, justify='left').pack(anchor='w')
        characters = 0
        thumbnails = []
        for directory in directories:
            var = os.path.basename(directory)
            directory = os.path.dirname(directory)
            #handle FLAC files
            if var.endswith('.flac'):
                audio, var = retrieveInfo(var, directory, frame, webScrapingWindow, options)
                if audio:
                    images = audio.pictures
                    # append thumbnail image to list if artwork exists
                    if len(images) > 0:
                        stream = BytesIO(images[0].data)
                        image = Image.open(stream).convert("RGBA")
                        thumbnails.append(image)
                        stream.close()
                    else:
                        thumbnails.append("NA")
                    track = AudioTrack(audio)
                    results, webScrapingWindow, characters, imageCounter, imageSelection = scrapeWeb(track, audio, var, frame, webScrapingWindow, characters, options, imageCounter)
                    finalResults.append(results)
                    imageSelections.append(imageSelection)
        finalReportWindow = Toplevel()
        webScrapingWindow.lift()
        finalReportWindow.lift()
        finalReportWindow.title("Final Report")
        canvas = Canvas(finalReportWindow)
        finalReport = Frame(canvas)
        scrollbar = Scrollbar(finalReportWindow, orient="vertical", command=canvas.yview)

        ws = finalReportWindow.winfo_screenwidth()  # width of the screen
        hs = finalReportWindow.winfo_screenheight()  # height of the screen
        y = (hs / 2) - (528 / 2)
        if characters <= 40:
            x = (ws / 2) - (450 / 2)
            finalReportWindow.geometry('%dx%d+%d+%d' % (450, 480, x, y))
            if len(directories) > 1:
                y = (hs / 2) - (770 / 2)
                finalReportWindow.geometry('%dx%d+%d+%d' % (450, 700, x, y))
            canvas.create_window(0, 0, window=finalReport)
        else:
            x = (ws / 2) - ((450 + (characters * 1.5)) / 2)
            finalReportWindow.geometry('%dx%d+%d+%d' % (450 + (characters * 1.5), 480, x, y))
            if len(directories) > 1:
                y = (hs / 2) - (770 / 2)
                finalReportWindow.geometry('%dx%d+%d+%d' % (450 + (characters * 1.5), 700, x, y))
            canvas.create_window(0, 0, window=finalReport, anchor='e')
        Label(finalReport, text="Final Report", font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(15, 0))
        for i in range(len(finalResults)):
            Label(finalReport, text=finalResults[i] + '\n').pack(side="top")
            if options["Reverse Image Search (B)"].get() == True and imageCounter >= 1 and len(finalResults) == len(imageSelections):
                #load image
                if imageSelections[i]!='THUMB':
                    fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageSelections[i]) + ".jpg")
                    width, height = fileImageImport.size
                    fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(fileImageImport)
                    fileImage = Label(finalReport, image=photo)
                    fileImage.image = photo
                    fileImage.pack(side="top", padx=(10, 10))
                    #resolution
                    Label(finalReport, text=str(width) + "x" + str(height)).pack(side="top", pady=(5, 10))
                else:
                    fileImageImport =thumbnails[i]
                    width, height = fileImageImport.size
                    fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(fileImageImport)
                    fileImage = Label(finalReport, image=photo)
                    fileImage.image = photo
                    fileImage.pack(side="top", padx=(10, 10))
                    #resolution
                    Label(finalReport, text=str(width) + "x" + str(height)).pack(side="top", pady=(5, 10))
            #load thumbnail image (if image scraping was not performed)
            else:
                if thumbnails[i] == 'NA':
                    Label(finalReport, text="No Artwork Found").pack(side="top", pady=(5,10))
                else:
                    fileImageImport = thumbnails[i]
                    width, height = fileImageImport.size
                    fileImageImport = thumbnails[i].resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(fileImageImport)
                    fileImage = Label(finalReport, image=photo)
                    fileImage.image = photo
                    fileImage.pack(side="top", padx=(10, 10))
                    # resolution
                    Label(finalReport, text=str(width) + "x" + str(height)).pack(side="top", pady=(5, 10))
        # load button and checkbox
        Button(finalReport, text='OK', command=lambda: completeSearch(finalReportWindow, webScrapingWindow, options)).pack(side=TOP, pady=(15, 15))
        Checkbutton(finalReport, text="Close scraping window", var=options["Close Scraping Window (B)"], command=lambda: closeScrapingWindowSelection(CONFIG_FILE)).pack(side=TOP, pady=(0,10))
        finalReportWindow.protocol('WM_DELETE_WINDOW', lambda: closePopup(finalReportWindow, webScrapingWindow))
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrollbar.set)
        canvas.pack(fill='both', expand=True, side='left')
        scrollbar.pack(side="right", fill=Y)


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