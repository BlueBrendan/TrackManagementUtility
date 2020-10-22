from tkinter import filedialog
from mutagen.flac import FLAC, Picture
from mutagen.aiff import AIFF
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE
from tkinter import messagebox
from tkinter.tix import *
import tkinter as tk
import os

#import classes
from AudioClass import *

#import methods
from track_preparation.initiateTrack.initiateFLAC import initiateFLAC
from track_preparation.initiateTrack.initiateAIFF import initiateAIFF
from track_preparation.initiateTrack.initiateMP3 import initiateMP3
from track_preparation.initiateTrack.initiateOGG import initiateOGG
from track_preparation.initiateTrack.initiateWAVE import initiateWAVE
from track_preparation.initiateTrack.initiateM4A import initiateM4A
from track_scraping.scrapeWeb import scrapeWeb
from track_scraping.handleFinalReport import handleFinalReport
from web_scrapers.webScrapingWindowControl import enableControls
from web_scrapers.webScrapingWindowControl import rerenderControls
from track_preparation.initiateTrack.commonOperations import resource_path

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

def fileSelect(options, imageCounter, CONFIG_FILE, window):
    directories = filedialog.askopenfilenames(title="Select File")
    webScrapingWindow = False
    if directories != '':
        # delete previous web scraping window from previous session
        if type(window)!=bool: window.destroy()
        imageSelections = []
        finalTitles = []
        finalResults = []
        characters = 0
        images = []
        thumbnails = []
        # create webscraping window on top left corner
        webScrapingWindow = Toplevel()
        webScrapingWindow.title("Web Scraping Display")
        webScrapingWindow.configure(bg=bg)
        webScrapingWindow.geometry("1000x300+0+0")
        webScrapingWindow.iconbitmap(resource_path('favicon.ico'))
        # component for search label and page indicator
        labelFrame = tk.Frame(webScrapingWindow, bg=bg)
        labelFrame.pack(fill=X, pady=(10, 10))
        searchFrame = tk.Frame(labelFrame, bg=bg)
        searchFrame.pack(side="left")
        pageFrame = tk.Frame(labelFrame, bg=bg)
        pageFrame.pack(side="right", pady=(20, 0))
        componentFrame = tk.Frame(webScrapingWindow, bg=bg)
        componentFrame.pack(fill=X, pady=(10, 0))
        rerenderControls(pageFrame, 0)

        # dictionary to store web scraping window values
        webScrapingLeftPane = {}
        webScrapingRightPane = {}
        webScrapingLinks = {}
        webScrapingPage = 0
        for directory in directories:
            filename = os.path.basename(directory)
            directory = os.path.dirname(directory)
            if not checkValidity(filename):
                extension = filename[filename.rfind("."):]
                messagebox.showinfo("Error", extension + " is not a supported format")
                if str(directory) + "/" + str(filename) == str(directories[len(directories)-1]): webScrapingWindow.destroy()
            audio = False
            track = ''
            informalTagDict = ''
            #handle FLAC file
            if filename.endswith('.flac') and type(checkFileValidity(filename, directory, "FLAC"))!=str:
                #handle naming preferences, tag settings, and replay gain
                audio, filename, informalTagDict, thumbnails, options = initiateFLAC(filename, directory, thumbnails, options)
                if type(audio) != bool: track = FLAC_Track(audio, options, informalTagDict)
            #handle AIFF file
            elif filename.endswith('.aiff') and type(checkFileValidity(filename, directory, "AIFF"))!=str:
                audio, filename, informalTagDict, thumbnails, options = initiateAIFF(filename, directory, thumbnails, options)
                if type(audio) != bool: track = ID3_Track(audio, options, informalTagDict)
            #handle MP3 file
            elif filename.endswith('mp3') and type(checkFileValidity(filename, directory, "MP3"))!=str:
                audio, filename, informalTagDict, thumbnails, options = initiateMP3(filename, directory, thumbnails, options)
                if type(audio) != bool: track = ID3_Track(audio, options, informalTagDict)
            #handle OGG file
            elif filename.endswith('.ogg') and type(checkFileValidity(filename, directory, "OGG"))!=str:
                audio, filename, informalTagDict, thumbnails, options = initiateOGG(filename, directory, thumbnails, options)
                if type(audio) != bool: track = Vorbis_Track(audio, options, informalTagDict)
            #handle WAV file
            elif filename.endswith('.wav') and type(checkFileValidity(filename, directory, "WAV"))!=str:
                audio, filename, informalTagDict, thumbnails, options = initiateWAVE(filename, directory, thumbnails, options)
                if type(audio) != bool: track = ID3_Track(audio, options, informalTagDict)
            #handle AAC and ALAC files
            elif filename.endswith('.m4a') and type(checkFileValidity(filename, directory, "M4A"))!=str:
                audio, filename, informalTagDict, thumbnails, options = initiateM4A(filename, directory, thumbnails, options)
                if type(audio) != bool: track = M4A_Track(audio, options, informalTagDict)
            # search web for tags
            if type(audio) != bool:
                reportTitle, reportResults, webScrapingWindow, characters, imageCounter, imageSelection, images, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame = scrapeWeb(track, audio, filename, webScrapingWindow, characters, options, imageCounter, images, informalTagDict, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, labelFrame, searchFrame, pageFrame, componentFrame)
                finalTitles.append(reportTitle)
                finalResults.append(reportResults)
                imageSelections.append(imageSelection)
        # enable controls in web scraping window
        enableControls(searchFrame, pageFrame, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, componentFrame)
        handleFinalReport(finalTitles, finalResults, characters, imageCounter, imageSelections, webScrapingWindow, thumbnails, options, CONFIG_FILE)
    return webScrapingWindow
#check if mutagen object can be made from file
def checkFileValidity(filename, directory, format):
    audio = ""
    if format=="FLAC":
        try:audio = FLAC(str(directory) + "/" + str(filename))
        except:
            messagebox.showinfo("Error", "Invalid or Corrupt File")
            return "Invalid or corrupt file\n"
    elif format=="AIFF":
        try: audio = AIFF(str(directory) + "/" + str(filename))
        except:
            messagebox.showinfo("Error", "Invalid or Corrupt File")
            return "Invalid or corrupt file\n"
    elif format=="MP3":
        try: audio = MP3(str(directory) + "/" + str(filename))
        except:
            messagebox.showinfo("Error", "Invalid or Corrupt File")
            return "Invalid or corrupt file\n"
    elif format=="OGG":
        try: audio = OggVorbis(str(directory) + "/" + str(filename))
        except:
            messagebox.showinfo("Error", "Invalid or Corrupt File")
            return "Invalid or corrupt file\n"
    elif format=="WAV":
        try: audio = WAVE(str(directory) + "/" + str(filename))
        except:
            messagebox.showinfo("Error", "Invalid or Corrupt File")
            return "Invalid or corrupt file\n"
    elif format=="M4A":
        #M4A is deprecated in mutagen, MP4 is suggested instead
        try: audio = MP4(str(directory) + "/" + str(filename))
        except:
            messagebox.showinfo("Error", "Invalid or Corrupt File")
            return "Invalid or corrupt file\n"
    return audio

#check if filetype is supported
def checkValidity(filename):
    if filename.endswith('.flac') or filename.endswith(".aiff") or filename.endswith(".mp3") or filename.endswith(".ogg") or filename.endswith(".wav") or filename.endswith(".m4a"): return True
    return False