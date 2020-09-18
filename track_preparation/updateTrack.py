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
            artist, title, extension = keepFormat(audio, filename, directory, options, webScrapingWindow, "Artist - Title")
            filename = str(artist) + ' - ' + str(title) + extension
            audio = FLAC(directory + '/' + str(artist) + ' - ' + str(title) + extension)
            if str(audio["artist"][0]) != artist or str(audio["title"][0]) != title:
                audio["artist"] = artist
                audio['title'] = title
                audio.save()
        else:
            if changeFormat(audio, filename, directory, options, frame, webScrapingWindow, "Artist - Title"):
                artist, title, extension = changeFormat(audio, filename, directory, options, frame, webScrapingWindow, "Artist - Title")
                filename = str(artist) + ' - ' + str(title) + extension
                audio = FLAC(directory + '/' + str(artist) + ' - ' + str(title) + extension)
                if str(audio["artist"][0]) != artist or str(audio["title"][0])!=title:
                    audio["artist"] = artist
                    audio["title"] = title
                    audio.save()
            else:return False, filename
    elif options["Audio naming format (S)"].get() == "Title":
        # rename track so that the artist is removed from the title
        if ' - ' in filename:
            if changeFormat(audio, filename, directory, options, frame, webScrapingWindow, "Artist - Title"):
                artist, title, extension = changeFormat(audio, filename, directory, options, frame, webScrapingWindow, "Title")
                filename = str(title) + extension
                audio = FLAC(directory + '/' + str(title) + extension)
                if str(audio["artist"][0]) != artist or str(audio["title"][0]) != title:
                    audio["artist"] = artist
                    audio["title"] = title
                    audio.save()
            else:return False, filename
        else:
            artist, title, extension = keepFormat(audio, filename, directory, options, webScrapingWindow, "Title")
            filename = str(title) + extension
            audio = FLAC(directory + '/' + str(title) + extension)
            if str(audio["artist"][0]) != artist or str(audio["title"][0]) != title:
                audio["artist"] = artist
                audio['title'] = title
                audio.save()

    # handle replayGain
    if options["Calculate ReplayGain (B)"].get() == True: audio = handleReplayGain(directory, filename, audio, webScrapingWindow)
    return audio, filename

def changeFormat(audio, filename, directory, options, frame, webScrapingWindow, format):
    artist = str(audio['artist'][0])
    if artist == '':
        tk.Label(frame.scrollable_frame, text="No artist information found, aborting procedure", justify='left').pack(anchor='w')
        return False
    title = str(audio['title'][0])
    fileArtist = str(filename.split(' - ')[0])
    fileTitle = str(filename.split(' - ')[1][:-5])
    extension = filename[filename.rfind('.'):]
    #if title is not saved as tag
    if title == '': title = filename[:-5]
    if options["Check Artist for Typos (B)"].get() == True:
        #run through list of possible typos
        artist, title = checkTypos(artist, title, fileArtist, fileTitle, directory, filename, extension, format, webScrapingWindow)
    return artist, title, extension

def keepFormat(audio, filename, directory, options, webScrapingWindow, format):
    artist = str(audio['artist'][0]).strip()
    title = str(audio['title'][0]).strip()
    fileArtist = str(filename.split(' - ')[0])
    fileTitle = str(filename.split(' - ')[1][:-5])
    if artist == '' or title == '':
        artist = str(filename.split(' - ')[0])
        title = str(filename.split(' - ')[1][:-5])
    extension = filename[filename.rfind('.'):]
    if options["Check Artist for Typos (B)"].get() == True:
        # run through list of possible typos
        artist, title = checkTypos(artist, title, fileArtist, fileTitle, directory, filename, extension, format, webScrapingWindow)
    return artist, title, extension

def checkTypos(artist, title, fileArtist, fileTitle, directory, filename, extension, format, webScrapingWindow):
    # check if tag and filename match
    if artist != fileArtist or title != fileTitle:
        artist, title = handleTypo(fileArtist, artist, fileTitle, title, webScrapingWindow, directory, filename, extension, format, "Tag Filename Mismatch")
    # scan artist for numbering prefix
    if '.' in artist:
        artistPrefix = artist[:artist.index('.') + 1]
        newArtist = artist[artist.index('.') + 1:].strip()
        newTitle = title
        if '.' in artistPrefix[0:5]:
            if any(char.isdigit() for char in artistPrefix[0:artistPrefix.index('.')]):
                artist, title = handleTypo(artist, newArtist, title, newTitle, webScrapingWindow, directory, filename, extension, format, "Prefix")
    # scan artist and title for hyphens
    if '-' in artist or '-' in title:
        newArtist = artist
        newTitle = title
        if '-' in artist:
            newArtist = artist.replace('-', ' ')
        if '-' in title:
            newTitle = title.replace('-', ' ')
        artist, title = handleTypo(artist, newArtist, title, newTitle, webScrapingWindow, directory, filename, extension, format, "Hyphen")
    # scan artist and title for lowercase letters
    artistList = artist.split(' ')
    titleList = title.split(' ')
    newArtist = ''
    newTitle = ''
    for word in artistList:
        if word[:1].islower():
            newArtist += word.capitalize() + " "
        else:
            newArtist += word + " "
    newArtist = newArtist.strip()
    for word in titleList:
        if word[:1].islower():
            newTitle += word.capitalize() + " "
        else:
            newTitle += word + " "
    newTitle = newTitle.strip()
    if artist != newArtist or title != newTitle:
        artist, title = handleTypo(artist, newArtist, title, newTitle, webScrapingWindow, directory, filename, extension, format, "Capitalization")
    return artist, title