import tkinter as tk
from tkinter.tix import *
from mutagen.flac import Picture
from PIL import Image, ImageTk
from io import BytesIO
import getpass
import base64
import math

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

#global variables
page = 0

def Vorbis_conflict(audio, track, options, initialCounter, imageCounter, informalTagDict, webScrapingWindow):
    global page
    if audio['date'][0] != '' or audio['bpm'][0] != '' or audio['initialkey'][0] != '' or audio['genre'][0] != '':
        #tag conflict
        if str(audio['date'][0]) != str(track.release_date) or str(audio['bpm'][0]) != str(track.bpm) or str(audio['initialkey'][0]) != track.key or str(audio['genre'][0]) != track.genre:
            conflictPopup = tk.Toplevel()
            conflictPopup.title("Conflicting Tags")
            ws = conflictPopup.winfo_screenwidth()  # width of the screen
            hs = conflictPopup.winfo_screenheight()  # height of the screen
            x = (ws / 2) - (650 / 2)
            y = (hs / 2) - (330 / 2)
            conflictPopup.geometry('%dx%d+%d+%d' % (650, 300, x, y))
            if len(str(track.artist) + " - " + str(track.title)) > 30:
                x = (ws / 2) - ((650 + (len(str(track.artist) + " - " + str(track.title)) * 1.5)) / 2)
                conflictPopup.geometry('%dx%d+%d+%d' % ((650 + (len(str(track.artist) + " - " + str(track.title)) * 1.5)), 300, x, y))
            conflictPopup.config(bg=bg)
            #tag conflict window
            tk.Label(conflictPopup, text="Conflicting tags in " + str(track.artist) + " - " + str(track.title), font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(pady=(30, 40), side="top")
            # tags
            tags = tk.Frame(conflictPopup, bg=bg)
            tags.pack()

            # print current tags
            leftTags = tk.Frame(tags, bg=bg)
            leftTags.pack(side="left", padx=(0, 50), pady=(0, 50))
            currentTagDict = {}
            scrapedTagDict = {}
            # THIS is the list of tags that the user wants to retrieve
            list = ["Release_Date", "BPM", "Key", "Genre"]
            currentTagDict[0] = tk.Label(leftTags, text="CURRENT TAGS:", font=("Proxima Nova Rg", 11), fg="white", bg=bg, justify="left", bd=-10)
            currentTagDict[0].pack(anchor="w", pady=(0, 5))
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
            scrapedTagDict[0].pack(anchor="w", pady=(0, 5))
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
            tk.Button(optionButtons, text="Overwrite", command=lambda: overwriteOption(audio, track, conflictPopup, webScrapingWindow), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            tk.Button(optionButtons, text="Merge (favor scraped data)", command=lambda: mergeScrapeOption(audio, track, conflictPopup, webScrapingWindow), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            tk.Button(optionButtons, text="Merge (favor source data)", command=lambda: mergeSourceOption(audio, track, conflictPopup, webScrapingWindow), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            tk.Button(optionButtons, text="Skip", command=lambda: skipOption(audio, track, conflictPopup, webScrapingWindow), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            conflictPopup.attributes("-topmost", 1)
            conflictPopup.attributes("-topmost", 0)
            conflictPopup.wait_window()

        # image conflict
        if options["Reverse Image Search (B)"].get() == True and imageCounter >= 1:
            buttons = []
            conflictFrame = tk.Toplevel()
            conflictFrame.title("Conflicting Images")
            ws = conflictFrame.winfo_screenwidth()  # width of the screen
            hs = conflictFrame.winfo_screenheight()  # height of the screen
            y = (hs / 2) - (770 / 2)
            x = (ws / 2) - ((350 + (200 * min((imageCounter - initialCounter), 4))) / 2)
            conflictFrame.geometry('%dx%d+%d+%d' % (350 + (200 * min((imageCounter - initialCounter), 4)), 700, x, y))
            conflictFrame.config(bg=bg)
            # print current thumbnail
            Label(conflictFrame, text="Current artwork", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(pady=(20, 10))
            imageFrame = audio["metadata_block_picture"]
            thumbnailFrame = tk.Frame(conflictFrame, bg=bg)
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
                thumbnailImage = tk.Label(conflictFrame, image=photo)
                thumbnailImage.image = photo
                thumbnailButton = tk.Button(thumbnailFrame, image=photo, bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, conflictFrame))
                thumbnailButton.pack(side="top")
                buttons.append(thumbnailButton)
                tk.Label(conflictFrame, text=str(width) + "x" + str(height), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="top", pady=(5, 10))
                thumbnail = [thumbnailImageImport, width, height]
            else:
                thumbnail = "NA"
                fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Images/Thumbnail.png")
                fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(fileImageImport)
                fileImage = tk.Label(thumbnailFrame, image=photo, bg=bg)
                fileImage.image = photo
                thumbnailButton = tk.Button(thumbnailFrame, image=photo, font=("Proxima Nova Rg", 11), bg="yellow", highlightcolor='yellow', highlightthickness=3,  command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, conflictFrame))
                thumbnailButton.pack(side="top", pady=(5, 10))
                buttons.append(thumbnailButton)

            tk.Label(conflictFrame, text="Scraped artwork", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="top", pady=(15, 10))
            imageFrame = tk.Frame(conflictFrame, bg=bg)
            imageFrame.pack(side="top")
            imageButtons = []
            imageResolutions = []

            # print images as buttons
            start = initialCounter
            end = imageCounter
            for i in range(min(end - start, 2)):
                fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(start) + ".jpg")
                fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(fileImageImport)
                fileImage = tk.Label(imageFrame, image=photo)
                fileImage.image = photo
                imageButtons.append(tk.Button(imageFrame, image=photo, highlightthickness=3, command=lambda i=i: selectImage(i, track, imageButtons[i], buttons, conflictFrame)))
                imageButtons[len(imageButtons)-1].pack(side="left", padx=(20, 20))
                buttons.append(imageButtons[len(imageButtons)-1])
                im = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg")
                width, height = im.size
                imageResolutions.append(str(height) + "x" + str(width))

            resolutionsFrame = tk.Frame(conflictFrame, bg=bg)
            resolutionsFrame.pack(side="top")
            # print resolutions underneath respective images
            for i in imageResolutions: tk.Label(resolutionsFrame, text=i, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left", padx=(90, 90), pady=(5, 5))
            # page indicator
            pageFrame = tk.Frame(conflictFrame, bg=bg)
            pageFrame.pack()
            #left navigation button
            leftButton = tk.Button(pageFrame, text=" < ", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, anchor="w", state=DISABLED, command=lambda: navigateLeft(start, end, imageFrame, resolutionsFrame, pageFrame, conflictFrame, thumbnailFrame, track, thumbnail))
            leftButton.pack(side="left", padx=(0, 15), pady=(15, 10))
            tk.Label(pageFrame, text=str(page+1) + "/" + str(math.ceil(float(imageCounter - initialCounter) / 2.0)), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left", pady=(15, 10))
            tk.Button(conflictFrame, text="Select", font=("Proxima Nova Rg", 11), fg="white", bg=bg, command=lambda: saveImage(track, audio, conflictFrame, webScrapingWindow)).pack(side="top", pady=(10, 10))
            # right navigation button
            rightButton = tk.Button(pageFrame, text=" > ", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, anchor="e", command=lambda: navigateRight(start, end, imageFrame, resolutionsFrame, pageFrame, conflictFrame, thumbnailFrame, track, thumbnail))
            if math.ceil(float(imageCounter - initialCounter) / 2.0) == 1: rightButton.config(state=DISABLED)
            rightButton.pack(side="right", padx=(15, 0), pady=(15, 10))
            conflictFrame.attributes("-topmost", 1)
            conflictFrame.attributes("-topmost", 0)
            conflictFrame.wait_window()
    else:
        audio['date'] = str(track.release_date)
        audio['bpm'] = str(track.bpm)
        audio['initialkey'] = track.key
        audio['genre'] = track.genre
        audio.save()

#four button options
def overwriteOption(audio, track, window, webScrapingWindow):
    audio['date'] = str(track.release_date)
    audio['bpm'] = str(track.bpm)
    audio['initialkey'] = track.key
    audio['genre'] = track.genre
    audio.save()
    if track.imageSelection!="THUMB": saveImage(track, audio, window, webScrapingWindow)
    else: window.destroy()

def mergeScrapeOption(audio, track, window, webScrapingWindow):
    if str(track.release_date) != '':
        audio['date'] = str(track.release_date)
    if str(track.bpm) != '':
        audio['bpm'] = str(track.bpm)
    if track.key != '':
        audio['initialkey'] = track.key
    if track.genre != '':
        audio['genre'] = track.genre
    audio.save()
    if track.imageSelection!="THUMB": saveImage(track, audio, window, webScrapingWindow)
    else: window.destroy()

def mergeSourceOption(audio, track, window, webScrapingWindow):
    if audio['date'] == ['']: audio['date'] = str(track.release_date)
    else: track.release_date = str(audio['date'][0])
    if audio['bpm'] == ['']: audio['bpm'] = str(track.bpm)
    else: track.bpm = str(audio['BPM'][0])
    if audio['initialkey'] == ['']: audio['initialkey'] = track.key
    else: track.key = str(audio['initialkey'][0])
    if audio['genre'] == ['']: audio['genre'] = track.genre
    else: track.genre = str(audio['genre'][0])
    audio.save()
    if track.imageSelection!="THUMB": saveImage(track, audio, window, webScrapingWindow)
    else: window.destroy()

def skipOption(audio, track, window, webScrapingWindow):
    track.release_date = str(audio['date'][0])
    track.bpm = str(audio['BPM'][0])
    track.key = str(audio['initialkey'][0])
    track.genre = str(audio['genre'][0])
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
        audio['metadata_block_picture'] = ''
        with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(track.imageSelection) + ".jpg", 'rb') as f:
            image.data = f.read()
        image.type = 17
        image.mime = u"image/jpeg"
        image = image.write()
        value = base64.b64encode(image)
        value = value.decode("ascii")
        audio['metadata_block_picture'] = [value]
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
        tk.Label(conflictFrame, text=str(thumbnail[1]) + "x" + str(thumbnail[2]), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="top", pady=(5, 10))
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
    imageButtons = []
    imageResolutions = []
    for i in range(min(end - (start + (page * 2)), 2)):
        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i + (page * 2)) + ".jpg")
        fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(fileImageImport)
        fileImage = tk.Label(imageFrame, image=photo)
        fileImage.image = photo
        imageButtons.append(tk.Button(imageFrame, image=photo, highlightthickness=3, command=lambda i=i + (page * 2), j=i: selectImage(i, track, imageButtons[j], buttons, conflictFrame)))
        imageButtons[len(imageButtons) - 1].pack(side="left", padx=(20, 20))
        buttons.append(imageButtons[len(imageButtons) - 1])
        im = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i + (page * 2)) + ".jpg")
        width, height = im.size
        imageResolutions.append(str(height) + "x" + str(width))
    # print resolutions underneath respective images
    for i in imageResolutions:
        tk.Label(resolutionsFrame, text=i, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left", padx=(90, 90), pady=(5, 5))

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
