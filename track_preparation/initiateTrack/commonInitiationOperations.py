from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.aiff import AIFF
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.id3._frames import *
import tkinter as tk
from PIL import Image
from tkinter import messagebox
import os
import getpass
import math
import re

# import methods
from commonOperations import resource_path

# main bg color
bg = "#282f3b"
# secondary color
secondary_bg = "#364153"

# global variable
change = False
capitalize = False
uncapitalize = False
word = ''

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
        width, height = image.size
        image = image.resize((200, 200), Image.ANTIALIAS)
        thumbnails.append([image, width, height])
    else:
        fileImageImport = Image.open(resource_path('Thumbnail.png'))
        fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
        thumbnails.append([fileImageImport, '', ''])
    return thumbnails

def rename(directory, filename, artist, title, extension, namingConvention):
    if namingConvention == "Artist - Title" or (namingConvention == 'Dynamic' and ' - ' in filename):
        try:
            os.rename(directory + '/' + filename, directory + '/' + str(artist) + ' - ' + str(title) + extension)
            filename = str(artist) + ' - ' + str(title) + extension
        except PermissionError:
            messagebox.showinfo("Permission Error", "File cannot be renamed, it may still be open")
            return False, False
    elif namingConvention == "Title" or (namingConvention == 'Dynamic' and ' - ' not in filename):
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

def checkTypos(audio, artist, title, directory, filename, extension, namingConvention, options):
    # scan artist for numbering prefix
    if options["Check for Numbering Prefix (B)"].get() == True:
        if '.' in artist:
            artistPrefix = artist[:artist.index('.') + 1]
            newArtist = artist[artist.index('.') + 1:].strip()
            newTitle = title
            if '.' in artistPrefix[0:5]:
                if any(char.isdigit() for char in artistPrefix[0:artistPrefix.index('.')]):
                    artist, title, options, renameFile = handleTypo(artist, newArtist, title, newTitle, "Prefix", options)
                    if renameFile==True: audio, filename = rename(directory, filename, artist, title, extension, namingConvention)

    # scan artist and title for hyphens
    if options["Check for Extraneous Hyphens (B)"].get() == True:
        if ('-' in artist or '-' in title) and (artist.count('-') > artist.count(' ') or title.count('-') > title.count(' ')):
            newArtist = artist
            newTitle = title
            if '-' in artist: newArtist = artist.replace('-', '*hyphen*')
            if '-' in title: newTitle = title.replace('-', '*hyphen*')
            artist, title, options, renameFile = handleTypo(artist, newArtist, title, newTitle, "Hyphen", options)
            if renameFile == True: audio, filename = rename(directory, filename, artist.replace('*hyphen*', ' '), title.replace('*hyphen*', ' '), extension, namingConvention)

    # scan artist and title for capitalization
    if options["Check for Capitalization (B)"].get()==True:
        if namingConvention == 'Dynamic': audio, filename = checkCapitalization(artist, title, filename, directory, audio, options, extension, 'Dynamic')
        if namingConvention == "Artist - Title": audio, filename = checkCapitalization(artist, title, filename, directory, audio, options, extension, "Artist - Title")
        elif namingConvention == "Title": audio, filename = checkCapitalization(artist, title, filename, directory, audio, options, extension, "Title")
    return audio, filename, options

# check window scaling
def handleTypo(artist, newArtist, title, newTitle, type, options):
    global change, word, capitalize, uncapitalize
    popup = tk.Toplevel()
    popup.title("Potential Typo - " + type)
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (450 / 2)
    y = (hs / 2) - (352 / 2)
    popup.geometry('%dx%d+%d+%d' % (450, 320, x, y))
    if type == "Capitalization":
        x = (ws / 2) - (550 / 2)
        popup.geometry('%dx%d+%d+%d' % (550, 320, x, y))
    popup.configure(bg=bg)
    if len(str(artist) + " - " + str(title)) > 50:
        x = (ws / 2) - ((450 + (len(str(artist) + " - " + str(title)) * 3)) / 2)
        popup.geometry('%dx%d+%d+%d' % (450 + (len(str(artist) + " - " + str(title)) * 3), 320, x, y))
        if type == "Capitalization":
            x = (ws / 2) - ((550 + (len(str(artist) + " - " + str(title)) * 1.5)) / 2)
            popup.geometry('%dx%d+%d+%d' % (550 + (len(str(artist) + " - " + str(title)) * 1.5), 320, x, y))
    tk.Label(popup, text="A potential typo/error was found. \nAccept or reject the proposed filename\n", font=("Proxima Nova Rg", 14), fg="white", bg=bg).pack(pady=(20, 10))
    # pack a label for each individual word in the current filename
    tk.Label(popup, text="Current filename", font=("Proxima Nova Rg", 12), fg="white", bg=bg).pack()
    currentFilename = str(artist).split(' ')
    currentFilename.append('-')
    currentFilename += str(title).split(' ')
    currentFilenameContainer = tk.Label(popup, justify="left",  fg="white", bg=bg)
    currentFilenameContainer.pack(pady=(0,25))
    currentFilenameDict = {}
    for i in range(len(currentFilename)):
        currentFilenameDict[i] = tk.Label(currentFilenameContainer, text=currentFilename[i], borderwidth=-2, font=("Proxima Nova Rg", 11), fg="white", bg=bg)
        currentFilenameDict[i].pack(side="left")
        if i != len(currentFilename) - 1: tk.Label(currentFilenameContainer, text='', borderwidth=-2, fg="white", bg=bg).pack(side="left")
    #pack a label for each individual word in the proposed filename
    tk.Label(popup, text="Proposed filename", font=("Proxima Nova Rg", 12), fg="white", bg=bg).pack(pady=(10, 0))
    newFilename = str(newArtist).split(' ')
    newFilename.append('-')
    newFilename += str(newTitle).split(' ')
    newFilenameContainer = tk.Label(popup, justify="left",  fg="white", bg=bg)
    newFilenameContainer.pack(pady=(0, 10))
    newFilenameDict = {}
    for i in range(len(newFilename)):
        newFilenameDict[i] = tk.Label(newFilenameContainer, text=str(newFilename[i].replace('*hyphen*', ' ')), borderwidth=-2, font=("Proxima Nova Rg", 11), fg="white", bg=bg)
        newFilenameDict[i].pack(side="left")
        if i!=len(newFilename)-1: tk.Label(newFilenameContainer, text='', borderwidth=-2, fg="white", bg=bg).pack(side="left")
        #highlight word if it does not match with the current filename; only highlight the first mismatched word
        if type == 'Hyphen':
            if len(currentFilename) == len(newFilename) and currentFilename[i] != newFilename[i]:
                currentFilenameDict[i].configure(fg="black", bg="yellow")
                newFilenameDict[i].configure(fg="black", bg="yellow")
        else:
            if len(currentFilename) == len(newFilename) and currentFilename[i] != newFilename[i] and word=='':
                word = str(newFilenameDict[i]["text"])
                currentFilenameDict[i].configure(fg="black", bg="yellow")
                newFilenameDict[i].configure(fg="black", bg="yellow")
    buttons = tk.Frame(popup, bg=bg)
    buttons.pack(side="top")
    tk.Button(buttons, text='Accept', command=lambda: setChange(popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(25, 10), padx=(10, 30), side="left")
    tk.Button(buttons, text='Reject', command=lambda: closePopup(popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(25, 10), padx=(30, 10), side="left")
    if type == "Capitalization":
        tk.Button(buttons, text="Always Accept " + "(" + word + ")", command=lambda: addCapitalizedList(word, popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(25, 10), padx=(30, 10), side="left")
        tk.Button(buttons, text="Always Reject " + "(" + word.lower() + ")", command=lambda: addUncapitalizedList(word, popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(25, 10), padx=(30, 10), side="left")
        popup.iconbitmap(resource_path('favicon.ico'))
        popup.wait_window()
        if capitalize: options["Always Capitalize (L)"].append(word.capitalize())
        elif uncapitalize: options["Never Capitalize (L)"].append(word.lower())
        capitalize = False
        uncapitalize = False
        word = ''
    else:
        popup.iconbitmap(resource_path('favicon.ico'))
        popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())
        popup.wait_window()
    if change:
        artist = newArtist
        title = newTitle
        return artist, title, options, True
    return artist, title, options, False

def handleDiscrepancy(original, new, index, type, options):
    global change, word, capitalize, uncapitalize
    word = ''
    popup = tk.Toplevel()
    popup.title("Potential Typo - " + type)
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (550 / 2)
    y = (hs / 2) - (330 / 2)
    popup.geometry('%dx%d+%d+%d' % (550, 300, x, y))
    if type == "Capitalization":
        x = (ws / 2) - (550 / 2)
        popup.geometry('%dx%d+%d+%d' % (650, 300, x, y))
    popup.configure(bg=bg)
    originalName = ' '.join(original)
    newName = ' '.join(new)
    if max(len(originalName), len(newName)) > 50 or len(new[index]) > 15:
        if max(len(originalName), len(newName)) > 50 and len(new[index]) > 15:
            value = max(((550 + (max(len(originalName), len(newName)) * 1.5))), ((550 + (len(new[index]) * 6))))
            x = (ws / 2) - (value / 2)
            popup.geometry('%dx%d+%d+%d' % (value, 300, x, y))
            if type == "Capitalization":
                value = max(((650 + (max(len(originalName), len(newName)) * 1.5))), ((650 + (len(new[index]) * 6))))
                x = (ws / 2) - (value / 2)
                popup.geometry('%dx%d+%d+%d' % (value, 300, x, y))
        elif max(len(originalName), len(newName)) > 50:
            x = (ws / 2) - ((550 + (max(len(originalName), len(newName)) * 1.5)) / 2)
            popup.geometry('%dx%d+%d+%d' % (550 + (max(len(originalName), len(newName)) * 1.5), 300, x, y))
            if type == "Capitalization":
                x = (ws / 2) - ((650 + (max(len(originalName), len(newName)) * 1.5)) / 2)
                popup.geometry('%dx%d+%d+%d' % (650 + (max(len(originalName), len(newName)) * 1.5), 300, x, y))
        else:
            x = (ws / 2) - ((550 + (len(new[index]) * 6)) / 2)
            popup.geometry('%dx%d+%d+%d' % (550 + (len(new[index]) * 6), 300, x, y))
            if type == "Capitalization":
                x = (ws / 2) - ((650 + (len(new[index]) * 6)) / 2)
                popup.geometry('%dx%d+%d+%d' % (650 + (len(new[index]) * 6), 300, x, y))
    tk.Label(popup, text="A potential typo/error was found. \nAccept or reject the proposed filename\n", font=("Proxima Nova Rg", 14), fg="white", bg=bg).pack(pady=(20, 10))
    # pack a label for each individual word in the current filename
    tk.Label(popup, text="Current filename", font=("Proxima Nova Rg", 12), fg="white", bg=bg).pack()
    currentFilenameContainer = tk.Label(popup, text=originalName, justify="left",  font=("Proxima Nova Rg", 11), fg="white", bg=bg)
    currentFilenameContainer.pack(pady=(0,25))

    beforeHighlight = ''
    for i in range(0, index): beforeHighlight += original[i] + ' '
    beforeHighlight.strip()
    highlight, word = new[index], new[index]
    afterHighlight = ''
    for i in range(index + 1, len(original)): afterHighlight += original[i] + ' '
    afterHighlight.strip()

    # pack a label for each individual word in the proposed filename
    newFilenameContainer = tk.Label(popup, justify="left",  fg="white", bg=bg)
    newFilenameContainer.pack(pady=(0, 10))
    tk.Label(newFilenameContainer, text=beforeHighlight, borderwidth=-2, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    tk.Label(newFilenameContainer, text=highlight, borderwidth=-2, font=("Proxima Nova Rg", 11),fg="black", bg="yellow").pack(side="left")
    tk.Label(newFilenameContainer, text=afterHighlight, borderwidth=-2, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    buttons = tk.Frame(popup, bg=bg)
    buttons.pack(side="top")
    tk.Button(buttons, text='Accept', command=lambda: setChange(popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(35, 10), padx=(10, 30), side="left")
    tk.Button(buttons, text='Reject', command=lambda: closePopup(popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(35, 10), padx=(30, 10), side="left")
    if type == "Capitalization":
        tk.Button(buttons, text="Always Accept " + "(" + word + ")", width=15 + math.ceil(len(word)/1.5), command=lambda: addCapitalizedList(word, popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(35, 10), padx=(30, 10), side="left")
        tk.Button(buttons, text="Always Reject " + "(" + word.lower() + ")", width=15 + math.ceil(len(word)/1.5), command=lambda: addUncapitalizedList(word, popup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(pady=(35, 10), padx=(30, 10), side="left")
        popup.iconbitmap(resource_path('favicon.ico'))
        popup.wait_window()
        if capitalize: options["Always Capitalize (L)"].append(word.capitalize())
        elif uncapitalize: options["Never Capitalize (L)"].append(word.lower())
        capitalize = False
        uncapitalize = False
        word = ''
    else:
        popup.iconbitmap(resource_path('favicon.ico'))
        popup.protocol("WM_DELETE_WINDOW", lambda: popup.destroy())
        popup.wait_window()
    if change:
        originalName = ''
        for i in range(0, index+1): originalName += new[i] + ' '
        for i in range (index + 1, len(original)): originalName += original[i] + ' '
        originalName = originalName.strip()
        return originalName, options, True
    return originalName, options, False

def addCapitalizedList(keyword, popup):
    global change, capitalize, uncapitalize
    change = True
    capitalize = True
    uncapitalize = False
    CONFIG_FILE = r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt"
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    term = "Always Capitalize (L)"
    originalListValues = str(config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))])
    newListValues = originalListValues
    if originalListValues == '': newListValues += keyword.capitalize()
    else:newListValues  += ", " + keyword.capitalize()
    with open(CONFIG_FILE, 'wt') as file:
        file.write(config_file.replace(term + ":" + str(config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]), term + ":" + str(newListValues)))
    file.close()
    popup.destroy()

def addUncapitalizedList(keyword, popup):
    global change, capitalize, uncapitalize
    change = False
    capitalize = False
    uncapitalize = True
    CONFIG_FILE = r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt"
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    term = "Never Capitalize (L)"
    originalListValues = str(config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))])
    newListValues = originalListValues
    if originalListValues == '': newListValues += keyword.lower()
    else:newListValues += ", " + keyword.lower()
    with open(CONFIG_FILE, 'wt') as file:
        file.write(config_file.replace(term + ":" + str(config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]), term + ":" + str(newListValues)))
    file.close()
    popup.destroy()

# handle artist and title renaming for fixed naming convention
def handleStaticNamingConvention(audio, filename, artist, title, directory, namingConvention):
    extension = filename[filename.rfind('.'):]
    # rename track so that the artist is appended at the front of the title
    if ' - ' not in filename and namingConvention == 'Artist - Title': audio, filename = rename(directory, filename, artist, title, extension, "Artist - Title")
    # rename track so that the artist is removed from the title
    elif ' - ' in filename and namingConvention == 'Title': audio, filename = rename(directory, filename, artist, title, extension, "Title")
    return audio, filename

def setChange(popup):
    global change
    change = True
    popup.destroy()

def closePopup(popup):
    global change
    change = False
    popup.destroy()