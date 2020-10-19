import tkinter as tk
from tkinter.tix import *
from mutagen.flac import Picture
from PIL import Image, ImageTk
from io import BytesIO
import getpass
import base64
import math

#import methods
from track_scraping.conflictPopup.commonOperations import navigateLeft
from track_scraping.conflictPopup.commonOperations import navigateRight
from track_scraping.conflictPopup.commonOperations import loadImageButtons
from track_scraping.conflictPopup.commonOperations import selectImage

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

#global variables
page = 0

def Vorbis_conflict(audio, track, options, initialCounter, imageCounter, images, informalTagDict):
    global page
    page = 0
    tagAlert = False
    if "Release_Date" in options["Selected Tags (L)"] and audio['date'][0] != '': tagAlert = True
    if "BPM" in options["Selected Tags (L)"] and audio['bpm'][0] != '': tagAlert = True
    if "Key" in options["Selected Tags (L)"] and audio['initialkey'][0] != '': tagAlert = True
    if "Genre" in options["Selected Tags (L)"] and audio['genre'][0] != '': tagAlert = True
    if tagAlert:
        # tag conflict
        tagConflict = False
        if "Release_Date" in options["Selected Tags (L)"] and str(audio['date'][0]) != str(track.release_date): tagConflict = True
        if "BPM" in options["Selected Tags (L)"] and str(audio['bpm'][0]) != str(track.bpm): tagConflict = True
        if "Key" in options["Selected Tags (L)"] and str(audio['initialkey'][0]) != track.key: tagConflictt = True
        if "Genre" in options["Selected Tags (L)"] and str(audio['genre'][0]) != track.genre: tagConflict = True
        if tagConflict:
            conflictPopup = tk.Toplevel()
            conflictPopup.title("Conflicting Tags")
            ws = conflictPopup.winfo_screenwidth()  # width of the screen
            hs = conflictPopup.winfo_screenheight()  # height of the screen
            x = (ws / 2) - (650 / 2)
            y = (hs / 2) - (264 / 2)
            conflictPopup.geometry('%dx%d+%d+%d' % (650, 240, x, y))
            if len(str(track.artist) + " - " + str(track.title)) > 30:
                x = (ws / 2) - ((650 + (len(str(track.artist) + " - " + str(track.title)) * 1.5)) / 2)
                conflictPopup.geometry('%dx%d+%d+%d' % ((650 + (len(str(track.artist) + " - " + str(track.title)) * 1.5)), 240, x, y))
            conflictPopup.config(bg=bg)
            # tag conflict window
            tk.Label(conflictPopup, text="Conflicting tags in " + str(track.artist) + " - " + str(track.title), font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(pady=(30, 40), side="top")
            tags = tk.Frame(conflictPopup, bg=bg)
            tags.pack()
            # print current tags
            leftTags = tk.Frame(tags, bg=bg)
            leftTags.pack(side="left", padx=(0, 50), pady=(0, 50))
            currentTagDict = {}
            scrapedTagDict = {}
            list = []
            if "Release_Date" in options["Selected Tags (L)"]:
                list.append("Release_Date")
                conflictPopup.update_idletasks()
                y = (hs / 2) - (((conflictPopup.winfo_height() + 10) * 1.1) / 2)
                conflictPopup.geometry('%dx%d+%d+%d' % (conflictPopup.winfo_width(), conflictPopup.winfo_height() + 20, x, y))
            if "BPM" in options["Selected Tags (L)"]:
                list.append("BPM")
                conflictPopup.update_idletasks()
                y = (hs / 2) - (((conflictPopup.winfo_height() + 10) * 1.1) / 2)
                conflictPopup.geometry('%dx%d+%d+%d' % (conflictPopup.winfo_width(), conflictPopup.winfo_height() + 20, x, y))
            if "Key" in options["Selected Tags (L)"]:
                list.append("Key")
                conflictPopup.update_idletasks()
                y = (hs / 2) - (((conflictPopup.winfo_height() + 10) * 1.1) / 2)
                conflictPopup.geometry('%dx%d+%d+%d' % (conflictPopup.winfo_width(), conflictPopup.winfo_height() + 20, x, y))
            if "Genre" in options["Selected Tags (L)"]:
                list.append("Genre")
                conflictPopup.update_idletasks()
                y = (hs / 2) - (((conflictPopup.winfo_height() + 10) * 1.1) / 2)
                conflictPopup.geometry('%dx%d+%d+%d' % (conflictPopup.winfo_width(), conflictPopup.winfo_height() + 20, x, y))
            currentTagDict[0] = tk.Label(leftTags, text="CURRENT TAGS:", font=("Proxima Nova Rg", 11), fg="white", bg=bg, justify="left", bd=-10)
            currentTagDict[0].pack(anchor="w", pady=(0, 15))
            for i in range(len(list)):
                # Avoid printing the underscore
                if list[i] == "Release_Date":
                    currentTagDict[i + 1] = tk.Label(leftTags, text="Release Date: " + str(audio[informalTagDict[list[i]]][0]), font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    currentTagDict[i + 1].pack(pady=(0, 0), anchor='w')
                else:
                    currentTagDict[i + 1] = tk.Label(leftTags, text=list[i] + ": " + str(audio[informalTagDict[list[i]]][0]), font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    currentTagDict[i + 1].pack(pady=(0, 0), anchor='w')

            # print scraped tags
            rightTags = tk.Frame(tags, bg=bg)
            rightTags.pack(side="right", padx=(50, 0), pady=(0, 50))
            scrapedTagDict[0] = tk.Label(rightTags, text="SCRAPED TAGS:", font=("Proxima Nova Rg", 11), fg="white", bg=bg, justify="left", bd=-10)
            scrapedTagDict[0].pack(anchor="w", pady=(0, 15))
            for i in range(len(list)):
                # Avoid printing the underscore
                if list[i] == "Release_Date":
                    scrapedTagDict[i + 1] = tk.Label(rightTags, text="Release Date: " + str(getattr(track, list[i].lower())), font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    scrapedTagDict[i + 1].pack(pady=(0, 0), anchor='w')
                else:
                    scrapedTagDict[i + 1] = tk.Label(rightTags, text=list[i] + ": " + str(getattr(track, list[i].lower())), font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    scrapedTagDict[i + 1].pack(pady=(0, 0), anchor='w')
            # check if both tag dictionaries are of equal length
            if len(currentTagDict) == len(scrapedTagDict):
                for i in range(1, len(currentTagDict)):
                    # highlight yellow
                    if str(currentTagDict[i]["text"]) != str(scrapedTagDict[i]["text"]):
                        currentTagDict[i].config(fg="black", bg="yellow")
                        scrapedTagDict[i].config(fg="black", bg="yellow")
            # buttons
            optionButtons = tk.Frame(conflictPopup, bg=bg)
            optionButtons.pack()
            tk.Button(optionButtons, text="Overwrite", command=lambda: overwriteOption(audio, track, options, conflictPopup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            tk.Button(optionButtons, text="Merge (favor scraped data)", command=lambda: mergeScrapeOption(audio, track, options, conflictPopup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            tk.Button(optionButtons, text="Merge (favor source data)", command=lambda: mergeSourceOption(audio, track, options, conflictPopup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            tk.Button(optionButtons, text="Skip", command=lambda: skipOption(audio, track, options, conflictPopup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            conflictPopup.attributes("-topmost", True)
            conflictPopup.iconbitmap(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/favicon.ico")
            conflictPopup.wait_window()
    else:
        if "Release_Date" in options["Selected Tags (L)"]: audio['date'] = str(track.release_date)
        if "BPM" in options["Selected Tags (L)"]: audio['bpm'] = str(track.bpm)
        if "Key" in options["Selected Tags (L)"]: audio['initialkey'] = track.key
        if "Genre" in options["Selected Tags (L)"]: audio['genre'] = track.genre
        audio.save()

    # image conflict
    if imageCounter >= 1:
        buttons = []
        conflictPopup = tk.Toplevel()
        conflictPopup.title("Conflicting Images")
        ws = conflictPopup.winfo_screenwidth()  # width of the screen
        hs = conflictPopup.winfo_screenheight()  # height of the screen
        y = (hs / 2) - (803 / 2)
        x = (ws / 2) - ((350 + (200 * min((imageCounter - initialCounter), 2))) / 2)
        conflictPopup.geometry('%dx%d+%d+%d' % (350 + (200 * min((imageCounter - initialCounter), 2)), 730, x, y))
        conflictPopup.config(bg=bg)
        # print current thumbnail
        Label(conflictPopup, text="Current artwork", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(pady=(20, 10))
        imageFrame = audio["metadata_block_picture"]
        thumbnailFrame = tk.Frame(conflictPopup, bg=bg)
        thumbnailFrame.pack()
        if imageFrame[0] != '':
            data = base64.b64decode(imageFrame[0])
            image = Picture(data)
            stream = BytesIO(image.data)
            image = Image.open(stream).convert("RGBA")
            stream.close()
            width, height = image.size
            thumbnailImageImport = image.resize((200, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(thumbnailImageImport)
            thumbnailImage = tk.Label(conflictPopup, image=photo)
            thumbnailImage.image = photo
            thumbnailButton = tk.Button(thumbnailFrame, image=photo, bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, conflictPopup))
            thumbnailButton.pack(side="top")
            buttons.append(thumbnailButton)
            tk.Label(conflictPopup, text=str(width) + "x" + str(height), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="top", pady=(5, 10))
            thumbnail = [thumbnailImageImport, width, height]
        else:
            thumbnail = "NA"
            fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Images/Thumbnail.png")
            fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(fileImageImport)
            fileImage = tk.Label(thumbnailFrame, image=photo, bg=bg)
            fileImage.image = photo
            thumbnailButton = tk.Button(thumbnailFrame, image=photo, font=("Proxima Nova Rg", 11), bg="yellow", highlightcolor='yellow', highlightthickness=3,  command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, conflictPopup))
            thumbnailButton.pack(side="top", pady=(5, 10))
            buttons.append(thumbnailButton)

        tk.Label(conflictPopup, text="Scraped artwork", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="top", pady=(15, 10))
        imageFrame = tk.Frame(conflictPopup, bg=bg)
        imageFrame.pack(side="top")

        # print images as buttons
        start = initialCounter
        end = imageCounter
        resolutionsFrame = tk.Frame(conflictPopup, bg=bg)
        resolutionsFrame.pack(side="top")
        loadImageButtons(start, end, imageFrame, images, resolutionsFrame, conflictPopup, track, buttons, page)

        # page indicator
        pageFrame = tk.Frame(conflictPopup, bg=bg)
        pageFrame.pack()
        #left navigation button
        leftButton = tk.Button(pageFrame, text=" < ", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, anchor="w", state=DISABLED, command=lambda: navigateLeft(start, end, imageFrame, images, resolutionsFrame, pageFrame, conflictPopup, thumbnailFrame, track, thumbnail, page))
        leftButton.pack(side="left", padx=(0, 15), pady=(15, 10))
        tk.Label(pageFrame, text=str(page+1) + "/" + str(math.ceil(float(imageCounter - initialCounter) / 2.0)), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left", pady=(15, 10))
        tk.Button(conflictPopup, text="Select", font=("Proxima Nova Rg", 11), fg="white", bg=bg, command=lambda: saveImage(track, audio, conflictPopup)).pack(side="top", pady=(25, 10))
        # right navigation button
        rightButton = tk.Button(pageFrame, text=" > ", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, anchor="e", command=lambda: navigateRight(start, end, imageFrame, images, resolutionsFrame, pageFrame, conflictPopup, thumbnailFrame, track, thumbnail, page))
        if math.ceil(float(imageCounter - initialCounter) / 2.0) == 1: rightButton.config(state=DISABLED)
        rightButton.pack(side="right", padx=(15, 0), pady=(15, 10))
        conflictPopup.attributes("-topmost", True)
        conflictPopup.iconbitmap(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/favicon.ico")
        conflictPopup.wait_window()

#four button options
def overwriteOption(audio, track, options, window):
    if "Release_Date" in options["Selected Tags (L)"]: audio['date'] = str(track.release_date)
    if "BPM" in options["Selected Tags (L)"]: audio['bpm'] = str(track.bpm)
    if "Key" in options["Selected Tags (L)"]: audio['initialkey'] = track.key
    if "Genre" in options["Selected Tags (L)"]: audio['genre'] = track.genre
    audio.save()
    window.destroy()

def mergeScrapeOption(audio, track, options, window):
    if "Release_Date" in options["Selected Tags (L)"] and str(track.release_date) != '': audio['date'] = str(track.release_date)
    if "BPM" in options["Selected Tags (L)"] and str(track.bpm) != '': audio['bpm'] = str(track.bpm)
    if "Key" in options["Selected Tags (L)"] and track.key != '': audio['initialkey'] = track.key
    if "Genre" in options["Selected Tags (L)"] and track.genre != '': audio['genre'] = track.genre
    audio.save()
    window.destroy()

def mergeSourceOption(audio, track, options, window):
    if "Release_Date" in options["Selected Tags (L)"]:
        if audio['date'] == ['']: audio['date'] = str(track.release_date)
        else: track.release_date = str(audio['date'][0])
    if "BPM" in options["Selected Tags (L)"]:
        if audio['bpm'] == ['']: audio['bpm'] = str(track.bpm)
        else: track.bpm = str(audio['BPM'][0])
    if "Key" in options["Selected Tags (L)"]:
        if audio['initialkey'] == ['']: audio['initialkey'] = track.key
        else: track.key = str(audio['initialkey'][0])
    if "Genre" in options["Selected Tags (L)"]:
        if audio['genre'] == ['']: audio['genre'] = track.genre
        else: track.genre = str(audio['genre'][0])
    audio.save()
    window.destroy()

def skipOption(audio, track, options, window):
    if "Release_Date" in options["Selected Tags (L)"]: track.release_date = str(audio['date'][0])
    if "BPM" in options["Selected Tags (L)"]: track.bpm = str(audio['BPM'][0])
    if "Key" in options["Selected Tags (L)"]: track.key = str(audio['initialkey'][0])
    if "Genre" in options["Selected Tags (L)"]: track.genre = str(audio['genre'][0])
    window.destroy()

#saving image to file
def saveImage(track, audio, window):
    # store image data, width, and height from downloaded image into imageSelection field
    if track.imageSelection != "THUMB":
        image = Picture()
        # first clear all images from audio file
        audio['metadata_block_picture'] = ''
        # file image import will be used as a thumbnail in various windows
        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(track.imageSelection) + ".jpg")
        width, height = fileImageImport.size
        with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(track.imageSelection) + ".jpg", 'rb') as f: image.data = f.read()
        image.type = 17
        image.mime = u"image/jpeg"
        image = image.write()
        value = base64.b64encode(image)
        value = value.decode("ascii")
        audio['metadata_block_picture'] = [value]
        audio.save()
        track.imageSelection = [fileImageImport, width, height]
    # check if current track has artwork image
    else:
        if audio["metadata_block_picture"][0] != '':
            data = base64.b64decode(audio["metadata_block_picture"][0])
            image = Picture(data)
            stream = BytesIO(image.data)
            image = Image.open(stream).convert("RGBA")
            stream.close()
            width, height = image.size
            image = image.resize((200, 200), Image.ANTIALIAS)
            track.imageSelection = [image, width, height]
        else:
            image = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Images/Thumbnail.png")
            track.imageSelection = [image, "NA", "NA"]
    window.destroy()
