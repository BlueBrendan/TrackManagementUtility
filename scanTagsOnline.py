import os
import requests
from bs4 import BeautifulSoup
from mutagen.flac import FLAC
from mutagen.id3 import ID3, TIT2, TKEY
from tkinter import filedialog
from tkinter.tix import *
import getpass
from selenium import webdriver
from PIL import Image, ImageTk

#import methods from other files
from junodownloadSearch import junodownloadSearch
from beatportSearch import beatportSearch
from discogsSearch import discogsSearch
from buildTrackReport import buildTrackReport
from buildVariations import buildVariations
from handleTypo import handleTypo

#global variables
imageCounter = 0

#class for scrollbar in web scraping window
class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="w")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        canvas.config(width=680, height=640)
        scrollbar.pack(side="right", fill="y")

class SmallScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.small_scrollable_frame = Frame(canvas)

        self.small_scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.small_scrollable_frame, anchor="center")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        canvas.config(width=420, height=230)
        scrollbar.pack(side="right", fill="y")

#class for audiotrack file (stores tags externally)
class AudioTrack:
    def __init__(self, audio):
        interestParameters = ['artist', 'title', 'date', 'BPM', 'initialkey', 'genre', 'replaygain_track_gain']
        self.artist = audio["artist"][0]
        self.title = audio["title"][0]
        self.year = ''
        self.BPM = ''
        self.key = ''
        self.genre = ''
        self.replaygain_track_gain = ''

    def searchTags(track, audio, frame, webScrapingWindow, characters, options, imageCounter):
        interestParameters = ['artist', 'title', 'date', 'bpm', 'initialkey', 'genre', 'replaygain_track_gain']
        fileParameters = []
        for x in audio:
            fileParameters.append(x)
        for x in fileParameters:
            # delete extraneous tags
            if x not in interestParameters:
                print("Deleting " + str(x))
                audio[x] = ""
                audio.pop(x)
                audio.save()
        for x in interestParameters:
            # add tags of interest if missing
            if x not in fileParameters:
                audio[x] = ""
                audio.save()
        search = str(track.artist) + " - " + str(track.title)
        # clean search query of ampersands (query ends upon reaching ampersand symbol)
        if '&' in search:
            search = search.replace('&', 'and')
        yearList = []
        BPMList = []
        keyList = []
        genreList = []
        # build list of artist and track title variations to prepare for scraping
        artistVariations, titleVariations = buildVariations(track.artist, track.title)
        # web scraping
        headers = {'User-Agent': "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1b3pre) Gecko/20090109 Shiretoko/3.1b3pre"}
        headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",}
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
        # }
        # junodownload
        if options['Scrape Junodownload (B)'].get() == True:yearList, BPMList, genreList, imageCounter = junodownloadSearch(track.artist, track.title, yearList, BPMList, genreList, artistVariations, titleVariations, headers, search, frame, webScrapingWindow, audio, options, imageCounter)
        # # #beatport
        if options['Scrape Beatport (B)'].get() == True:yearList, BPMList, keyList, genreList= beatportSearch(track.artist, track.title, yearList, BPMList, keyList, genreList, artistVariations, titleVariations, headers, search, frame, webScrapingWindow)
        # #discogs
        if options['Scrape Discogs (B)'].get() == True:yearList, genreList, imageCounter = discogsSearch(track.artist, track.title, yearList, genreList, artistVariations, titleVariations, headers, search, frame, webScrapingWindow, imageCounter)
        # spotify
        # apple music
        finalResults, webScrapingWindow, characters = buildTrackReport(track, yearList, BPMList, keyList, genreList, audio, webScrapingWindow, characters, options, imageCounter)
        return finalResults, webScrapingWindow, characters, imageCounter

    def scanFLAC(self, directory, frame, webScrapingWindow, characters, options, imageCounter):
        # check if artist and title are in filename
        audio = FLAC(directory + '/' + self.artist + ' - ' + self.title + '.flac')
        audio["artist"] = self.artist
        audio["title"] = self.title
        audio.pprint()
        audio.save()
        finalResults, webScrapingWindow, characters, imageCounter = AudioTrack.searchTags(self, audio, frame, webScrapingWindow, characters, options, imageCounter)
        return finalResults, webScrapingWindow, characters, imageCounter

#driver code
def selectFileOrDirectory(CONFIG_FILE, options):
    #TODO
    #Implement typo/misspell detection system
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
    Button(window, text="Files", command=lambda: scanTagsOnline(options['Subdirectories (B)'], "file", window, options['Close Scraping Window (B)'], CONFIG_FILE, options, imageCounter)).grid(row=2, column=1, pady=(5, 3))
    Button(window, text="Directories", command=lambda: scanTagsOnline(options['Subdirectories (B)'], "directory", window, options['Close Scraping Window (B)'], CONFIG_FILE, options, imageCounter)).grid(row=2,column=2, pady=(5, 3))

def scanTagsOnline(subdirectories, type, window, closeScrapingWindow, CONFIG_FILE, options, imageCounter):
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
                directory = os.path.dirname(directory)
                #handle FLAC files
                if var.endswith('.flac'):
                    row+=1
                    audio = retrieveInfo(var, directory, frame, webScrapingWindow)
                    if audio:
                        track = AudioTrack(audio)
                        result, webScrapingWindow, characters, imageCounter = AudioTrack.scanFLAC(track, directory, frame, webScrapingWindow, characters, options, imageCounter)
                        results += result + '\n'
            if audio:
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
                    fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(0) + ".jpg")
                    fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(fileImageImport)
                    fileImage = Label(finalReportWindow, image=photo)
                    fileImage.image = photo
                    fileImage.pack(side="top", padx=(10, 10))
                    #load button and checkbox
                    Button(finalReportWindow, text='OK', command=lambda: completeSearch(finalReportWindow, webScrapingWindow, closeScrapingWindow, options)).pack(side="top", pady=(15, 10))
                    Checkbutton(finalReportWindow, text="Close scraping window", var=closeScrapingWindow, command=lambda: closeScrapingWindowSelection(CONFIG_FILE)).pack(side="top")
                    finalReportWindow.protocol('WM_DELETE_WINDOW', lambda: closePopup(finalReportWindow, webScrapingWindow))
                else:
                    Label(finalReportWindow, text="Final Report", font=("TkDefaultFont", 9, 'bold')).grid(row=0, column=0, pady=(15,0))
                    Label(finalReportWindow, text=results).grid(row=1, column=0)
                    Button(finalReportWindow, text='OK', command=lambda: completeSearch(finalReportWindow, webScrapingWindow, closeScrapingWindow, options)).grid(row=2, column=0, pady=(0, 5))
                    Checkbutton(finalReportWindow, text="Close scraping window", var=closeScrapingWindow, command=lambda: closeScrapingWindowSelection(CONFIG_FILE)).grid(row=3, column=0)
                    finalReportWindow.protocol('WM_DELETE_WINDOW', lambda: closePopup(finalReportWindow, webScrapingWindow))
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
            y = (hs / 2) - (770 / 2)
            webScrapingWindow.geometry('%dx%d+%d+%d' % (700, 650, x, y))
            Label(frame.scrollable_frame, text="Beginning web scraping procedure...", wraplength=300, justify='left').pack(anchor='w')
            finalReport, webScrapingWindow, characters = directorySearch(directory, subdirectories, results, frame, webScrapingWindow, characters, options, imageCounter)
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
            #empty directory provided
            if len(finalReport)==0:
                Label(finalReportWindow, text="No tracks were found in the provided directory").pack()
            Button(frame.small_scrollable_frame, text='OK', command=lambda: completeSearch(finalReportWindow, webScrapingWindow, closeScrapingWindow, options)).pack(anchor="center")
            finalReportWindow.protocol('WM_DELETE_WINDOW', lambda: closePopup(finalReportWindow, webScrapingWindow))

def completeSearch(finalReportWindow, webScrapingWindow, closeScrapingWindow, options):
    finalReportWindow.destroy()
    webScrapingWindow.lift()
    if closeScrapingWindow.get() != False:
        webScrapingWindow.destroy()
    # delete all images in temp if both revese image search and delete stored image options are both true
    if options["Reverse Image Search (B)"].get() == True and options["Delete Stored Images (B)"].get() == True:
        images = os.listdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/")
        for image in images:
            os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(image))

def directorySearch(directory, subdirectories, results, frame, webScrapingWindow, characters, options, imageCounter):
    files = os.listdir(directory)
    for var in files:
        if os.path.isdir(directory + '/' + var) and subdirectories.get() == True:
            directorySearch(directory + '/' + var, subdirectories, results, frame, webScrapingWindow, characters, options, imageCounter)
        else:
            #handle FLAC files
            if var.endswith(".flac"):
                audio = retrieveInfo(var, directory, frame, webScrapingWindow)
                if audio:
                    track = AudioTrack(audio)
                    result, webScrapingWindow, characters, imageCounter = AudioTrack.scanFLAC(track, var, directory, frame, webScrapingWindow, characters, options, imageCounter)
                    results.append(result)
    return results, webScrapingWindow, characters

def retrieveInfo(var, directory, frame, webScrapingWindow):
    audio = checkFileValidity(var, directory, frame, webScrapingWindow)
    if type(audio) == str:
        return False
    # check if artist and title are in filename
    if ' - ' in var:
        artist = var.split(' - ')[0]
        title = var.split(' - ')[1][:-5]
        # scan artist for numbering prefix
        if '.' in artist:
            artistPrefix = artist[:artist.index('.')+1]
            artistPostfix = artist[artist.index('.')+1:].strip()
            if '.' in artistPrefix[0:5]:
                if any(char.isdigit() for char in artistPrefix[0:artistPrefix.index('.')]):
                    audio = handleTypo(artist, title, artistPostfix, webScrapingWindow, audio, directory, frame, webScrapingWindow)
    # check file tags for artist
    else:
        if audio['artist'] == '':
            print("No artist information found in file")
            return False
        artist = str(audio['artist'])[2:-2]
        title = var[:-5]
        if ' ' in title or '.' in title:
            if ' ' in artist:
                titlePrefix = title.split(' ', 1)[0]
                titlePostfix = title.split(' ', 1)[1]
            else:
                titlePrefix = title.split('.')[0]
                titlePostfix = title.split('.')[1]
            if '.' in titlePrefix[0:5]:
                if any(char.isdigit() for char in titlePrefix[0:titlePrefix.index('.')]):
                    audio = handleTypo(artist, title, titlePrefix, webScrapingWindow, audio, directory, frame, webScrapingWindow)
    # if "featuring" in artist:
    #     artist = artist.replace("featuring", "feat.")
    #     audio = renameArtist(directory, var, artist, title, frame, webScrapingWindow)
    # if '’' in filename:
    #     filename = filename.replace("’", "'")
    #     renameFile(directory, var, filename, frame, webScrapingWindow)
    # audio["artist"] = artist
    # audio["title"] = title
    return audio

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

def checkFileValidity(var, directory, frame, window):
    try:
        audio = FLAC(str(directory) + "/" + str(var))
        return audio
    except:
        Label(frame.scrollable_frame, text="Invalid or Corrupt File").pack(anchor='w')
        window.update()
        return "Invalid or corrupt file\n"

def closePopup(popup, webScrapingWindow):
    popup.destroy()
    webScrapingWindow.lift()


