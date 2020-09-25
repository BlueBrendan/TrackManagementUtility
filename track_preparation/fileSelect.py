from tkinter import filedialog
from mutagen.flac import FLAC, Picture
from mutagen.aiff import AIFF
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE
from mutagen.wavpack import WavPack
import base64
import tkinter as tk
from tkinter.tix import *
import os
import getpass
from PIL import Image, ImageTk
from io import BytesIO

#import classes
from classes.AudioClass import *
from classes.scrollbarClass import ScrollableFrame

#import methods
from track_preparation.initiateTrack.initiateFLAC import initiateFLAC
from track_preparation.initiateTrack.initiateAIFF import initiateAIFF
from track_preparation.initiateTrack.initiateMP3 import initiateMP3
from track_preparation.initiateTrack.initiateOGG import initiateOGG
from track_preparation.initiateTrack.initiateWAVE import initiateWAVE
from track_preparation.initiateTrack.initiateM4A import initiateM4A
from track_scraping.scrapeWeb import scrapeWeb

def fileSelect(window, options, imageCounter, CONFIG_FILE):
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
        Label(frame.scrollable_frame, text="Beginning procedure...", wraplength=300, justify='left').pack(anchor='w')
        characters = 0
        thumbnails = []
        for directory in directories:
            filename = os.path.basename(directory)
            directory = os.path.dirname(directory)
            if checkValidity(filename):
                audio = False
                track = ''
                #handle FLAC file
                if filename.endswith('.flac') and type(checkFileValidity(filename, directory, "FLAC", frame, window))!=str:
                    #handle naming preferences, tag settings, and replay gain
                    audio, filename, informalTagDict = initiateFLAC(filename, directory, frame, webScrapingWindow, options)
                    if type(audio) != bool:
                        images = audio.pictures
                        # append thumbnail image to list if artwork exists
                        if len(images) > 0:
                            stream = BytesIO(images[0].data)
                            image = Image.open(stream).convert("RGBA")
                            thumbnails.append(image)
                            stream.close()
                        else: thumbnails.append("NA")
                        track = FLAC_Track(audio, options, informalTagDict)
                #handle AIFF file
                elif filename.endswith('.aiff') and type(checkFileValidity(filename, directory, "AIFF", frame, window))!=str:
                    audio, filename, informalTagDict = initiateAIFF(filename, directory, frame, webScrapingWindow, options)
                    if type(audio) != bool:
                        image = audio["APIC:"]
                        if image.data != b'':
                            stream = BytesIO(image.data)
                            image = Image.open(stream).convert("RGBA")
                            thumbnails.append(image)
                            stream.close()
                        else: thumbnails.append("NA")
                        track = ID3_Track(audio, options, informalTagDict)
                #handle MP3 file
                elif filename.endswith('mp3') and type(checkFileValidity(filename, directory, "MP3", frame, window))!=str:
                    audio, filename, informalTagDict = initiateMP3(filename, directory, frame, webScrapingWindow, options)
                    if type(audio) != bool:
                        image = audio["APIC:"]
                        if image.data != b'':
                            stream = BytesIO(image.data)
                            image = Image.open(stream).convert("RGBA")
                            thumbnails.append(image)
                            stream.close()
                        else: thumbnails.append("NA")
                        track = ID3_Track(audio, options, informalTagDict)
                #handle OGG file
                elif filename.endswith('.ogg') and type(checkFileValidity(filename, directory, "OGG", frame, window))!=str:
                    audio, filename, informalTagDict = initiateOGG(filename, directory, frame, webScrapingWindow, options)
                    if type(audio) != bool:
                        images = audio["metadata_block_picture"]
                        if images[0] != '':
                            data = base64.b64decode(images[0])
                            image = Picture(data)
                            stream = BytesIO(image.data)
                            image = Image.open(stream).convert("RGBA")
                            thumbnails.append(image)
                            stream.close()
                        # append thumbnail image to list if artwork exists
                        else: thumbnails.append("NA")
                        track = Vorbis_Track(audio, options, informalTagDict)
                #handle WAV file
                elif filename.endswith('.wav') and type(checkFileValidity(filename, directory, "WAV", frame, window))!=str:
                    audio, filename, informalTagDict = initiateWAVE(filename, directory, frame, webScrapingWindow, options)
                    if type(audio) != bool:
                        image = audio["APIC:"]
                        if image.data != b'':
                            stream = BytesIO(image.data)
                            image = Image.open(stream).convert("RGBA")
                            thumbnails.append(image)
                            stream.close()
                        else: thumbnails.append("NA")
                        track = ID3_Track(audio, options, informalTagDict)
                #handle AAC and ALAC files
                elif filename.endswith('.m4a') and type(checkFileValidity(filename, directory, "M4A", frame, window))!=str:
                    audio, filename, informalTagDict = initiateM4A(filename, directory, frame, webScrapingWindow, options)
                    if type(audio) != bool:
                        image = audio["covr"]
                        if len(image) != 0:
                            stream = BytesIO(image[0])
                            image = Image.open(stream).convert("RGBA")
                            thumbnails.append(image)
                            stream.close()
                        else: thumbnails.append("NA")
                        track = ALAC_Track(audio, options, informalTagDict)
                # search web for tags
                if type(audio) != bool:
                    results, webScrapingWindow, characters, imageCounter, imageSelection = scrapeWeb(track, audio, filename, frame, webScrapingWindow, characters, options, imageCounter)
                    finalResults.append(results)
                    imageSelections.append(imageSelection)

        finalReportWindow = Toplevel()
        webScrapingWindow.lift()
        finalReportWindow.title("Final Report")
        canvas = Canvas(finalReportWindow)
        finalReport = Frame(canvas)
        scrollbar = Scrollbar(finalReportWindow, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        ws = finalReportWindow.winfo_screenwidth()  # width of the screen
        hs = finalReportWindow.winfo_screenheight()  # height of the screen
        y = (hs / 2) - (572 / 2)
        x = (ws / 2) - (450 / 2)
        finalReportWindow.geometry('%dx%d+%d+%d' % (450, 520, x, y))
        canvas.create_window((450 / 2), 0, window=finalReport, anchor="n")
        if len(directories) > 1:
            y = (hs / 2) - (770 / 2)
            finalReportWindow.geometry('%dx%d+%d+%d' % (450, 700, x, y))
        if characters > 40:
            x = (ws / 2) - ((450 + (characters * 1.5)) / 2)
            finalReportWindow.geometry('%dx%d+%d+%d' % (450 + (characters * 1.5), 520, x, y))
            canvas.create_window(((450 + (characters * 1.5)) / 2), 0, window=finalReport, anchor="n")
            if len(directories) > 1:
                y = (hs / 2) - (770 / 2)
                finalReportWindow.geometry('%dx%d+%d+%d' % (450 + (characters * 1.5), 700, x, y))
        Label(finalReport, text="Final Report", font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(15, 10))
        for i in range(len(finalResults)):
            Label(finalReport, text=finalResults[i] + '\n').pack(side="top")
            # load non-thumbnailimage
            if options["Reverse Image Search (B)"].get() == True and imageCounter >= 1 and imageSelections[i] != 'THUMB':
                fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageSelections[i]) + ".jpg")
                width, height = fileImageImport.size
                fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(fileImageImport)
                fileImage = Label(finalReport, image=photo)
                fileImage.image = photo
                fileImage.pack(side="top", padx=(10, 10))
                #resolution
                Label(finalReport, text=str(width) + "x" + str(height)).pack(side="top", pady=(5, 10))
            #load thumbnail image
            else:
                if thumbnails[i] == 'NA': Label(finalReport, text="No Artwork Found").pack(side="top", pady=(5,20))
                else:
                    fileImageImport = thumbnails[i]
                    width, height = fileImageImport.size
                    fileImageImport = thumbnails[i].resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(fileImageImport)
                    fileImage = Label(finalReport, image=photo)
                    fileImage.image = photo
                    fileImage.pack(side="top", padx=(10, 10))
                    # resolution
                    Label(finalReport, text=str(width) + "x" + str(height)).pack(side="top", pady=(5, 20))
        # load button and checkbox
        Button(finalReport, text='OK', command=lambda: completeSearch(finalReportWindow, webScrapingWindow, options)).pack(side=TOP, pady=(15, 15))
        Checkbutton(finalReport, text="Close scraping window", var=options["Close Scraping Window (B)"], command=lambda: closeScrapingWindowSelection(CONFIG_FILE)).pack(side=TOP, pady=(0,10))
        finalReportWindow.protocol('WM_DELETE_WINDOW', lambda: closePopup(finalReportWindow, webScrapingWindow))
        finalReportWindow.lift()
        canvas.update_idletasks()
        canvas.pack(side="left", expand=YES, fill=BOTH)
        canvas.configure(scrollregion=(0,0,0,(520 + (361 * (len(directories)-1)))))
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

#check if mutagen object can be made from file
def checkFileValidity(filename, directory, format, frame, window):
    audio = ""
    if format=="FLAC":
        try:audio = FLAC(str(directory) + "/" + str(filename))
        except:
            tk.Label(frame.scrollable_frame, text="Invalid or Corrupt File").pack(anchor='w')
            window.update()
            return "Invalid or corrupt file\n"
    elif format=="AIFF":
        try: audio = AIFF(str(directory) + "/" + str(filename))
        except:
            tk.Label(frame.scrollable_frame, text="Invalid or Corrupt File").pack(anchor='w')
            window.update()
            return "Invalid or corrupt file\n"
    elif format=="MP3":
        try: audio = MP3(str(directory) + "/" + str(filename))
        except:
            tk.Label(frame.scrollable_frame, text="Invalid or Corrupt File").pack(anchor='w')
            window.update()
            return "Invalid or corrupt file\n"
    elif format=="OGG":
        try: audio = OggVorbis(str(directory) + "/" + str(filename))
        except:
            tk.Label(frame.scrollable_frame, text="Invalid or Corrupt File").pack(anchor='w')
            window.update()
            return "Invalid or corrupt file\n"
    elif format=="WAV":
        try: audio = WAVE(str(directory) + "/" + str(filename))
        except:
            tk.Label(frame.scrollable_frame, text="Invalid or Corrupt File").pack(anchor='w')
            window.update()
            return "Invalid or corrupt file\n"
    elif format=="M4A":
        #M4A is deprecated in mutagen, MP4 is suggested instead
        try: audio = MP4(str(directory) + "/" + str(filename))
        except:
            tk.Label(frame.scrollable_frame, text="Invalid or Corrupt File").pack(anchor='w')
            window.update()
            return "Invalid or corrupt file\n"
    return audio

#check if filetype is supported
def checkValidity(filename):
    if filename.endswith('.flac') or filename.endswith(".aiff") or filename.endswith(".mp3") or filename.endswith(".ogg") or filename.endswith(".wav") or filename.endswith(".m4a"): return True
    return False

def closePopup(popup, webScrapingWindow):
    popup.destroy()
    webScrapingWindow.lift()