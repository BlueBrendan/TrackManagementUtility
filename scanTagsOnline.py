import os
import requests
from bs4 import BeautifulSoup
from mutagen.flac import FLAC
from mutagen.id3 import ID3, TIT2, TKEY
from statistics import mode
from collections import Counter
from tkinter import filedialog
from tkinter.tix import *
import getpass
import scrapy
from selenium import webdriver
from PIL import Image, ImageTk

from junodownloadSearch import junodownloadSearch
from beatportSearch import beatportSearch
from discogsSearch import discogsSearch

#global variables
newArtistName = ''
newTitleName = ''
cancel = False

class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="w")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        canvas.config(width=680, height=500)
        scrollbar.pack(side="right", fill="y")

def selectFileOrDirectory(CONFIG_FILE, subdirectories, closeScrapingWindow):
    #TODO
    #Implement typo/misspell detection system
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

    Button(window, text="Files", command=lambda: scanTagsOnline(subdirectories, "file", window, closeScrapingWindow, CONFIG_FILE)).grid(row=2, column=1, pady=(5, 3))
    Button(window, text="Directories", command=lambda: scanTagsOnline(subdirectories, "directory", window, closeScrapingWindow, CONFIG_FILE)).grid(row=2,column=2, pady=(5, 3))

def completeSearch(finalReportWindow, webScrapingWindow, closeScrapingWindow):
    finalReportWindow.destroy()
    webScrapingWindow.lift()
    if closeScrapingWindow.get()!=False:
        webScrapingWindow.destroy()

def scanTagsOnline(subdirectories, type, window, closeScrapingWindow, CONFIG_FILE):
    global cancel
    if type=="file":
        #scan for a file
        window.lift()
        directories = filedialog.askopenfilenames(parent=window, title="Select File")
        if directories != '':
            window.destroy()
            results = ''
            webScrapingWindow = Toplevel()
            frame = ScrollableFrame(webScrapingWindow)
            frame.grid(row=0, column=0)
            webScrapingWindow.lift()
            webScrapingWindow.title("Web Scraping Display")
            ws = webScrapingWindow.winfo_screenwidth()  # width of the screen
            hs = webScrapingWindow.winfo_screenheight()  # height of the screen
            x = (ws / 2) - (700 / 2)
            y = (hs / 2) - (800 / 2)
            webScrapingWindow.geometry('%dx%d+%d+%d' % (700, 650, x, y))
            Label(frame.scrollable_frame, text="Beginning web scraping procedure...", wraplength=300, justify='left').pack(anchor='w')
            row = 0
            characters = 0
            for directory in directories:
                var = os.path.basename(directory)
                #handle FLAC files
                if var.endswith('.flac'):
                    row+=1
                    result, webScrapingWindow, characters = scanFLACFile(var, os.path.dirname(directory), frame, webScrapingWindow, characters)
                    results += result + '\n\n'
                #handle MP3 files
                # elif var.endswith('.mp3'):
                #     row+=1
                #     result, webScrapingWindow, characters = scanMP3File(var, os.path.dirname(directory), frame, webScrapingWindow, characters)
                #     results += result + '\n\n'
                # only print a report if the process was not cancelled
            if cancel==False:
                finalReportWindow = Toplevel()
                webScrapingWindow.lift()
                finalReportWindow.lift()
                finalReportWindow.title("Final Report")
                finalReportWindow.columnconfigure(0, weight=1)
                ws = finalReportWindow.winfo_screenwidth()  # width of the screen
                hs = finalReportWindow.winfo_screenheight()  # height of the screen
                y = (hs / 2) - (200+((row-1)*75)/ 2)
                if characters <= 40:
                    x = (ws / 2) - (450 / 2)
                    finalReportWindow.geometry('%dx%d+%d+%d' % (450, 250+((row-1)*100), x, y))
                else:
                    x = (ws / 2) - ((450 + (characters * 1.5)) / 2)
                    finalReportWindow.geometry('%dx%d+%d+%d' % (450 + (characters*1.5), 250 + ((row - 1) * 100), x, y))
                Label(finalReportWindow, text="Final Report", font=("TkDefaultFont", 9, 'bold')).grid(row=0, column=0, pady=(15,0))
                Label(finalReportWindow, text=results).grid(row=1, column=0)
                Button(finalReportWindow, text='OK', command=lambda: completeSearch(finalReportWindow, webScrapingWindow, closeScrapingWindow)).grid(row=2, column=0, pady=(0, 5))
                Checkbutton(finalReportWindow, text="Close scraping window", var=closeScrapingWindow, command=lambda: closeScrapingWindowSelection(CONFIG_FILE)).grid(row=3, column=0)
                finalReportWindow.protocol('WM_DELETE_WINDOW', lambda: closeFinalReport(finalReportWindow, webScrapingWindow))
    elif type=="directory":
        #scan for a directory
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
            y = (hs / 2) - (800 / 2)
            webScrapingWindow.geometry('%dx%d+%d+%d' % (700, 650, x, y))
            Label(frame.scrollable_frame, text="Beginning web scraping procedure...", wraplength=300, justify='left').pack(anchor='w')
            finalReport, webScrapingWindow, characters = directorySearch(directory, subdirectories, results, frame, webScrapingWindow, characters)
            if cancel == False:
                finalReportWindow = Toplevel()
                webScrapingWindow.lift()
                finalReportWindow.lift()
                finalReportWindow.title("Final Report")
                finalReportWindow.columnconfigure(0, weight=1)
                ws = finalReportWindow.winfo_screenwidth()  # width of the screen
                hs = finalReportWindow.winfo_screenheight()  # height of the screen
                y = (hs / 2) - (800 / 2)
                if characters <= 60:
                    x = (ws / 2) - (450 / 2)
                    finalReportWindow.geometry('%dx%d+%d+%d' % (450, 650, x, y))
                else:
                    x = (ws / 2) - ((450 + (characters * 1.5)) / 2)
                    finalReportWindow.geometry('%dx%d+%d+%d' % ((450 + (characters*1.5)), 650, x, y))
                Label(finalReportWindow, text="Final Report", font=("TkDefaultFont", 9, 'bold')).grid(row=0, column=0, pady=(15, 0))
                row=0
                for i in range(len(finalReport)):
                    Label(finalReportWindow, text=finalReport[i]).grid(row=i+1, column=0, pady=(15,10))
                    row+=1
                #empty directory provided
                if len(finalReport)==0:
                    Label(finalReportWindow, text="No tracks were found in the provided directory").grid(row=1, column=0, pady=(15, 10))
                    row += 1
                Button(finalReportWindow, text='OK', command=lambda: completeSearch(finalReportWindow, webScrapingWindow, closeScrapingWindow)).grid(row=row+1, column=0, pady=(15,10))
                finalReportWindow.protocol('WM_DELETE_WINDOW', lambda: closeFinalReport(finalReportWindow, webScrapingWindow))

def directorySearch(directory, subdirectories, results, frame, webScrapingWindow, characters):
    global newArtistName, newTitleName, cancel
    files = os.listdir(directory)
    for var in files:
        if os.path.isdir(directory + '/' + var) and subdirectories.get() == True:
            directorySearch(directory + '/' + var, subdirectories, results, frame, webScrapingWindow, characters)
        else:
            #handle FLAC files
            if var.endswith(".flac"):
                result, webScrapingWindow, characters = scanFLACFile(var, directory, frame, webScrapingWindow, characters)
                results.append(result)
        newArtistName = ''
        newTitleName = ''
    return results, webScrapingWindow, characters


def resetArtistName(artistPostfix, popup):
    global newArtistName
    newArtistName = artistPostfix
    popup.destroy()

def resetTitleName(titlePostfix, popup):
    global newTitleName
    newTitleName = titlePostfix
    popup.destroy()

def onClose(popup):
    global cancel
    cancel = True
    popup.destroy()

def scanFLACFile(var, directory, frame, webScrapingWindow, characters):
    global newArtistName, cancel
    audio = checkFileValidity(directory, var, frame, webScrapingWindow)
    if type(audio)==str:
        return audio, webScrapingWindow
    # check if artist and title are in filename
    filename = var
    if ' - ' in var:
        artist = var.split(' - ')[0]
        title = var.split(' - ')[1][:-5]
        # scan artist for numbering prefix
        if ' ' in artist or '.' in artist:
            if ' ' in artist:
                artistPrefix = artist.split(' ', 1)[0]
                artistPostfix = artist.split(' ', 1)[1]
            else:
                artistPrefix = artist.split('.')[0]
                artistPostfix = artist.split('.')[1]
            for character in artistPrefix:
                if character.isdigit() or character == '.':
                    popup = Toplevel()
                    popup.title("Potential Misspell in File Name")
                    ws = popup.winfo_screenwidth()  # width of the screen
                    hs = popup.winfo_screenheight()  # height of the screen
                    x = (ws / 2) - (450 / 2)
                    y = (hs / 2) - (280 / 2)
                    print(len(str(artist) + " - " + str(title)))
                    if len(str(artist) + " - " + str(title)) <= 30:
                        popup.geometry('%dx%d+%d+%d' % (450, 180, x, y))
                    else:
                        x = (ws / 2) - ((450 + (len(str(artist) + " - " + str(title)) * 1.5)) / 2)
                        popup.geometry('%dx%d+%d+%d' % (450 + (len(str(artist) + " - " + str(title)) * 1.5), 180, x, y))
                    popup.columnconfigure(1, weight=1)
                    popup.columnconfigure(2, weight=1)
                    Label(popup, text="A potential typo was found in the file name. Rename\n\n" + str(artist) + " - " + str(title) + "\nto\n" + str(artistPostfix) + ' - ' + str(title) + "?").grid(row=0, column=1,columnspan=2,pady=(10, 0))
                    Button(popup, text='Yes', command=lambda: resetArtistName(artistPostfix, popup)).grid(row=1, column=1,pady=(20, 10))
                    Button(popup, text='No', command=popup.destroy).grid(row=1, column=2)
                    popup.protocol("WM_DELETE_WINDOW", lambda: onClose(popup))
                    popup.wait_window()
                    break
    # check file tags for artist
    else:
        if audio['artist'] == '':
            print("No artist information found in file")
            return
        artist = str(audio['artist'])[2:-2]
        title = var[:-5]
        if ' ' in title or '.' in title:
            if ' ' in artist:
                titlePrefix = title.split(' ', 1)[0]
                titlePostfix = title.split(' ', 1)[1]
            else:
                titlePrefix = title.split('.')[0]
                titlePostfix = title.split('.')[1]
            for character in titlePrefix:
                if character.isdigit() or character == '.':
                    popup = Toplevel()
                    popup.title("Potential Misspell in File Name")
                    ws = popup.winfo_screenwidth()  # width of the screen
                    hs = popup.winfo_screenheight()  # height of the screen
                    x = (ws / 2) - (450 / 2)
                    y = (hs / 2) - (280 / 2)
                    if len(str(artist) + " - " + str(title)) <= 30:
                        popup.geometry('%dx%d+%d+%d' % (450, 180, x, y))
                    else:
                        x = (ws / 2) - ((450 + (len(str(artist) + " - " + str(title))*1.5)) / 2)
                        popup.geometry('%dx%d+%d+%d' % (450 + (len(str(artist) + " - " + str(title))*1.5), 180, x, y))
                    popup.columnconfigure(1, weight=1)
                    popup.columnconfigure(2, weight=1)
                    Label(popup,text="A potential typo was found in the file name. Rename\n\n" + str(title) + "\nto\n" + str(titlePostfix) + "?").grid(row=0, column=1,columnspan=2,pady=(10, 0))
                    Button(popup, text='Yes', command=lambda: resetTitleName(titlePostfix, popup)).grid(row=1, column=1,pady=(20, 10))
                    Button(popup, text='No', command=popup.destroy).grid(row=1, column=2)
                    popup.protocol("WM_DELETE_WINDOW", lambda: onClose(popup))
                    popup.wait_window()
                    break
    if cancel==True:
        return
    if newArtistName != '':
        renameArtist(directory, var, newArtistName, title, frame, webScrapingWindow)
        artist = newArtistName
        filename = newArtistName + ' - ' + title + '.flac'
    elif newTitleName != '':
        renameFile(directory, var, newTitleName+".flac", frame, webScrapingWindow)
        title = newTitleName
        filename = newTitleName + '.flac'
    if "featuring" in artist:
        artist = artist.replace("featuring", "feat.")
        renameArtist(directory, var, artist, title, frame, webScrapingWindow)
    if '’' in filename:
        filename = filename.replace("’", "'")
        renameFile(directory, var, filename, frame, webScrapingWindow)
    audio["artist"] = artist
    audio["title"] = title
    audio.pprint()
    audio.save()

    interestParameters = ['artist', 'title', 'date', 'bpm', 'initialkey', 'genre', 'replaygain_track_gain']
    fileParameters = []
    for x in audio:
        fileParameters.append(x)
    for x in fileParameters:
        #delete extraneous tags
        if x not in interestParameters:
            print("Deleting " + str(x))
            audio[x]= ""
            audio.pop(x)
            audio.save()
    for x in interestParameters:
        #add tags of interest if missing
        if x not in fileParameters:
            audio[x] = ""
            audio.save()
    search = str(artist) + " - " + str(title)
    #clean search query of ampersands
    ampersand = re.finditer("&", search)
    ampersandPositions = [match.start() for match in ampersand]
    for var in ampersandPositions:
        search = search[0:var] + " " + search[var + 1:]
    yearList = []
    BPMList = []
    keyList = []
    genreList = []
    imageList = []
    #build list of artist and track title variations to prepare for scraping
    artistVariations, titleVariations = buildVariations(artist,title)
    #Perform scraping
    headers = {'User-Agent': "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1b3pre) Gecko/20090109 Shiretoko/3.1b3pre"}

    #web scraping
    #junodownload
    yearList, BPMList, genreList, imageList = junodownloadSearch(artist, title, yearList, BPMList, genreList, imageList, artistVariations, titleVariations, headers, search, frame, webScrapingWindow)
    # window.update()
    # # #beatport
    yearList, BPMList, keyList, genreList, imageList = beatportSearch(artist, title, yearList, BPMList, keyList, genreList, imageList, artistVariations, titleVariations, headers, search, frame, webScrapingWindow)
    # #discogs
    yearList, genreList, imageList, window = discogsSearch(artist, title, yearList, genreList, imageList, artistVariations, titleVariations, headers, search, frame, webScrapingWindow)
    #spotify
    #apple music
    finalResults, webScrapingWindow, characters = buildTrackReport(yearList, BPMList, keyList, genreList, imageList, artist, title, audio, webScrapingWindow, characters)
    return finalResults, webScrapingWindow, characters

# def scanMP3File(var, directory, frame, webScrapingWindow, characters):
#     global newArtistName, cancel
#     # check if artist and title are in filename
#     filename = var
#     if ' - ' in var:
#         artist = var.split(' - ')[0]
#         title = var.split(' - ')[1][:-5]
#         # scan artist for numbering prefix
#         if ' ' in artist or '.' in artist:
#             if ' ' in artist:
#                 artistPrefix = artist.split(' ', 1)[0]
#                 artistPostfix = artist.split(' ', 1)[1]
#             else:
#                 artistPrefix = artist.split('.')[0]
#                 artistPostfix = artist.split('.')[1]
#             for character in artistPrefix:
#                 if character.isdigit() or character == '.':
#                     popup = Toplevel()
#                     popup.title("Potential Misspell in File Name")
#                     ws = popup.winfo_screenwidth()  # width of the screen
#                     hs = popup.winfo_screenheight()  # height of the screen
#                     x = (ws / 2) - (450 / 2)
#                     y = (hs / 2) - (280 / 2)
#                     popup.geometry('%dx%d+%d+%d' % (450, 180, x, y))
#                     popup.columnconfigure(1, weight=1)
#                     popup.columnconfigure(2, weight=1)
#                     Label(popup,text="A potential typo was found in the file name. Rename\n\n" + str(artist) + " - " + str(title) + "\nto\n" + str(artistPostfix) + ' - ' + str(title) + "?").grid(row=0, column=1,columnspan=2,pady=(10, 0))
#                     Button(popup, text='Yes', command=lambda: resetArtistName(artistPostfix, popup)).grid(row=1, column=1,pady=(20, 10))
#                     Button(popup, text='No', command=popup.destroy).grid(row=1, column=2)
#                     popup.protocol("WM_DELETE_WINDOW", lambda: onClose(popup))
#                     popup.wait_window()
#                     break
#     # check file tags for artist
#     else:
#         try: audio = ID3(str(directory) + '/' + str(var))
#         except:
#             print("Invalid or corrupt file")
#             return
#         if audio['TPE1'].text[0] == '':
#             print("No artist information found in file")
#             return
#
#         title = var[:-5]
#         if ' ' in title or '.' in title:
#             if ' ' in artist:
#                 titlePrefix = title.split(' ', 1)[0]
#                 titlePostfix = title.split(' ', 1)[1]
#             else:
#                 titlePrefix = title.split('.')[0]
#                 titlePostfix = title.split('.')[1]
#             for character in titlePrefix:
#                 if character.isdigit() or character == '.':
#                     popup = Toplevel()
#                     popup.title("Potential Misspell in File Name")
#                     ws = popup.winfo_screenwidth()  # width of the screen
#                     hs = popup.winfo_screenheight()  # height of the screen
#                     x = (ws / 2) - (450 / 2)
#                     y = (hs / 2) - (280 / 2)
#                     popup.geometry('%dx%d+%d+%d' % (450, 180, x, y))
#                     popup.columnconfigure(1, weight=1)
#                     popup.columnconfigure(2, weight=1)
#                     Label(popup,text="A potential typo was found in the file name. Rename\n\n" + str(title) + "\nto\n" + str(titlePostfix) + "?").grid(row=0, column=1,columnspan=2,pady=(10, 0))
#                     Button(popup, text='Yes', command=lambda: resetTitleName(titlePostfix, popup)).grid(row=1, column=1,pady=(20, 10))
#                     Button(popup, text='No', command=popup.destroy).grid(row=1, column=2)
#                     popup.protocol("WM_DELETE_WINDOW", lambda: onClose(popup))
#                     popup.wait_window()
#                     break
#     if cancel==True:
#         return
#     if newArtistName != '':
#         try: os.rename(directory + '/' + var, directory + '/' + newArtistName + ' - ' + title + '.flac')
#         except PermissionError:
#             print("The file is open in another application, close it and try again")
#             return
#         artist = newArtistName
#         filename = newArtistName + ' - ' + title + '.flac'
#     elif newTitleName != '':
#         try: os.rename(directory + '/' + var, directory + '/' + newTitleName + '.flac')
#         except PermissionError:
#             print("The file is open in another application, close it and try again")
#             return
#         title = newTitleName
#         filename = newTitleName + '.flac'
#
#     if "featuring" in artist:
#         artist = artist.replace("featuring", "feat.")
#         try: os.rename(directory + '/' + var, str(directory) + str(artist) + " - " + str(title) + ".flac")
#         except PermissionError:
#             print("The file is open in another application, close it and try again")
#             return
#     if '’' in filename:
#         filename = filename.replace("’", "'")
#         try:
#             (directory + '/' + var, str(directory) + '/' + str(filename))
#         except PermissionError:
#             print("The file is open in another application, close it and try again")
#             return
#     try: audio = FLAC(str(directory) + '/' + str(filename))
#     except:
#         print("Invalid or corrupt file")
#         return
#     audio["artist"] = artist
#     audio["title"] = title
#     audio.pprint()
#     audio.save()
#
#     interestParameters = ['artist', 'title', 'date', 'bpm', 'initialkey', 'genre', 'replaygain_track_gain']
#     fileParameters = []
#     for x in audio:
#         fileParameters.append(x)
#     for x in fileParameters:
#         #delete extraneous tags
#         if x not in interestParameters:
#             print("Deleting " + str(x))
#             audio[x]= ""
#             audio.pop(x)
#             audio.save()
#     for x in interestParameters:
#         #add tags of interest if missing
#         if x not in fileParameters:
#             audio[x] = ""
#             audio.save()
#     search = str(artist) + " - " + str(title)
#     #clean search query of ampersands
#     ampersand = re.finditer("&", search)
#     ampersandPositions = [match.start() for match in ampersand]
#     for var in ampersandPositions:
#         search = search[0:var] + " " + search[var + 1:]
#     yearList = []
#     BPMList = []
#     keyList = []
#     genreList = []
#     imageList = []
#     #build list of artist and track title variations to prepare for scraping
#     artistVariations, titleVariations = buildVariations(artist,title)
#     #Perform scraping
#     headers = {'User-Agent': "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1b3pre) Gecko/20090109 Shiretoko/3.1b3pre"}
#
#     #web scraping
#     #junodownload
#     yearList, BPMList, genreList, imageList = junodownloadSearch(artist, title, yearList, BPMList, genreList, imageList, artistVariations, titleVariations, headers, search, frame, webScrapingWindow)
#     # window.update()
#     # # #beatport
#     yearList, BPMList, keyList, genreList, imageList = beatportSearch(artist, title, yearList, BPMList, keyList, genreList, imageList, artistVariations, titleVariations, headers, search, frame, webScrapingWindow)
#     # #discogs
#     yearList, genreList, imageList, window = discogsSearch(artist, title, yearList, genreList, imageList, artistVariations, titleVariations, headers, search, frame, webScrapingWindow)
#     #spotify
#     #apple music
#     finalResults, webScrapingWindow, characters = buildTrackReport(yearList, BPMList, keyList, genreList, imageList, artist, title, audio, webScrapingWindow, characters)
#     return finalResults, webScrapingWindow

def buildTrackReport(yearList, BPMList, keyList, genreList, imageList, artist, title, audio, webScrapingWindow, characters):
    yearValue = False
    BPMValue = False
    keyValue = False
    genreValue = False
    year = ''
    BPM = ''
    key = ''
    genre = ''
    images = ''
    # check year for false values
    if len(yearList) != 0:
        commonYear = [word for word, word_count in Counter(yearList).most_common(5)]
        year = commonYear[0]
        yearValue = True
        if len(commonYear) > 1:
            for i in range(len(commonYear) - 1):
                # prioritize older years to avoid quoting re-releases
                if len(yearList) <= 5:
                    if int(commonYear[0]) > int(commonYear[i + 1]) and yearList.count(
                            commonYear[0]) <= yearList.count(commonYear[i + 1]) * 2:
                        year = commonYear[i + 1]
                else:
                    if int(commonYear[0]) > int(commonYear[i + 1]) and yearList.count(
                            commonYear[0]) <= yearList.count(commonYear[i + 1]) * 2 and yearList.count(commonYear[0]) > 1:
                        year = commonYear[i + 1]
    # check BPM for false values
    if len(BPMList) != 0:
        commonBPM = ([word for word, word_count in Counter(BPMList).most_common(3)])
        BPM = commonBPM[0]
        BPMValue = True
        if len(commonBPM) > 1:
            if int(commonBPM[0]) * 2 == int(commonBPM[1]) and int(commonBPM[0]) < 85:
                BPM = commonBPM[1]
    if len(keyList)!=0:
        key = str(mode(keyList))
        keyValue = True
    if len(genreList)!=0:
        genre = str(mode(genreList))
        genreValue = True
    if len(imageList)!=0:
        for i in range(len(imageList)):
            images += imageList[i] + ", "
    #update audio tags
    if yearValue == True or BPMValue == True or keyValue == True or genreValue == True:
        if audio['date']!=[''] or audio['bpm']!=[''] or audio['initialkey']!=[''] or audio['genre']!=['']:
            if str(audio['DATE'])[2:-2]!=str(year) or str(audio['bpm'])[2:-2]!=str(BPM) or str(audio['initialkey'])[2:-2]!=key or str(audio['genre'])[2:-2]!=genre:
                window = Toplevel()
                window.lift()
                window.title("Conflicting Tags")
                ws = window.winfo_screenwidth()  # width of the screen
                hs = window.winfo_screenheight()  # height of the screen
                x = (ws / 2) - (550 / 2)
                y = (hs / 2) - (320 / 2)
                if len(str(artist) + " - " + str(title)) <= 30:
                    window.geometry('%dx%d+%d+%d' % (550, 220, x, y))
                else:
                    x = (ws / 2) - ((550 + (len(str(artist) + " - " + str(title)) * 1.5)) / 2)
                    window.geometry('%dx%d+%d+%d' % (550 + (len(str(artist) + " - " + str(title)) * 1.5), 220, x, y))
                window.columnconfigure(0, weight=1)
                window.columnconfigure(1, weight=1)
                window.columnconfigure(2, weight=1)
                window.columnconfigure(3, weight=1)
                Label(window, text="Conflicting tags in " + str(artist) + " - " + str(title), font=("TkDefaultFont", 9, 'bold')).grid(row=0, column=0, columnspan=4, pady=(10,0))
                Label(window, text="CURRENT TAGS: \nYear: " + str(audio['date'])[2:-2] + "\nBPM: " + str(audio['bpm'])[2:-2] + "\nKey: " + str(audio['initialkey'])[2:-2] + "\nGenre: " + str(audio['genre'])[2:-2]).grid(row=1, column=1, pady=(10,35))
                Label(window, text="NEW TAGS: \nYear: " + str(year) + "\nBPM: " + str(BPM) + "\nKey: " + str(key) + "\nGenre: " + str(genre)).grid(row=1, column=2, pady=(10,35))
                Button(window, text="Overwrite", command=lambda: overwriteOption(audio, year, BPM, key, genre, window, webScrapingWindow)).grid(row=2, column=0)
                Button(window, text="Merge (favor scraped data)", command=lambda: mergeScrapeOption(audio, year, BPM, key, genre, window, webScrapingWindow)).grid(row=2, column=1)
                Button(window, text="Merge (favor source data)", command=lambda: mergeSourceOption(audio, year, BPM, key, genre, window, webScrapingWindow)).grid(row=2, column=2)
                Button(window, text="Skip", command=lambda: skipOption(window, webScrapingWindow)).grid(row=2, column=3)
                window.wait_window()
        else:
            audio['date'] = str(year)
            audio['bpm'] = str(BPM)
            audio['initialkey'] = key
            audio['genre'] = genre
            audio.pprint()
            audio.save()
    # return "\nTrack: " + str(artist) + " - " + str(title) + "\nYear: " + str(year) + "\nBPM: " + str(BPM) + "\nKey: " + str(key) + "\nGenre: " + str(genre) + "\nImage Links: " + str(images)
    if len(str(artist) + " - " + str(title)) > characters:
        characters = len(str(artist) + " - " + str(title))
    return "\nTrack: " + str(artist) + " - " + str(title) + "\nYear: " + str(year) + "\nBPM: " + str(BPM) + "\nKey: " + str(key) + "\nGenre: " + str(genre), webScrapingWindow, characters

def buildVariations(artist, title):
    # strip title of common prefixes like "Original Mix" or "Extended Mix"
    artistVariations = []
    titleVariations = []
    if " (Original Mix)" in title:
        titleVariations.append(title[0:title.index(" (Original Mix)")].lower())
    # strip title of spaces, paranthesis, ampersands, and other symbols that might botch the search
    spaces = re.finditer(" ", title)
    spacePositions = [match.start() for match in spaces]
    for var in spacePositions:
         title = title[0:var] + "-" + title[var + 1:]
    titleVariations.append(title.lower())
    spaces = re.finditer(" ", artist)
    spacePositions = [match.start() for match in spaces]
    for var in spacePositions:
        artist = artist[0:var] + "-" + artist[var + 1:]
    artistVariations.append(artist.lower())
    if "-(" in title:
        titleVariations.append(str(title[0:title.index("-(")]).lower())
        string = str(title[0:title.index("(")]) + str(title[title.index("(") + 1:])
        string = str(string[0:string.index(")")]) + str(string[string.index(")") + 1:])
        titleVariations.append(string.lower())
    if "." in title.lower():
        titleVariations.append(str(title[0:title.index(".")]).lower() + str(title[title.index(".") + 1:]).lower())
    if "&" in title:
        titleVariations.append(str(title[0:title.index("&")]).lower() + str(title[title.index("&") + 1:]).lower())
    if "-mix" in title.lower():
        titleVariations.append(str(title[0:title.lower().index("-mix")]) + "-Remix" + str(title[title.lower().index("-mix") + 4:]))
    return artistVariations, titleVariations

def overwriteOption(audio, year, BPM, key, genre, window, webScrapingWindow):
    audio['date'] = str(year)
    audio['bpm'] = str(BPM)
    audio['initialkey'] = key
    audio['genre'] = genre
    audio.pprint()
    audio.save()
    window.destroy()
    webScrapingWindow.lift()

def mergeScrapeOption(audio, year, BPM, key, genre, window, webScrapingWindow):
    if str(year) != '':
        audio['date'] = str(year)
    if str(BPM) != '':
        audio['bpm'] = str(BPM)
    if key != '':
        audio['initialkey'] = key
    if genre != '':
        audio['genre'] = genre
    audio.pprint()
    audio.save()
    window.destroy()
    webScrapingWindow.lift()

def mergeSourceOption(audio, year, BPM, key, genre, window, webScrapingWindow):
    if audio['date'] == ['']:
        audio['date'] = str(year)
    if audio['bpm'] == ['']:
        audio['bpm'] = str(BPM)
    if audio['initialkey'] == ['']:
        audio['initialkey'] = key
    if audio['genre'] == ['']:
        audio['genre'] = genre
    audio.pprint()
    audio.save()
    window.destroy()
    webScrapingWindow.lift()

def skipOption(window, webScrapingWindow):
    window.destroy()
    webScrapingWindow.lift()

def reverseImageSearch(link):
    print("in progress")
    # url = "https://images.google.com/searchbyimage?image_url=" + link
    # if "https://" in link:
    #     link = link.replace("https://", '')
    # elif "http://" in link:
    #     link = link.replace("http://", '')
    # print(link)
    # print(url)
    # headers = {'User-Agent': "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1b3pre) Gecko/20090109 Shiretoko/3.1b3pre"}
    # try:
    #     response = requests.get(url, data=None, headers=headers)
    #     print(response.status_code)
    #     print(response.history)
    # except requests.exceptions.ConnectionError:
    #     print("Connection refused")
    #     return
    # soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    # browser = webdriver.Firefox(executable_path=r'C:\Users\Brendan\Downloads\geckodriver-v0.27.0-win64\geckodriver.exe')
    # browser.get(url)
    #
    # soup = BeautifulSoup(browser.page_source, "html.parser")
    # link = soup.find('div', class_="O1id0e")
    # browser.quit()
    # header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    # link = soup.find('div', class_="tab-container insttab")
    # print(link)

#handle subdirectory selection
def closeScrapingWindowSelection(CONFIG_FILE):
    config_file = open(CONFIG_FILE, 'r').read()
    #if true, turn option to false
    term = "Close scraping window:"
    if config_file[config_file.index(term) + len(term):config_file.index('\n', config_file.index(term) + len(term))]=="True":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term))+1]) + "True", str(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term))+1])) + "False"))
        file.close()
    #if false, turn option to true
    elif config_file[config_file.index(term) + len(term):config_file.index('\n', config_file.index(term) + len(term))]=="False":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term)) + 1]) + "False", str(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term)) + 1])) + "True"))
        file.close()

def renameArtist(directory, var, artist, title, frame, window):
    try: os.rename(directory + '/' + var, str(directory) + str(artist) + " - " + str(title) + ".flac")
    except PermissionError:
        Label(frame.scrollable_frame, text="The file is open in another application, close it and try again").pack(anchor='w')
        window.update()
    return

def renameFile(directory, var, filename, frame, window):
    try:os.rename(directory + '/' + var, str(directory) + '/' + str(filename))
    except PermissionError:
        Label(frame.scrollable_frame, text="The file is open in another application, close it and try again").pack(anchor='w')
        window.update()
    return

def checkFileValidity(directory, var, frame, window):
    try:
        audio = FLAC(str(directory) + '/' + str(var))
        return audio
    except:
        Label(frame.scrollable_frame, text="Invalid or Corrupt File").pack(anchor='w')
        window.update()
        return "Invalid or corrupt file\n"

def closeFinalReport(finalReportWindow, webScrapingWindow):
    finalReportWindow.destroy()
    webScrapingWindow.lift()


