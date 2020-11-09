from mutagen.flac import FLAC
from tkinter import messagebox
from PIL import Image
from io import BytesIO
import os

#import methods
from track_preparation.handleDiscrepancy import handleArtistTitleDiscrepancy
from track_preparation.handleDiscrepancy import handleTitleDiscrepancy
from track_preparation.initiateTrack.commonInitiationOperations import checkTypos
from track_preparation.initiateTrack.commonInitiationOperations import handleStaticNamingConvention
from track_preparation.initiateTrack.commonInitiationOperations import rename
from track_preparation.initiateTrack.commonInitiationOperations import saveThumbnail

def initiateFLAC(filename, directory, thumbnails, options):
    audio = FLAC(str(directory) + "/" + str(filename))
    # verify artist information is present before preceeding
    if ' - ' not in filename and str(audio['artist'][0]) == '':
        messagebox.showinfo("No artist information found, aborting procedure")
        return False, False, False

    # transcribe formal tagnames into informal counterpart
    formalTagDict = {
        'artist': 'Artist',
        'album': 'Album',
        'albumartist': 'Album_Artist',
        'bpm': 'BPM',
        'comment': 'Comment',
        'compilation': 'Compilation',
        'copyright': 'Copyright',
        'discnumber': 'Discnumber',
        'genre': 'Genre',
        'initialkey': 'Key',
        'date': 'Release_Date',
        'title': 'Title',
        'replaygain_track_gain': 'ReplayGain',
    }
    # transcribe informal tagnames into formal counterpart
    informalTagDict = {v: k for k, v in formalTagDict.items()}
    fileParameters = []
    for tag in audio:
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
                    return False, False, False

    #check for discrepancies between tags and filename
    #check both artist and title tags
    if ' - ' in filename:
        artist = filename.split(' - ')[0]
        title = filename[filename.index(filename.split(' - ')[1]):filename.rfind('.')]
        if artist!=str(audio['artist'][0]) or title!=str(audio['title'][0]):
            # save artist and title to tag if both are empty
            if str(audio['artist'][0]) == '' and str(audio['title'][0]) == '':
                audio['artist'] = artist
                audio['title'] = title
                audio.save()
            else:
                audio, filename = compareArtistAndTitle(audio, artist, title, filename, directory, options)
    #only check title tag
    else:
        title = filename[:filename.rfind('.')]
        if title!=str(audio['title'][0]):
            #save title to tag if tag is empty
            if str(audio['title'][0])=='':
                audio['title'] = title
                audio.save()
            else: audio, filename = compareTitle(audio, title, filename, directory, options)

    # handle naming format and typo check
    namingConvention = options['Audio naming format (S)'].get()
    artist = str(audio['artist'][0])
    audio, filename = handleStaticNamingConvention(audio, filename, artist, title, directory, namingConvention)
    if options["Scan Filename and Tags (B)"].get() == True and type(audio) != bool: audio, filename, options = extractArtistAndTitle(audio, filename, directory, options, namingConvention)
    if type(audio) != bool:
        # save thumbnail to list
        images = audio.pictures
        # append thumbnail image to list if artwork exists
        if len(images) > 0:
            stream = BytesIO(images[0].data)
            image = Image.open(stream).convert("RGBA")
            thumbnails = saveThumbnail(image, thumbnails)
            stream.close()
        else: thumbnails = saveThumbnail("NA", thumbnails)
    return audio, filename, informalTagDict, thumbnails, options

def extractArtistAndTitle(audio, filename, directory, options, namingConvention):
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
        if title == '': title = filename[:-5]
    # run through list of possible typos
    if options["Scan Filename and Tags (B)"]: audio, filename, options = checkTypos(audio, artist, title, directory, filename, extension, namingConvention, options)
    return audio, filename, options

def compareArtistAndTitle(audio, artist, title, filename, directory, options):
    # compare file artist with tag artist
    fileArtistList = artist.split(' ')
    tagArtistList = str(audio["artist"][0]).split(' ')
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
                    input = handleArtistTitleDiscrepancy(artist, str(audio["artist"][0]), title, str(audio["title"][0]))
                    if input == "file":
                        audio['artist'] = artist
                        audio['title'] = title
                        audio.save()
                    elif input == "tag":
                        extension = filename[filename.rfind('.'):]
                        audio, filename = rename(directory, filename, str(audio["artist"][0]), str(audio["title"][0]), extension, "Artist - Title")
                    break
    else:
        input = handleArtistTitleDiscrepancy(artist, str(audio["artist"][0]), title, str(audio["title"][0]))
        if input == "file":
            audio['artist'] = artist
            audio['title'] = title
            audio.save()
        elif input == "tag":
            extension = filename[filename.rfind('.'):]
            audio, filename = rename(directory, filename, str(audio["artist"][0]), str(audio["title"][0]), extension, "Artist - Title")
    # compare file title with tag title
    fileTitleList = title.split(' ')
    tagTitleList = str(audio["title"][0]).split(' ')
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
                    input = handleArtistTitleDiscrepancy(artist, str(audio["artist"][0]), title, str(audio["title"][0]))
                    if input == "file":
                        audio['artist'] = artist
                        audio['title'] = title
                        audio.save()
                    elif input == "tag":
                        extension = filename[filename.rfind('.'):]
                        audio, filename = rename(directory, filename, str(audio["artist"][0]), str(audio["title"][0]), extension, "Artist - Title")
                    break
    else:
        input = handleArtistTitleDiscrepancy(artist, str(audio["artist"][0]), title, str(audio["title"][0]))
        if input == "file":
            audio['artist'] = artist
            audio['title'] = title
            audio.save()
        elif input == "tag":
            extension = filename[filename.rfind('.'):]
            audio, filename = rename(directory, filename, str(audio["artist"][0]), str(audio["title"][0]), extension, "Artist - Title")
    return audio, filename

def compareTitle(audio, title, filename, directory, options):
    # compare file title and tag title
    fileTitleList = title.split(' ')
    tagTitleList = str(audio["title"][0]).split(' ')
    if len(fileTitleList) == len(tagTitleList):
        for i in range(len(fileTitleList)):
            if fileTitleList[i] != tagTitleList[i]:
                if fileTitleList[i].lower() == tagTitleList[i].lower() and (fileTitleList[i].capitalize() in options["Always Capitalize (L)"] or fileTitleList[i].lower() in options["Never Capitalize (L)"]):
                    if fileTitleList[i].capitalize() in options["Always Capitalize (L)"]:
                        # capitalize both name and file tag
                        fileTitleList[i] = fileTitleList[i].capitalize()
                        title = " ".join(fileTitleList)
                        audio, filename = rename(directory, filename, str(audio["artist"][0]), title, filename[filename.rfind("."):], "Title")
                    elif fileTitleList[i].lower() in options["Never Capitalize (L)"]:
                        # lower both name and file tag
                        fileTitleList[i] = fileTitleList[i].lower()
                        title = " ".join(fileTitleList)
                        audio, filename = rename(directory, filename, str(audio["artist"][0]), title, filename[filename.rfind("."):], "Title")
                else:
                    input = handleTitleDiscrepancy(title, str(audio["title"][0]))
                    if input == "file":
                        audio["title"] = title
                        audio.save()
                    elif input == "tag":
                        extension = filename[filename.rfind('.'):]
                        audio, filename = rename(directory, filename, str(audio["artist"][0]), str(audio["title"][0]), extension, "Title")
    else:
        input = handleTitleDiscrepancy(title, str(audio["title"][0]))
        if input == "file":
            audio["title"] = title
            audio.save()
        elif input == "tag":
            extension = filename[filename.rfind('.'):]
            audio, filename = rename(directory, filename, str(audio["artist"][0]), str(audio["title"][0]), extension, "Title")
    return audio, filename