from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.aiff import AIFF
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.id3._frames import *
from PIL import Image
from tkinter import messagebox
import os
import getpass

# import methods
from track_preparation.handleTypo import handleDiscrepancy

def checkCapitalization(artist, title, filename, directory, audio, options, extension, namingConvention):
    artistList = artist.split(' ')
    titleList = title.split(' ')
    newArtistList, artistList, artist, filename = buildCapitalizationList(artistList, artist, title, "artist", directory, filename, namingConvention, options)
    newTitleList, titleList, title, filename = buildCapitalizationList(titleList, artist, title, "title", directory, filename, namingConvention, options)
    for index, (word, newWord) in enumerate(zip(artistList, newArtistList)):
        if word != newWord:
            artist, options, renameFile = handleDiscrepancy(artistList, newArtistList, index, "Capitalization", options)
            if renameFile:
                audio, filename = rename(directory, filename, artist, title, extension, namingConvention)
                artistList[index] = newArtistList[index]
    for index, (word, newWord) in enumerate(zip(titleList, newTitleList)):
        if word != newWord:
            title, options, renameFile = handleDiscrepancy(titleList, newTitleList, index, "Capitalization", options)
            if renameFile:
                audio, filename = rename(directory, filename, artist, title, extension, namingConvention)
                titleList[index] = newTitleList[index]
    return audio, filename

def buildCapitalizationList(list, artist, title, subject, directory, filename, namingConvention, options):
    newString = []
    for index, word in enumerate(list, start=0):
        if word.lower() in (string.lower() for string in options["Always Capitalize (L)"]):
            newString.append(word.capitalize())
            if word != word.capitalize():
                # recreate correct spelling
                if subject == "artist":
                    artist = artist.replace(word, word.capitalize())
                    list[index] = artist
                elif subject == "title":
                    title = title.replace(word, word.capitalize())
                    list[index] = title
                audio, filename = rename(directory, filename, artist, title, ".flac", namingConvention)
        elif word.lower() in (string.lower() for string in options["Never Capitalize (L)"]):
            newString.append(word.lower())
            if word != word.lower():
                # recreate correct spelling
                if subject == "artist":
                    artist = artist.replace(word, word.lower())
                    list[index] = artist
                elif subject == "title":
                    title = title.replace(word, word.lower())
                    list[index] = title
                audio, filename = rename(directory, filename, artist, title, ".flac", namingConvention)
        else:
            if word[:1].islower():newString.append(word.capitalize())
            else: newString.append(word)
            list[index] = word
    if subject == "artist": return newString, list, artist, filename
    elif subject == "title": return newString, list, title, filename

def saveThumbnail(image, thumbnails):
    if image != "NA":
        image = image.resize((200, 200), Image.ANTIALIAS)
        width, height = image.size
        thumbnails.append([image, width, height])
    else:
        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Images/Thumbnail.png")
        fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
        thumbnails.append([fileImageImport, "NA", "NA"])
    return thumbnails

def rename(directory, filename, artist, title, extension, namingConvention):
    if namingConvention == "Artist - Title":
        try:
            os.rename(directory + '/' + filename, str(directory) + '/' + str(artist) + ' - ' + str(title) + extension)
            filename = str(artist) + ' - ' + str(title) + extension
        except PermissionError:
            messagebox.showinfo("Permission Error", "File cannot be renamed, it may still be open")
            return False, False
    elif namingConvention == "Title":
        try:
            os.rename(directory + '/' + filename, str(directory) + '/' + str(title) + extension)
            filename = str(title) + extension
        except PermissionError:
            messagebox.showinfo("Permission Error", "File cannot be renamed, it may still be open")
            return False, False
    if extension == ".wav":
        audio = WAVE(str(directory) + '/' + filename)
        audio["TPE1"] = TPE1(encoding=3, text=artist)
        audio["TIT2"] = TIT2(encoding=3, text=title)
        audio.save()
        return audio, filename
    elif extension == ".flac":
        audio = FLAC(str(directory) + '/' + filename)
        audio['artist'] = artist
        audio['title'] = title
        audio.save()
        return audio, filename
    elif extension == ".aiff":
        audio = AIFF(str(directory) + '/' + filename)
        audio["TPE1"] = TPE1(encoding=3, text=artist)
        audio["TIT2"] = TIT2(encoding=3, text=title)
        audio.save()
        return audio, filename
    elif extension == ".m4a":
        audio = MP4(str(directory) + '/' + filename)
        audio["\xa9ART"] = artist
        audio["\xa9nam"] = title
        audio.save()
        return audio, filename
    elif extension == ".mp3":
        audio = MP3(str(directory) + '/' + filename)
        audio["TPE1"] = TPE1(encoding=3, text=artist)
        audio["TIT2"] = TIT2(encoding=3, text=title)
        audio.save()
        return audio, filename
    elif extension == ".ogg":
        audio = OggVorbis(str(directory) + '/' + filename)
        audio['artist'] = artist
        audio['title'] = title
        audio.save()
        return audio, filename
