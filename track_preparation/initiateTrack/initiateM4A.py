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

    # transcribe informal tagnames into formal counterpart
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
            else:audio, filename = compareArtistAndTitle(audio, artist, title, filename, directory, options)
    #only check title tag
    else:
        title = filename[:filename.rfind('.')]
        if title!=str(audio["\xa9nam"][0]):
            #save title to tag if tag is empty
            if str(audio["\xa9nam"][0])=='':
                audio["\xa9nam"] = title
                audio.save()
            else: audio, filename = compareTitle(audio, title, filename, directory, options)
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
                    if handleTypo(artist, newArtist, title, newTitle, "Prefix", options)!=None:
                        artist, title = handleTypo(artist, newArtist, title, newTitle, "Hyphen", options)
                        audio, filename = rename(directory, filename, artist, title, extension, format)

    # scan artist and title for hyphens
    if options["Check for Extraneous Hyphens (B)"].get() == True:
        if '-' in artist or '-' in title:
            newArtist = artist
            newTitle = title
            if '-' in artist: newArtist = artist.replace('-', ' ')
            if '-' in title: newTitle = title.replace('-', ' ')
            if handleTypo(artist, newArtist, title, newTitle, "Hyphen", options) != None:
                artist, title = handleTypo(artist, newArtist, title, newTitle, "Hyphen", options)
                audio, filename = rename(directory, filename, artist, title, extension, format)

    # scan artist and title for capitalization
    if options["Check for Capitalization (B)"].get()==True:
        artistList = artist.split(' ')
        titleList = title.split(' ')
        newArtist, artist, filename = checkCapitalization(artistList, artist, title, "artist", directory, filename, format, options)
        newTitle, title, filename = checkCapitalization(titleList, artist, title, "title", directory, filename, format, options)
        if (artist != newArtist or title != newTitle) and handleTypo(artist, newArtist, title, newTitle, "Capitalization", options) != None:
            artist, title = handleTypo(artist, newArtist, title, newTitle,  "Capitalization", options)
            audio, filename = rename(directory, filename, artist, title, extension, format)
    return audio, filename

def compareArtistAndTitle(audio, artist, title, filename, directory, options):
    # compare file artist with tag artist
    fileArtistList = artist.split(' ')
    tagArtistList = str(audio["\xa9ART"][0]).split(' ')
    if len(fileArtistList) == len(tagArtistList):
        for i in range(len(fileArtistList)):
            if fileArtistList[i] != tagArtistList[i]:
                if fileArtistList[i].lower() == tagArtistList[i].lower() and (fileArtistList[i].capitalize() in options["Always Capitalize (L)"] or fileArtistList[i].lower() in options["Never Capitalize (L)"]):
                    if fileArtistList[i].capitalize() in options["Always Capitalize (L)"]:
                        # capitalize both name and file tag
                        fileArtistList[i] = fileArtistList[i].capitalize()
                        artist = " ".join(fileArtistList)
                        audio, filename = rename(directory, filename, artist, title, filename[filename.rfind("."):], "Artist - Title")
                    elif fileArtistList[i].lower() in options["Never Capitalize (L)"]:
                        # lower both name and file tag
                        fileArtistList[i] = fileArtistList[i].lower()
                        artist = " ".join(fileArtistList)
                        audio, filename = rename(directory, filename, artist, title, filename[filename.rfind("."):], "Artist - Title")
                else:
                    input = handleArtistTitleDiscrepancy(artist, str(audio["\xa9ART"][0]), title, str(audio["\xa9nam"][0]))
                    if input == "file":
                        audio["\xa9ART"] = artist
                        audio["\xa9nam"] = title
                        audio.save()
                    elif input == "tag":
                        extension = filename[filename.rfind('.'):]
                        audio, filename = rename(directory, filename, str(audio["\xa9ART"][0]), str(audio["\xa9nam"][0]), extension, "Artist - Title")
    else:
        input = handleArtistTitleDiscrepancy(artist, str(audio["\xa9ART"][0]), title, str(audio["\xa9nam"][0]))
        if input == "file":
            audio["\xa9ART"] = artist
            audio["\xa9nam"] = title
            audio.save()
        elif input == "tag":
            extension = filename[filename.rfind('.'):]
            audio, filename = rename(directory, filename, str(audio["\xa9ART"][0]), str(audio["\xa9nam"][0]), extension, "Artist - Title")
    # compare file title with tag title
    fileTitleList = title.split(' ')
    tagTitleList = str(audio["\xa9nam"][0]).split(' ')
    if len(fileTitleList) == len(tagTitleList):
        for i in range(len(fileTitleList)):
            if fileTitleList[i] != tagTitleList[i]:
                if fileTitleList[i].lower() == tagTitleList[i].lower() and (
                        fileTitleList[i].capitalize() in options["Always Capitalize (L)"] or fileTitleList[i].lower() in options["Never Capitalize (L)"]):
                    if fileTitleList[i].capitalize() in options["Always Capitalize (L)"]:
                        # capitalize both name and file tag
                        fileTitleList[i] = fileTitleList[i].capitalize()
                        title = " ".join(fileTitleList)
                        audio, filename = rename(directory, filename, artist, title, filename[filename.rfind("."):], "Artist - Title")
                    elif fileTitleList[i].lower() in options["Never Capitalize (L)"]:
                        # lower both name and file tag
                        fileTitleList[i] = fileTitleList[i].lower()
                        title = " ".join(fileTitleList)
                        audio, filename = rename(directory, filename, artist, title, filename[filename.rfind("."):], "Artist - Title")
                else:
                    input = handleArtistTitleDiscrepancy(artist, str(audio["\xa9ART"][0]), title, str(audio["\xa9nam"][0]))
                    if input == "file":
                        audio["\xa9ART"] = artist
                        audio["\xa9nam"] = title
                        audio.save()
                    elif input == "tag":
                        extension = filename[filename.rfind('.'):]
                        audio, filename = rename(directory, filename, str(audio["\xa9ART"][0]), str(audio["\xa9nam"][0]), extension, "Artist - Title")
    else:
        input = handleArtistTitleDiscrepancy(artist, str(audio["\xa9ART"][0]), title, str(audio["\xa9nam"][0]))
        if input == "file":
            audio["\xa9ART"] = artist
            audio["\xa9nam"] = title
            audio.save()
        elif input == "tag":
            extension = filename[filename.rfind('.'):]
            audio, filename = rename(directory, filename, str(audio["\xa9ART"][0]), str(audio["\xa9nam"][0]), extension, "Artist - Title")
    return audio, filename

def compareTitle(audio, title, filename, directory, options):
    # compare file title and tag title
    fileTitleList = title.split(' ')
    tagTitleList = str(audio["\xa9nam"][0]).split(' ')
    if len(fileTitleList) == len(tagTitleList):
        for i in range(len(fileTitleList)):
            if fileTitleList[i] != tagTitleList[i]:
                if fileTitleList[i].lower() == tagTitleList[i].lower() and (fileTitleList[i].capitalize() in options["Always Capitalize (L)"] or fileTitleList[i].lower() in options["Never Capitalize (L)"]):
                    if fileTitleList[i].capitalize() in options["Always Capitalize (L)"]:
                        # capitalize both name and file tag
                        fileTitleList[i] = fileTitleList[i].capitalize()
                        title = " ".join(fileTitleList)
                        audio, filename = rename(directory, filename, str(audio["\xa9nam"][0]), title, filename[filename.rfind("."):], "Title")
                    elif fileTitleList[i].lower() in options["Never Capitalize (L)"]:
                        # lower both name and file tag
                        fileTitleList[i] = fileTitleList[i].lower()
                        title = " ".join(fileTitleList)
                        audio, filename = rename(directory, filename, str(audio["\xa9nam"][0]), title, filename[filename.rfind("."):], "Title")
                else:
                    input = handleTitleDiscrepancy(title, str(audio["\xa9nam"][0]))
                    if input == "file":
                        audio["\xa9nam"] = title
                        audio.save()
                    elif input == "tag":
                        extension = filename[filename.rfind('.'):]
                        audio, filename = rename(directory, filename, str(audio["\xa9ART"][0]), str(audio["\xa9nam"][0]), extension, "Title")
    else:
        input = handleTitleDiscrepancy(title, str(audio["title"][0]))
        if input == "file":
            audio["\xa9nam"] = title
            audio.save()
        elif input == "tag":
            extension = filename[filename.rfind('.'):]
            audio, filename = rename(directory, filename, str(audio["\xa9ART"][0]), str(audio["\xa9nam"][0]), extension, "Title")
    return audio, filename

def checkCapitalization(list, artist, title, subject, directory, filename, format, options):
    newString = ''
    for word in list:
        if word.lower() in (string.lower() for string in options["Always Capitalize (L)"]):
            if word != word.capitalize():
                # recreate correct spelling
                if subject == "artist": artist = artist.replace(word, word.capitalize())
                elif subject == "title": title = title.replace(word, word.capitalize())
                audio, filename = rename(directory, filename, artist, title, ".flac", format)
            newString += word.capitalize() + ' '
        elif word.lower() in (string.lower() for string in options["Never Capitalize (L)"]):
            if word != word.lower():
                # recreate correct spelling
                if subject == "artist": artist = artist.replace(word, word.lower())
                elif subject == "title": title = title.replace(word, word.lower())
                audio, filename = rename(directory, filename, artist, title, ".flac", format)
            newString += word.lower() + ' '
        else:
            if word[:1].islower(): newString += word.capitalize() + ' '
            else: newString += word + ' '
    newString = newString.strip()
    if subject == "artist": return newString, artist, filename
    elif subject == "title": return newString, title, filename

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