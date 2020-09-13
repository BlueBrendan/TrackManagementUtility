from tkinter import filedialog
from tkinter.tix import *
import os
import getpass

#import classes
from classes.AudioClass import AudioTrack
from classes.scrollbarClass import ScrollableFrame
from classes.scrollbarClass import SmallScrollableFrame

#import methods
from track_preparation.retrieveInfo import retrieveInfo
from track_scraping.searchTags import searchTags

def directoryOption(window, options, imageCounter):
    window.lift()
    directory = filedialog.askdirectory(parent=window, title="Select Directory")
    if directory != '':
        window.destroy()
        results = []
        characters = 0
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
        finalReport, webScrapingWindow, characters, imageSelection = directorySearch(directory, results, frame, webScrapingWindow, characters, options, imageCounter)
        finalReportWindow = Toplevel()
        frame = SmallScrollableFrame(finalReportWindow)
        frame.pack(anchor="center")
        webScrapingWindow.lift()
        finalReportWindow.lift()
        finalReportWindow.title("Final Report")
        ws = finalReportWindow.winfo_screenwidth()  # width of the screen
        hs = finalReportWindow.winfo_screenheight()  # height of the screen
        y = (hs / 2) - (320 / 2)
        x = (ws / 2) - (450 / 2)
        finalReportWindow.geometry('%dx%d+%d+%d' % (450, 250, x, y))
        # if characters <= 60:
        # else:
        #     x = (ws / 2) - ((450 + (characters * 1.5)) / 2)
        #     finalReportWindow.geometry('%dx%d+%d+%d' % ((450 + (characters*1.5)), 250, x, y))
        #     frame.config(width=450 + (characters*1.5))
        Label(frame.small_scrollable_frame, text="Final Report", font=("TkDefaultFont", 9, 'bold')).pack(anchor="center")
        for i in range(len(finalReport)):
            Label(frame.small_scrollable_frame, text=finalReport[i]).pack(anchor="center")
            Label(frame.small_scrollable_frame, text="\n").pack(anchor="center")
        # empty directory provided
        if len(finalReport) == 0:
            Label(finalReportWindow, text="No tracks were found in the provided directory").pack()
        Button(frame.small_scrollable_frame, text='OK', command=lambda: completeSearch(finalReportWindow, webScrapingWindow, options)).pack(anchor="center")
        finalReportWindow.protocol('WM_DELETE_WINDOW', lambda: closePopup(finalReportWindow, webScrapingWindow))

def directorySearch(directory, results, frame, webScrapingWindow, characters, options, imageCounter):
    imageSelection = 0
    files = os.listdir(directory)
    for var in files:
        if os.path.isdir(directory + '/' + var) and options["Subdirectories (B)"].get() == True:
            directorySearch(directory + '/' + var, results, frame, webScrapingWindow, characters, options, imageCounter)
        else:
            #handle FLAC files
            if var.endswith(".flac"):
                audio = retrieveInfo(var, directory, frame, webScrapingWindow, options)
                if audio:
                    track = AudioTrack(audio)
                    finalResults, webScrapingWindow, characters, imageCounter, imageSelection = searchTags(track, audio, var, frame, webScrapingWindow, characters, options, imageCounter)
                    results.append(finalResults)
    return results, webScrapingWindow, characters, imageSelection

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