from tkinter import filedialog
from mutagen.flac import FLAC, Picture
from mutagen.aiff import AIFF
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE
import base64
from tkinter import messagebox
from tkinter.tix import *
import os
from PIL import Image
from io import BytesIO

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

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

def fileSelect(options, imageCounter, CONFIG_FILE):
    directories = filedialog.askopenfilenames(title="Select File")
    if directories != '':
        imageSelections = []
        finalResults = []
        characters = 0
        webScrapingWindow = ''
        thumbnails = []
        for directory in directories:
            filename = os.path.basename(directory)
            directory = os.path.dirname(directory)
            if checkValidity(filename):
                audio = False
                track = ''
                informalTagDict = ''
                #handle FLAC file
                if filename.endswith('.flac') and type(checkFileValidity(filename, directory, "FLAC"))!=str:
                    #handle naming preferences, tag settings, and replay gain
                    audio, filename, informalTagDict = initiateFLAC(filename, directory, options)
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
                elif filename.endswith('.aiff') and type(checkFileValidity(filename, directory, "AIFF"))!=str:
                    audio, filename, informalTagDict = initiateAIFF(filename, directory, options)
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
                elif filename.endswith('mp3') and type(checkFileValidity(filename, directory, "MP3"))!=str:
                    audio, filename, informalTagDict = initiateMP3(filename, directory, options)
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
                elif filename.endswith('.ogg') and type(checkFileValidity(filename, directory, "OGG"))!=str:
                    audio, filename, informalTagDict = initiateOGG(filename, directory, options)
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
                elif filename.endswith('.wav') and type(checkFileValidity(filename, directory, "WAV"))!=str:
                    audio, filename, informalTagDict = initiateWAVE(filename, directory, options)
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
                elif filename.endswith('.m4a') and type(checkFileValidity(filename, directory, "M4A"))!=str:
                    audio, filename, informalTagDict = initiateM4A(filename, directory, options)
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
                    #create webscraping window on top left corner
                    webScrapingWindow = Toplevel()
                    webScrapingWindow.title("Web Scraping Display")
                    webScrapingWindow.configure(bg=bg)
                    webScrapingWindow.geometry("900x300+0+0")
                    results, webScrapingWindow, characters, imageCounter, imageSelection = scrapeWeb(track, audio, filename, webScrapingWindow, characters, options, imageCounter, informalTagDict)
                    finalResults.append(results)
                    imageSelections.append(imageSelection)
        if type(webScrapingWindow)!=str: handleFinalReport(finalResults, characters, imageCounter, imageSelections, thumbnails, webScrapingWindow, options, CONFIG_FILE)

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