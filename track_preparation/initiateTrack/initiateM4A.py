from mutagen.mp4 import MP4
from tkinter import messagebox
import tkinter as tk
import os

#import methods
from track_preparation.handleDiscrepancy import handleArtistTitleDiscrepancy
from track_preparation.handleDiscrepancy import handleTitleDiscrepancy
from track_preparation.handleTypo import handleTypo

def initiateM4A(filename, directory, options):
    audio = MP4(str(directory) + "/" + str(filename))
    # verify artist information is present before preceeding
    if ' - ' not in filename and str(audio["\xa9ART"][0]) == '':
        messagebox.showinfo("No artist information found, aborting procedure")
        return False, filename

    # transcribe formal tagnames into informal counterpart
    formalTagDict = {
        "\xa9ART": 'Artist',
        "\alb": 'Album',
        "aART": 'Album Artist',
        "tmpo": 'BPM',
        "\xa9cmt": 'Comment',
        "cpil": 'Compilation', #bool
        "cprt": 'Copyright',
        'disk': 'Discnumber', #[0]
        "\xa9gen": 'Genre',
        "covr": 'Image',
        "----:com.apple.iTunes:INITIALKEY": 'Key',
        "\xa9day": 'Release_Date',
        "\xa9nam": 'Title',
        "----:com.apple.iTunes:replaygain_track_gain": 'ReplayGain',
    }
    # audio["----:com.apple.iTunes:INITIALKEY"] = 'C din'
    # print(audio.pprint())

#     # transcribe informal tagnames into formal counterpart
    informalTagDict = {v: k for k, v in formalTagDict.items()}
    fileParameters = []
    tagList = list(audio.keys())
    for tag in tagList:
        # delete extraneous tags if the tag is not in the list of selected tags and the delete unselected tags option is activated
        if (tag not in formalTagDict or formalTagDict[tag] not in options["Selected Tags (L)"]) and options["Delete Unselected Tags (B)"].get()==True:
            audio[tag] = ""
            audio.pop(tag)
            audio.save()
        else: fileParameters.append(tag)
    for tag in options["Selected Tags (L)"]:
        if tag in informalTagDict:
            tag = informalTagDict[tag]
            # add tags of interest if missing
            if tag not in fileParameters:
                try:
                    audio[tag] = ""
                    audio.save()
                except:
                    messagebox.showinfo("Permission Error", "Unable to save tags, file may be open somewhere")
                    return False, filename
#
#     #check for discrepancies between tags and filename
    #check both artist and title tags
    if ' - ' in filename:
        artist = filename.split(' - ')[0]
        title = filename[filename.index(filename.split(' - ')[1]):filename.rfind('.')]
        if artist!=str(audio["\xa9ART"][0]) or title!=str(audio["\xa9nam"][0]):
            # save artist and title to tag if both are empty
            if str(audio["\xa9ART"][0]) == '' and str(audio["\xa9nam"][0]) == '':
                audio["\xa9ART"] = artist
                audio["\xa9nam"] = title
                audio.save()
            else:
                input = handleArtistTitleDiscrepancy(artist, str(audio["\xa9ART"][0]), title, str(audio["\xa9nam"][0]))
                if input == "file":
                    audio["\xa9ART"] = artist
                    audio["\xa9nam"] = title
                    audio.save()
                elif input == "tag":
                    extension = filename[filename.rfind('.'):]
                    os.rename(directory + '/' + filename, str(directory) + '/' + str(audio["\xa9ART"][0]) + " - " + str(audio["\xa9nam"][0]) + extension)
                    filename = str(audio["\xa9ART"][0]) + " - " + str(audio["\xa9nam"][0]) + extension
                    audio = MP4(str(directory) + '/' + filename)
    #only check title tag
    else:
        title = filename[:filename.rfind('.')]
        if title!=str(audio["\xa9nam"][0]):
            #save title to tag if tag is empty
            if str(audio["\xa9nam"][0])=='':
                audio["\xa9nam"] = title
                audio.save()
            else:
                input = handleTitleDiscrepancy(title, str(audio["\xa9nam"][0]))
                if input == "file":
                    audio["\xa9nam"] = title
                    audio.save()
                elif input == "tag":
                    extension = filename[filename.rfind('.'):]
                    os.rename(directory + '/' + filename, str(directory) + '/' + str(audio["\xa9ART"][0]) + extension)
                    filename = str(audio["\xa9ART"][0]) + extension
                    audio = MP4(str(directory) + '/' + filename)
#
#     # handle naming format and typo check
    if options["Audio naming format (S)"].get() == "Artist - Title":
        # rename track so that the artist is appended at the front of the title
        if ' - ' not in filename:
            artist = str(audio["\xa9ART"][0])
            os.rename(directory + '/' + filename, directory + '/' + artist + ' - ' + filename)
            filename = artist + ' - ' + filename
            audio = MP4(directory + '/' + filename)
        if options["Scan Filename and Tags (B)"].get() == True: audio, filename = extractArtistAndTitle(audio, filename, directory, options, "Artist - Title")

    elif options["Audio naming format (S)"].get() == "Title":
        # rename track so that the artist is removed from the title
        if ' - ' in filename:
            os.rename(directory + '/' + filename, directory + '/' + filename[filename.index(' - ')+3:])
            filename = filename[filename.index(' - ')+3:]
            audio = MP4(directory + '/' + filename)
        if options["Scan Filename and Tags (B)"].get() == True: audio, filename = extractArtistAndTitle(audio, filename, directory, options, "Title")

    return audio, filename, informalTagDict

def extractArtistAndTitle(audio, filename, directory, options, format):
    extension = filename[filename.rfind('.'):]
    if ' - ' in filename:
        artist = str(audio["\xa9ART"][0])
        if artist == '': artist = str(filename.split(' - ')[0])
        title = str(audio["\xa9nam"][0])
        # if title is not saved as tag
        if title == '': title = str(filename.split(' - ')[1][:-5])
    else:
        artist = str(audio["\xa9ART"][0])
        title = str(audio["\xa9nam"][0])
        # if title is not saved as tag
        if title == '':
            title = filename[:-5]
    # run through list of possible typos
    audio, filename = checkTypos(audio, artist, title, directory, filename, extension, format, options)
    return audio, filename

def checkTypos(audio, artist, title, directory, filename, extension, format, options):
    # scan artist for numbering prefix
    if options["Check for Numbering Prefix (B)"].get() == True:
        if '.' in artist:
            artistPrefix = artist[:artist.index('.') + 1]
            newArtist = artist[artist.index('.') + 1:].strip()
            newTitle = title
            if '.' in artistPrefix[0:5]:
                if any(char.isdigit() for char in artistPrefix[0:artistPrefix.index('.')]):
                    if handleTypo(artist, newArtist, title, newTitle,"Prefix")!=None:
                        artist, title = handleTypo(artist, newArtist, title, newTitle,"Hyphen")
                        audio, filename = rename(directory, filename, artist, title, extension, format)

    # scan artist and title for hyphens
    if options["Check for Extraneous Hyphens (B)"].get() == True:
        if '-' in artist or '-' in title:
            newArtist = artist
            newTitle = title
            if '-' in artist: newArtist = artist.replace('-', ' ')
            if '-' in title: newTitle = title.replace('-', ' ')
            if handleTypo(artist, newArtist, title, newTitle, "Hyphen") != None:
                artist, title = handleTypo(artist, newArtist, title, newTitle, "Hyphen")
                audio, filename = rename(directory, filename, artist, title, extension, format)

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
        if (artist != newArtist or title != newTitle) and handleTypo(artist, newArtist, title, newTitle, "Capitalization") != None:
            artist, title = handleTypo(artist, newArtist, title, newTitle, "Capitalization")
            audio, filename = rename(directory, filename, artist, title, extension, format)
    return audio, filename

def rename(directory, filename, artist, title, extension, format):
    if format == "Artist - Title":
        try:
            os.rename(directory + '/' + filename, str(directory) + '/' + str(artist) + ' - ' + str(title) + extension)
            filename = str(artist) + ' - ' + str(title) + extension
            audio = MP4(str(directory) + '/' + str(artist) + ' - ' + str(title) + extension)
            audio["\xa9ART"] = artist
            audio["\xa9nam"] = title
            audio.save()
            return audio, filename
        except PermissionError:messagebox.showinfo("Permission Error", "File cannot be renamed, it may still be open")
    elif format == "Title":
        try:
            os.rename(directory + '/' + filename, str(directory) + '/' + str(title) + extension)
            filename = str(title) + extension
            audio = MP4(str(directory) + '/' + str(title) + extension)
            audio["\xa9ART"] = artist
            audio["\xa9nam"] = title
            audio.save()
            return audio, filename
        except PermissionError:messagebox.showinfo("Permission Error", "File cannot be renamed, it may still be open")