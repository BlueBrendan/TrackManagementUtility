from mutagen.aiff import AIFF
from mutagen.id3._frames import *
from tkinter import messagebox
from PIL import Image
from io import BytesIO

#import methods
from track_preparation.handleDiscrepancy import handleArtistTitleDiscrepancy
from track_preparation.handleDiscrepancy import handleTitleDiscrepancy
from track_preparation.initiateTrack.commonInitiationOperations import checkTypos
from track_preparation.initiateTrack.commonInitiationOperations import handleStaticNamingConvention
from track_preparation.initiateTrack.commonInitiationOperations import rename
from track_preparation.initiateTrack.commonInitiationOperations import saveThumbnail

def initiateAIFF(filename, directory, thumbnails, options):
    audio = AIFF(str(directory) + "/" + str(filename))
    # verify artist information is present before preceeding
    if ' - ' not in filename and str(audio['TCON']) == '':
        messagebox.showinfo("No artist information found, aborting procedure")
        return False, False, False

    # transcribe formal tagnames into informal counterpart
    formalTagDict = {
        'TPE1': 'Artist',
        'TALB': 'Album',
        'TPE2': 'Album Artist',
        'TBPM': 'BPM',
        'COMM::eng': 'Comment',
        'TCMP': 'Compilation',
        'TCOP': 'Copyright',
        'TPOS': 'Discnumber',
        'TCON': 'Genre',
        'APIC:': 'Image',
        'TKEY': 'Key',
        'TDRC': 'Release_Date',
        'TIT2': 'Title',
        'TXXX:replaygain_track_gain': 'ReplayGain',
    }
    # transcribe informal tagnames into formal counterpart
    informalTagDict = {v: k for k, v in formalTagDict.items()}

    ID3Frames = {
        'TPE1': TPE1,
        'TALB': TALB,
        'TPE2': TPE2,
        'TBPM': TBPM,
        'COMM': COMM,
        'TCMP': TCMP,
        'TCOP': TCOP,
        'TPOS': TPOS,
        'TCON': TCON,
        'APIC:': APIC,
        'TKEY': TKEY,
        'TDRC': TDRC,
        'TIT2': TIT2,
        'TXXX': TXXX,

    }
    fileParameters = []
    tagList = list(audio.keys())
    for tag in tagList:
        # delete extraneous tags if the tag is not in the list of selected tags and the delete unselected tags option is activated
        if (tag not in formalTagDict or formalTagDict[tag] not in options["Selected Tags (L)"]) and options["Delete Unselected Tags (B)"].get()==True:
            audio.pop(tag)
            audio.save()
        else: fileParameters.append(tag)
    for tag in options["Selected Tags (L)"]:
        if tag in informalTagDict:
            tag = informalTagDict[tag]
            # add tags of interest if missing
            if tag not in fileParameters:
                try:
                    if "COMM" in tag: audio[tag] = COMM(encoding=3, lang="eng", test="")
                    elif "TXXX" in tag: audio[tag] = TXXX(encoding=3, desc="replaygain_track_gain", test="")
                    else: audio[tag] = ID3Frames[tag](encoding=3, test="")
                    audio.save()
                except:
                    messagebox.showinfo("Permission Error", "Unable to save tags, file may be open somewhere")
                    return False, False, False

    #check for discrepancies between tags and filename
    #check both artist and title tags
    if ' - ' in filename:
        artist = filename.split(' - ')[0]
        title = filename[filename.index(filename.split(' - ')[1]):filename.rfind('.')]
        if artist!=str(audio["TPE1"]) or title!=str(audio["TIT2"]):
            # save artist and title to tag if both are empty
            if str(audio["TPE1"]) == '' and str(audio["TIT2"]) == '':
                audio["TPE1"] = TPE1(encoding=3, text=artist)
                audio["TIT2"] = TIT2(encoding=3, text=title)
                audio.save()
            else: audio, filename = compareArtistAndTitle(audio, artist, title, filename, directory, options)
    #only check title tag
    else:
        title = filename[:filename.rfind('.')]
        if title!=str(audio["TIT2"]):
            #save title to tag if tag is empty
            if str(audio["TIT2"])=='':
                audio["TIT2"] = TIT2(encoding=3, text=title)
                audio.save()
            else: audio, filename = compareTitle(audio, title, filename, directory, options)

    # handle naming format and typo check
    if options["Audio naming format (S)"].get() == "Artist - Title" or options['Audio naming format (S)'].get() == 'Title':
        namingConvention = options['Audio naming format (S)'].get()
        artist = str(audio["TPE1"])
        audio, filename = handleStaticNamingConvention(audio, filename, artist, title, directory, namingConvention)
        if options["Scan Filename and Tags (B)"].get() == True and type(audio) != bool: audio, filename, options = extractArtistAndTitle(audio, filename, directory, options, namingConvention)

    if type(audio) != bool:
        # save thumbnail to list
        image = audio["APIC:"]
        if image.data != b'':
            stream = BytesIO(image.data)
            image = Image.open(stream).convert("RGBA")
            thumbnails = saveThumbnail(image, thumbnails)
            stream.close()
        else: thumbnails = saveThumbnail("NA", thumbnails)
    return audio, filename, informalTagDict, thumbnails, options

def extractArtistAndTitle(audio, filename, directory, options, namingConvention):
    extension = filename[filename.rfind('.'):]
    if ' - ' in filename:
        artist = str(audio["TPE1"])
        if artist == '': artist = str(filename.split(' - ')[0])
        title = str(audio["TIT2"])
        # if title is not saved as tag
        if title == '': title = str(filename.split(' - ')[1][:-5])
    else:
        artist = str(audio["TPE1"])
        title = str(audio["TIT2"])
        # if title is not saved as tag
        if title == '':
            title = filename[:-5]
    # run through list of possible typos
    if options["Scan Filename and Tags (B)"]: audio, filename, options = checkTypos(audio, artist, title, directory, filename, extension, namingConvention, options)
    return audio, filename, options

def compareArtistAndTitle(audio, artist, title, filename, directory, options):
    # compare file artist with tag artist
    fileArtistList = artist.split(' ')
    tagArtistList = str(audio["TPE1"]).split(' ')
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
                    input = handleArtistTitleDiscrepancy(artist, str(audio["TPE1"]), title, str(audio["TIT2"]))
                    if input == "file":
                        audio["TPE1"] = TPE1(encoding=3, text=artist)
                        audio["TIT2"] = TIT2(encoding=3, text=title)
                        audio.save()
                    elif input == "tag":
                        extension = filename[filename.rfind('.'):]
                        audio, filename = rename(directory, filename, str(audio["TPE1"]), str(audio["TIT2"]), extension, "Artist - Title")
                    break
    else:
        input = handleArtistTitleDiscrepancy(artist, str(audio["TPE1"]), title, str(audio["TIT2"]))
        if input == "file":
            audio["TPE1"] = TPE1(encoding=3, text=artist)
            audio["TIT2"] = TIT2(encoding=3, text=title)
            audio.save()
        elif input == "tag":
            extension = filename[filename.rfind('.'):]
            audio, filename = rename(directory, filename, str(audio["TPE1"]), str(audio["TIT2"]), extension, "Artist - Title")
    # compare file title with tag title
    fileTitleList = title.split(' ')
    tagTitleList = str(audio["TIT2"]).split(' ')
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
                    input = handleArtistTitleDiscrepancy(artist, str(audio["TPE1"]), title, str(audio["TIT2"]))
                    if input == "file":
                        audio["TPE1"] = TPE1(encoding=3, text=artist)
                        audio["TIT2"] = TIT2(encoding=3, text=title)
                        audio.save()
                    elif input == "tag":
                        extension = filename[filename.rfind('.'):]
                        audio, filename = rename(directory, filename, str(audio["TPE1"]), str(audio["TIT2"]), extension, "Artist - Title")
                    break
    else:
        input = handleArtistTitleDiscrepancy(artist, str(audio["TPE1"]), title, str(audio["TIT2"]))
        if input == "file":
            audio["TPE1"] = TPE1(encoding=3, text=artist)
            audio["TIT2"] = TIT2(encoding=3, text=title)
            audio.save()
        elif input == "tag":
            extension = filename[filename.rfind('.'):]
            audio, filename = rename(directory, filename, str(audio["TPE1"]), str(audio["TIT"]), extension, "Artist - Title")
    return audio, filename

def compareTitle(audio, title, filename, directory, options):
    # compare file title and tag title
    fileTitleList = title.split(' ')
    tagTitleList = str(audio["TIT2"]).split(' ')
    if len(fileTitleList) == len(tagTitleList):
        for i in range(len(fileTitleList)):
            if fileTitleList[i] != tagTitleList[i]:
                if fileTitleList[i].lower() == tagTitleList[i].lower() and (fileTitleList[i].capitalize() in options["Always Capitalize (L)"] or fileTitleList[i].lower() in options["Never Capitalize (L)"]):
                    if fileTitleList[i].capitalize() in options["Always Capitalize (L)"]:
                        # capitalize both name and file tag
                        fileTitleList[i] = fileTitleList[i].capitalize()
                        title = " ".join(fileTitleList)
                        audio, filename = rename(directory, filename, str(audio["TPE1"]), title, filename[filename.rfind("."):], "Title")
                    elif fileTitleList[i].lower() in options["Never Capitalize (L)"]:
                        # lower both name and file tag
                        fileTitleList[i] = fileTitleList[i].lower()
                        title = " ".join(fileTitleList)
                        audio, filename = rename(directory, filename, str(audio["TPE1"]), title, filename[filename.rfind("."):], "Title")
                else:
                    input = handleTitleDiscrepancy(title, str(audio["TIT2"]))
                    if input == "file":
                        audio["title"] = title
                        audio.save()
                    elif input == "tag":
                        extension = filename[filename.rfind('.'):]
                        audio, filename = rename(directory, filename, str(audio["TPE1"]), str(audio["TIT2"]), extension, "Title")
    else:
        input = handleTitleDiscrepancy(title, str(audio["title"][0]))
        if input == "file":
            audio["TIT2"] = TIT2(encoding=3, text=title)
            audio.save()
        elif input == "tag":
            extension = filename[filename.rfind('.'):]
            audio, filename = rename(directory, filename, str(audio["TPE1"]), str(audio["TIT2"]), extension, "Title")
    return audio, filename