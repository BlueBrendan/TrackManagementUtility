from mutagen.flac import FLAC
import tkinter as tk
import os

#import methods
from track_preparation.handleTypo import handleTypo

def retrieveInfo(var, directory, frame, webScrapingWindow, options):
    audio = checkFileValidity(var, directory, frame, webScrapingWindow)
    if type(audio) == str:
        return False
    # check if artist and title are in filename
    if options["Check Artist for Typos (B)"].get() == True:
        if ' - ' in var:
            artist = var.split(' - ')[0]
            title = var.split(' - ')[1][:-5]
            # scan artist for numbering prefix
            if '.' in artist:
                artistPrefix = artist[:artist.index('.')+1]
                artistPostfix = artist[artist.index('.')+1:].strip()
                if '.' in artistPrefix[0:5]:
                    if any(char.isdigit() for char in artistPrefix[0:artistPrefix.index('.')]):
                        audio, var = handleTypo(artist, title, var, artistPostfix, webScrapingWindow, audio, directory, frame, webScrapingWindow)
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
                        audio, var = handleTypo(artist, title, var, titlePrefix, webScrapingWindow, audio, directory, frame, webScrapingWindow)
    if options["Audio naming format (S)"].get() == "Audio - Title":
        #rename track so that the artist is appended at the front of the title
        if ' - ' not in var:
            artist = str(audio['artist'])[2:-2]
            os.rename(directory + '/' + var, str(directory) + '/' + str(artist) + ' - ' + var)
            var = str(artist) + ' - ' + var
            audio = FLAC(directory + '/' + var)
    elif options["Audio naming format (S)"].get() == "Title":
        # rename track so that the artist is not at the front of the title
        if ' - ' in var:
            os.rename(directory + '/' + var, str(directory) + '/' + var[var.index(' - ') + 3:])
            audio = FLAC(directory + '/' + var[var.index(' - ') + 3:])
            audio["artist"] = var[:var.index(' - ')]
            audio.save()
            var = var[var.index(' - ') + 3:]
    return audio, var

def checkFileValidity(var, directory, frame, window):
    try:
        audio = FLAC(str(directory) + "/" + str(var))
        return audio
    except:
        tk.Label(frame.scrollable_frame, text="Invalid or Corrupt File").pack(anchor='w')
        window.update()
        return "Invalid or corrupt file\n"