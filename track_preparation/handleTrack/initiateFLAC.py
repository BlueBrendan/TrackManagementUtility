from mutagen.flac import FLAC
from tkinter import messagebox
import tkinter as tk
import os

#import methods
from track_preparation.handleTypo import handleArtistTitleDiscrepancy
from track_preparation.handleTypo import handleTitleDiscrepancy
from track_preparation.handleTypo import handleTypo
from track_preparation.handleReplayGain import handleReplayGain

def initiateFLAC(filename, directory, frame, webScrapingWindow, options):
    audio = FLAC(str(directory) + "/" + str(filename))
    # verify artist information is present before preceeding
    if ' - ' not in filename and str(audio['artist'][0]) == '':
        tk.Label(frame.scrollable_frame, text="No artist information found, aborting procedure", justify='left').pack(anchor='w')
        return False, filename

    # transcribe formal tagnames into informal counterpart
    formalTagDict = {
        'artist': 'Artist',
        'album': 'Album',
        'albumartist': 'Album Artist',
        'bpm': 'BPM',
        'comment': 'Comment',
        'compilation': 'Compilation',
        'copyright': 'Copyright',
        'discnumber': 'Discnumber',
        'genre': 'Genre',
        'initialkey': 'Key',
        'date': 'Release Date',
        'title': 'Title',
        'replaygain_track_gain': 'ReplayGain',
    }
    # transcribe informal tagnames into formal counterpart
    informalTagDict = {
        'Artist': 'artist',
        'Album': 'album',
        'Album Artist': 'albumartist',
        'BPM': 'bpm',
        'Comment': 'comment',
        'Compilation': 'compilation',
        'Copyright': 'copyright',
        'Discnumber': 'discnumber',
        'Genre': 'genre',
        'Key': 'initialkey',
        'Release Date': 'date',
        'Title': 'title',
        'ReplayGain': 'replaygain_track_gain',
    }
    fileParameters = []
    for tag in audio:
        # delete extraneous tags if the tag is not in the list of selected tags and the delete unselected tags option is activated
        if (tag not in formalTagDict or formalTagDict[tag] not in options["Selected Tags (L)"]) and options["Delete Unselected Tags (B)"].get()==True:
            audio[tag] = ""
            audio.pop(tag)
            audio.save()
        else: fileParameters.append(tag)
    for tag in options["Selected Tags (L)"]:
        tag = informalTagDict[tag]
        # add tags of interest if missing
        if tag not in fileParameters:
            try:
                audio[tag] = ""
                audio.save()
            except:
                messagebox.showinfo("Permission Error", "Unable to save tags, file may be open somewhere")
                webScrapingWindow.lift()
                return False, filename

    #check for discrepancies between tags and filename
    #check both artist and title tags
    if ' - ' in filename:
        artist = str(filename.split(' - ')[0])
        title = str(filename.split(' - ')[1][:-5])
        if artist!=str(audio['artist'][0]) or title!=str(audio['title'][0]):
            # save artist and title to tag if both are empty
            if str(audio['artist'][0]) == '' and str(audio['title'][0]) == '':
                audio['artist'] = artist
                audio['title'] = title
                audio.save()
            else: audio, filename = handleArtistTitleDiscrepancy(artist, str(audio['artist'][0]), title, str(audio['title'][0]), audio, filename, directory, webScrapingWindow)
    #only check title tag
    else:
        title = str(filename[:-5])
        if title!=str(audio['title'][0]):
            #save title to tag if tag is empty
            if str(audio['title'][0])=='':
                audio['title'] = title
                audio.save()
            else: audio, filename = handleTitleDiscrepancy(title, str(audio['title'][0]), audio, filename, directory, webScrapingWindow)

    # handle naming format and typo check
    if options["Audio naming format (S)"].get() == "Artist - Title":
        # rename track so that the artist is appended at the front of the title
        if ' - ' not in filename:
            artist = str(audio['artist'][0])
            os.rename(directory + '/' + filename, directory + '/' + artist + ' - ' + filename)
            filename = artist + ' - ' + filename
            audio = FLAC(directory + '/' + filename)
        if options["Scan Filename and Tags (B)"].get() == True: audio, filename = extractArtistAndTitle(audio, filename, directory, options, frame, webScrapingWindow, "Artist - Title")

    elif options["Audio naming format (S)"].get() == "Title":
        # rename track so that the artist is removed from the title
        if ' - ' in filename:
            os.rename(directory + '/' + filename, directory + '/' + filename[filename.index(' - ')+3:])
            filename = filename[filename.index(' - ')+3:]
            audio = FLAC(directory + '/' + filename)
        if options["Scan Filename and Tags (B)"].get() == True: audio, filename = extractArtistAndTitle(audio, filename, directory, options, frame, webScrapingWindow, "Title")

    # handle replayGain
    if options["Calculate ReplayGain (B)"].get() == True: audio = handleReplayGain(directory, filename, audio, webScrapingWindow)
    return audio, filename

def extractArtistAndTitle(audio, filename, directory, options, frame, webScrapingWindow, format):
    extension = filename[filename.rfind('.'):]
    if ' - ' in filename:
        artist = str(audio['artist'][0])
        if artist == '': artist = str(filename.split(' - ')[0])
        title = str(audio['title'][0])
        # if title is not saved as tag
        if title == '': title = str(filename.split(' - ')[1][:-5])
    else:
        artist = str(audio['artist'][0])
        title = str(audio['title'][0])
        # if title is not saved as tag
        if title == '':
            title = filename[:-5]
    # run through list of possible typos
    audio, filename = checkTypos(audio, artist, title, directory, filename, extension, format, options, webScrapingWindow)
    return audio, filename

def checkTypos(audio, artist, title, directory, filename, extension, format, options, webScrapingWindow):
    # scan artist for numbering prefix
    if options["Check for Numbering Prefix (B)"].get() == True:
        if '.' in artist:
            artistPrefix = artist[:artist.index('.') + 1]
            newArtist = artist[artist.index('.') + 1:].strip()
            newTitle = title
            if '.' in artistPrefix[0:5]:
                if any(char.isdigit() for char in artistPrefix[0:artistPrefix.index('.')]): artist, title, audio, filename = handleTypo(audio, artist, newArtist, title, newTitle, webScrapingWindow, directory, filename, extension, format, "Prefix")

    # scan artist and title for hyphens
    if options["Check for Extraneous Hyphens (B)"].get() == True:
        if '-' in artist or '-' in title:
            newArtist = artist
            newTitle = title
            if '-' in artist: newArtist = artist.replace('-', ' ')
            if '-' in title: newTitle = title.replace('-', ' ')
            artist, title, audio, filename = handleTypo(audio, artist, newArtist, title, newTitle, webScrapingWindow, directory, filename, extension, format, "Hyphen")

    # scan artist and title for capitalization
    if options["Check for Capitalization (B)"].get()==True:
        artistList = artist.split(' ')
        titleList = title.split(' ')
        newArtist = ''
        newTitle = ''
        for word in artistList:
            if word[:1].islower(): newArtist += word.capitalize() + " "
            else: newArtist += word + " "
        newArtist = newArtist.strip()
        for word in titleList:
            if word[:1].islower(): newTitle += word.capitalize() + " "
            else: newTitle += word + " "
        newTitle = newTitle.strip()
        if artist != newArtist or title != newTitle: artist, title, audio, filename = handleTypo(audio, artist, newArtist, title, newTitle, webScrapingWindow, directory, filename, extension, format, "Capitalization")
    return audio, filename