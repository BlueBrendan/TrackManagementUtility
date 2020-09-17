from mutagen.flac import FLAC
import tkinter as tk
import os

#import methods
from track_preparation.handleTypo import handleTypo
from track_preparation.handleReplayGain import handleReplayGain

def updateTrack(filename, directory, frame, webScrapingWindow, options):
    audio = FLAC(str(directory) + "/" + str(filename))

    # handle file tags
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

    # handle naming format and typo check
    if options["Audio naming format (S)"].get() == "Artist - Title":
        # rename track so that the artist is appended at the front of the title
        if ' - ' in filename:
            artist, title, extension = keepFormat(filename, options, webScrapingWindow)
            os.rename(directory + '/' + filename, str(directory) + '/' + str(artist) + ' - ' + str(title) + extension)
            filename = str(artist) + ' - ' + str(title) + extension
            audio = FLAC(directory + '/' + str(artist) + ' - ' + str(title) + extension)
            if str(audio["artist"][0]) != artist or str(audio["title"][0]) != title:
                audio["artist"] = artist
                audio['title'] = title
                audio.save()
        else:
            if changeFormat(audio, filename, options, frame, webScrapingWindow):
                artist, title, extension = changeFormat(audio, filename, options, frame, webScrapingWindow)
                os.rename(directory + '/' + filename, str(directory) + '/' + str(artist) + ' - ' + str(title) + extension)
                filename = str(artist) + ' - ' + str(title) + extension
                audio = FLAC(directory + '/' + str(artist) + ' - ' + str(title) + extension)
                if str(audio["artist"][0]) != artist or str(audio["title"][0])!=title:
                    audio["artist"] = artist
                    audio["title"] = title
                    audio.save()
            else:
                return False, filename
    elif options["Audio naming format (S)"].get() == "Title":
        # rename track so that the artist is removed from the title
        if ' - ' in filename:
            if changeFormat(audio, filename, options, frame, webScrapingWindow):
                artist, title, extension = changeFormat(audio, filename, options, frame, webScrapingWindow)
                os.rename(directory + '/' + filename, str(directory) + '/' + str(title) + extension)
                filename = str(title) + extension
                audio = FLAC(directory + '/' + str(title) + extension)
                if str(audio["artist"][0]) != artist or str(audio["title"][0]) != title:
                    audio["artist"] = artist
                    audio["title"] = title
                    audio.save()
            else:
                return False, filename
        else:
            artist, title, extension = keepFormat(filename, options, webScrapingWindow)
            os.rename(directory + '/' + filename, str(directory) + '/' + str(title) + extension)
            filename = str(title) + extension
            audio = FLAC(directory + '/' + str(title) + extension)
            if str(audio["artist"][0]) != artist or str(audio["title"][0]) != title:
                audio["artist"] = artist
                audio['title'] = title
                audio.save()

    # handle replayGain
    if options["Calculate ReplayGain (B)"].get() == True: audio = handleReplayGain(directory, filename, audio)

    return audio, filename

def changeFormat(audio, filename, options, frame, webScrapingWindow):
    artist = str(audio['artist'][0])
    if artist == '':
        tk.Label(frame.scrollable_frame, text="No artist information found, aborting procedure", justify='left').pack(anchor='w')
        return False
    title = filename[:-5]
    extension = filename[filename.rfind('.'):]
    if options["Check Artist for Typos (B)"].get() == True:
        # scan artist for numbering prefix
        if '.' in artist:
            artistPrefix = artist[:artist.index('.') + 1]
            artistPostfix = artist[artist.index('.') + 1:].strip()
            if '.' in artistPrefix[0:5]:
                if any(char.isdigit() for char in artistPrefix[0:artistPrefix.index('.')]):
                    artist = handleTypo(artist, artistPostfix, title, webScrapingWindow)
    return artist, title, extension

def keepFormat(filename, options, webScrapingWindow):
    artist = str(filename.split(' - ')[0])
    title = str(filename.split(' - ')[1][:-5])
    extension = filename[filename.rfind('.'):]
    if options["Check Artist for Typos (B)"].get() == True:
        # scan artist for numbering prefix
        if '.' in artist:
            artistPrefix = artist[:artist.index('.') + 1]
            artistPostfix = artist[artist.index('.') + 1:].strip()
            if '.' in artistPrefix[0:5]:
                if any(char.isdigit() for char in artistPrefix[0:artistPrefix.index('.')]):
                    artist = handleTypo(artist, artistPostfix, title, webScrapingWindow)
    return artist, title, extension