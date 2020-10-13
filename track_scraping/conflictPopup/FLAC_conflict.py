import tkinter as tk
from tkinter.tix import *
from mutagen.flac import Picture
from mutagen import id3
from PIL import Image, ImageTk
from io import BytesIO
import getpass
import math

# main bg color
bg = "#282f3b"
# secondary color
secondary_bg = "#364153"

# global variables
page = 0

def FLAC_conflict(audio, track, options, initialCounter, imageCounter, informalTagDict, webScrapingWindow):
    global page
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
            #tag conflict window
            tk.Label(conflictPopup, text="Conflicting tags in " + str(track.artist) + " - " + str(track.title), font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(pady=(30, 40), side="top")
            tags = tk.Frame(conflictPopup, bg=bg)
            tags.pack()

            #print current tags
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
                    currentTagDict[i+1] = tk.Label(leftTags, text="Release Date: " + str(audio[informalTagDict[list[i]]][0]), font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    currentTagDict[i+1].pack(pady=(0, 0), anchor='w')
                else:
                    currentTagDict[i+1] = tk.Label(leftTags, text=list[i] + ": " + str(audio[informalTagDict[list[i]]][0]), font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    currentTagDict[i+1].pack(pady=(0, 0), anchor='w')

            #print scraped tags
            rightTags = tk.Frame(tags, bg=bg)
            rightTags.pack(side="right", padx=(50, 0), pady=(0, 50))
            scrapedTagDict[0] = tk.Label(rightTags, text="SCRAPED TAGS:", font=("Proxima Nova Rg", 11), fg="white", bg=bg, justify="left", bd=-10)
            scrapedTagDict[0].pack(anchor="w", pady=(0, 15))
            for i in range(len(list)):
                #Avoid printing the underscore
                if list[i] == "Release_Date":
                    scrapedTagDict[i+1] = tk.Label(rightTags, text="Release Date: " + str(getattr(track, list[i].lower())), font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    scrapedTagDict[i+1].pack(pady=(0, 0), anchor='w')
                else:
                    scrapedTagDict[i+1] = tk.Label(rightTags, text=list[i] + ": " + str(getattr(track, list[i].lower())), font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    scrapedTagDict[i+1].pack(pady=(0, 0), anchor='w')
            #check if both tag dictionaries are of equal length
            if len(currentTagDict) == len(scrapedTagDict):
                for i in range(1, len(currentTagDict)):
                    #highlight yellow
                    if str(currentTagDict[i]["text"])!=str(scrapedTagDict[i]["text"]):
                        currentTagDict[i].config(fg="black", bg="yellow")
                        scrapedTagDict[i].config(fg="black", bg="yellow")
            # buttons
            optionButtons = tk.Frame(conflictPopup, bg=bg)
            optionButtons.pack()
            tk.Button(optionButtons, text="Overwrite", command=lambda: overwriteOption(audio, track, options, conflictPopup, webScrapingWindow), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            tk.Button(optionButtons, text="Merge (favor scraped data)", command=lambda: mergeScrapeOption(audio, track, options, conflictPopup, webScrapingWindow), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            tk.Button(optionButtons, text="Merge (favor source data)", command=lambda: mergeSourceOption(audio, track, options, conflictPopup, webScrapingWindow), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            tk.Button(optionButtons, text="Skip", command=lambda: skipOption(audio, track, options, conflictPopup, webScrapingWindow), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            conflictPopup.attributes("-topmost", True)
            conflictPopup.iconbitmap(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/favicon.ico")
            conflictPopup.wait_window()

    # image conflict
    if imageCounter >= 1:
        buttons = []
        conflictPopup = tk.Toplevel()
        conflictPopup.title("Conflicting Images")
        ws = conflictPopup.winfo_screenwidth()  # width of the screen
        hs = conflictPopup.winfo_screenheight()  # height of the screen
        y = (hs / 2) - (781 / 2)
        x = (ws / 2) - ((350 + (200 * min((imageCounter - initialCounter), 2))) / 2)
        conflictPopup.geometry('%dx%d+%d+%d' % ((350 + (200 * min((imageCounter - initialCounter), 2))), 710, x, y))
        conflictPopup.config(bg=bg)
        # print current thumbnail
        Label(conflictPopup, text="Current artwork", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(pady=(20, 10))
        thumbnailFrame = tk.Frame(conflictPopup, bg=bg)
        thumbnailFrame.pack()
        if len(audio.pictures) > 0:
            stream = BytesIO(audio.pictures[0].data)
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
            thumbnailButton = tk.Button(thumbnailFrame, image=photo, font=("Proxima Nova Rg", 11), bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, conflictPopup))
            thumbnailButton.pack(side="top", pady=(5, 10))
            buttons.append(thumbnailButton)
        tk.Label(conflictPopup, text="Scraped artwork", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="top", pady=(15, 10))
        imageFrame = tk.Frame(conflictPopup, bg=bg)
        imageFrame.pack(side="top")
        imageButtons = []
        imageResolutions = []

        # print images as buttons
        start = initialCounter
        end = imageCounter
        for i in range(start, min(start + 2, end)):
            fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg")
            width, height = fileImageImport.size
            fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(fileImageImport)
            fileImage = tk.Label(imageFrame, image=photo)
            fileImage.image = photo
            imageButtons.append(tk.Button(imageFrame, image=photo, highlightthickness=3, command=lambda i=i: selectImage(i, track, imageButtons[i-start], buttons, conflictPopup)))
            imageButtons[len(imageButtons) - 1].pack(side="left", padx=(20, 20))
            buttons.append(imageButtons[len(imageButtons) - 1])
            imageResolutions.append(str(height) + "x" + str(width))

        resolutionsFrame = tk.Frame(conflictPopup, bg=bg)
        resolutionsFrame.pack(side="top")
        # print resolutions underneath respective images
        for i in imageResolutions: tk.Label(resolutionsFrame, text=i, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left", padx=(90, 90), pady=(5, 5))
        # page indicator
        pageFrame = tk.Frame(conflictPopup, bg=bg)
        pageFrame.pack()
        #left navigation button
        leftButton = tk.Button(pageFrame, text=" < ", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, anchor="w", state=DISABLED, command=lambda: navigateLeft(start, end, imageFrame, resolutionsFrame, pageFrame, conflictPopup, thumbnailFrame, track, thumbnail))
        leftButton.pack(side="left", padx=(0, 15), pady=(15, 10))
        tk.Label(pageFrame, text=str(page+1) + "/" + str(math.ceil(float(imageCounter - initialCounter) / 2.0)), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left", pady=(15, 10))
        tk.Button(conflictPopup, text="Select", font=("Proxima Nova Rg", 11), fg="white", bg=bg, command=lambda: saveImage(track, audio, conflictPopup, webScrapingWindow)).pack(side="top", pady=(10, 10))
        # right navigation button
        rightButton = tk.Button(pageFrame, text=" > ", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, anchor="e", command=lambda: navigateRight(start, end, imageFrame, resolutionsFrame, pageFrame, conflictPopup, thumbnailFrame, track, thumbnail))
        if math.ceil(float(imageCounter - initialCounter) / 2.0) == 1: rightButton.config(state=DISABLED)
        rightButton.pack(side="right", padx=(15, 0), pady=(15, 10))
        conflictPopup.attributes("-topmost", True)
        conflictPopup.iconbitmap(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/favicon.ico")
        conflictPopup.wait_window()
    # no tags were collected, acquire tags directly from track
    else:
        if "Release_Date" in options["Selected Tags (L)"]: audio['date'] = str(track.release_date)
        if "BPM" in options["Selected Tags (L)"]: audio['bpm'] = str(track.bpm)
        if "Key" in options["Selected Tags (L)"]: audio['initialkey'] = track.key
        if "Genre" in options["Selected Tags (L)"]: audio['genre'] = track.genre
        audio.save()

#four button options
def overwriteOption(audio, track, options, window, webScrapingWindow):
    if "Release_Date" in options["Selected Tags (L)"]: audio['date'] = str(track.release_date)
    if "BPM" in options["Selected Tags (L)"]: audio['bpm'] = str(track.bpm)
    if "Key" in options["Selected Tags (L)"]: audio['initialkey'] = track.key
    if "Genre" in options["Selected Tags (L)"]: audio['genre'] = track.genre
    audio.save()
    if track.imageSelection!="THUMB": saveImage(track, audio, window, webScrapingWindow)
    else: window.destroy()

def mergeScrapeOption(audio, track, options, window, webScrapingWindow):
    if "Release_Date" in options["Selected Tags (L)"] and str(track.release_date) != '': audio['date'] = str(track.release_date)
    if "BPM" in options["Selected Tags (L)"] and str(track.bpm) != '': audio['bpm'] = str(track.bpm)
    if "Key" in options["Selected Tags (L)"] and track.key != '': audio['initialkey'] = track.key
    if "Genre" in options["Selected Tags (L)"] and track.genre != '': audio['genre'] = track.genre
    audio.save()
    if track.imageSelection!="THUMB": saveImage(track, audio, window, webScrapingWindow)
    else: window.destroy()

def mergeSourceOption(audio, track, options, window, webScrapingWindow):
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
    if track.imageSelection!="THUMB": saveImage(track, audio, window, webScrapingWindow)
    else: window.destroy()

def skipOption(audio, track, options, window, webScrapingWindow):
    if "Release_Date" in options["Selected Tags (L)"]: track.release_date = str(audio['date'][0])
    if "BPM" in options["Selected Tags (L)"]: track.bpm = str(audio['BPM'][0])
    if "Key" in options["Selected Tags (L)"]: track.key = str(audio['initialkey'][0])
    if "Genre" in options["Selected Tags (L)"]:track.genre = str(audio['genre'][0])
    if track.imageSelection!="THUMB": saveImage(track, audio, window, webScrapingWindow)
    else: window.destroy()

#selecting image to variable
def selectImage(i, track, button, buttons, window):
    track.imageSelection = i
    #unhighlight all buttons
    for item in buttons:
        item.config(bg="white", highlightcolor="white")
    #highlight selected button
    button.config(bg="yellow", highlightcolor="yellow")
    window.update()

#saving image to file
def saveImage(track, audio, window, webScrapingWindow):
    #first clear all images from audio file
    if track.imageSelection != "THUMB":
        image = Picture()
        audio.clear_pictures()
        with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(track.imageSelection) + ".jpg", 'rb') as f:
            image.data = f.read()
        image.type = id3.PictureType.COVER_FRONT
        image.mime = u"image/jpeg"
        audio.add_picture(image)
        audio.save()
    window.destroy()

def navigateLeft(start, end, imageFrame, resolutionsFrame, pageFrame, conflictFrame, thumbnailFrame, track, thumbnail):
    global page
    page-=1
    track.imageSelection = "THUMB"
    # buttons starts off as a list already containing the thumbnail button
    buttons = []
    # reload thumbnailFrame, imageFrame, resolutions Frame, and pageFrame
    reloadFrames(thumbnailFrame, imageFrame, resolutionsFrame, pageFrame)
    # reload thumbnail
    buttons = reloadThumbnail(thumbnail, track, buttons, conflictFrame, thumbnailFrame)
    # reload image buttons
    reloadButtons(start, end, imageFrame, resolutionsFrame, conflictFrame, track, buttons)
    # reload navigation buttons and page indicator
    reloadNavigation(start, end, pageFrame, imageFrame, resolutionsFrame, conflictFrame, thumbnailFrame, track, thumbnail, "left")


def navigateRight(start, end, imageFrame, resolutionsFrame, pageFrame, conflictFrame, thumbnailFrame, track, thumbnail):
    global page
    page+=1
    track.imageSelection = "THUMB"
    # buttons starts off as a list already containing the thumbnail button
    buttons = []
    # reload thumbnailFrame, imageFrame, resolutions Frame, and pageFrame
    reloadFrames(thumbnailFrame, imageFrame, resolutionsFrame, pageFrame)
    # reload thumbnail
    buttons = reloadThumbnail(thumbnail, track, buttons, conflictFrame, thumbnailFrame)
    # reload image buttons
    reloadButtons(start, end, imageFrame, resolutionsFrame, conflictFrame, track, buttons)
    # reload navigation buttons and page indicator
    reloadNavigation(start, end, pageFrame, imageFrame, resolutionsFrame, conflictFrame, thumbnailFrame, track, thumbnail, "right")

def allWidgets(window):
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())
    return _list

def reloadFrames(thumbnailFrame, imageFrame, resolutionsFrame, pageFrame):
    widgetList = allWidgets(thumbnailFrame)
    for item in widgetList: item.pack_forget()
    widgetList = allWidgets(imageFrame)
    for item in widgetList: item.pack_forget()
    widgetList = allWidgets(resolutionsFrame)
    for item in widgetList: item.pack_forget()
    widgetList = allWidgets(pageFrame)
    for item in widgetList: item.pack_forget()

def reloadThumbnail(thumbnail, track, buttons, conflictFrame, thumbnailFrame):
    if type(thumbnail) != str:
        photo = ImageTk.PhotoImage(thumbnail[0])
        thumbnailImage = tk.Label(conflictFrame, image=photo)
        thumbnailImage.image = photo
        thumbnailButton = tk.Button(thumbnailFrame, image=photo, bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, conflictFrame))
        thumbnailButton.pack(side="top")
        buttons.append(thumbnailButton)
    else:
        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Images/Thumbnail.png")
        fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(fileImageImport)
        fileImage = tk.Label(thumbnailFrame, image=photo, bg=bg)
        fileImage.image = photo
        thumbnailButton = tk.Button(thumbnailFrame, image=photo, font=("Proxima Nova Rg", 11), bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, conflictFrame))
        thumbnailButton.pack(side="top", pady=(5, 10))
        buttons.append(thumbnailButton)
    return buttons

def reloadButtons(start, end, imageFrame, resolutionsFrame, conflictFrame, track, buttons):
    global page
    imageButtons = []
    imageResolutions = []
    for i in range((start + (page * 2)), min((start + (page * 2) + 2), end)):
        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg")
        width, height = fileImageImport.size
        fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(fileImageImport)
        fileImage = tk.Label(imageFrame, image=photo)
        fileImage.image = photo
        imageButtons.append(tk.Button(imageFrame, image=photo, highlightthickness=3, command=lambda i=i: selectImage(i, track, imageButtons[i], buttons, conflictFrame)))
        imageButtons[len(imageButtons) - 1].pack(side="left", padx=(20, 20))
        buttons.append(imageButtons[len(imageButtons) - 1])
        imageResolutions.append(str(height) + "x" + str(width))
    # print resolutions underneath respective images
    for i in imageResolutions: tk.Label(resolutionsFrame, text=i, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left", padx=(90, 90), pady=(5, 5))

def reloadNavigation(start, end, pageFrame, imageFrame, resolutionsFrame, conflictFrame, thumbnailFrame, track, thumbnail, direction):
    leftButton = tk.Button(pageFrame, text=" < ", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, anchor="w", state=NORMAL, command=lambda: navigateLeft(start, end, imageFrame, resolutionsFrame, pageFrame, conflictFrame, thumbnailFrame, track, thumbnail))
    leftButton.pack(side="left", padx=(0, 15), pady=(15, 10))
    tk.Label(pageFrame, text=str(page + 1) + "/" + str(math.ceil(float(end - start) / 2.0)), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left", pady=(15, 10))
    # right button
    rightButton = tk.Button(pageFrame, text=" > ", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, anchor="e",  state=NORMAL, command=lambda: navigateRight(start, end, imageFrame, resolutionsFrame, pageFrame, conflictFrame, thumbnailFrame, track, thumbnail))
    rightButton.pack(side="left", padx=(15, 0), pady=(15, 10))
    if direction == "left":
        # deactivate left button if on first page
        if page == 0: leftButton.config(state=DISABLED)
    elif direction == "right":
        # deactivate right button if on last page
        if page+1 == math.ceil((end - start)/2.0): rightButton.config(state=DISABLED)