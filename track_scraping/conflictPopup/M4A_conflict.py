import tkinter as tk
from tkinter.tix import *
from PIL import Image, ImageTk
from io import BytesIO
import getpass

#import methods
from commonOperations import loadImageButtons
from commonOperations import loadNavigation
from commonOperations import selectImage
from commonOperations import resource_path

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

#global variables
page = 0

def M4A_conflict(audio, track, options, initialCounter, imageCounter, images, informalTagDict):
    global page
    page = 0
    tagAlert = False
    if "Release_Date" in options["Selected Tags (L)"] and len(audio["\xa9day"]) != 0: tagAlert = True
    if "BPM" in options["Selected Tags (L)"] and len(audio["tmpo"]) != 0: tagAlert = True
    if "Key" in options["Selected Tags (L)"] and len(audio["----:com.apple.iTunes:INITIALKEY"]) != 0: tagAlert = True
    if "Genre" in options["Selected Tags (L)"] and len(audio["\xa9gen"]) != 0: tagAlert = True
    if tagAlert:
        #tag conflict
        tagConflict = False
        if "Release_Date" in options["Selected Tags (L)"] and len(audio["\xa9day"]) != 0 and str(audio["\xa9day"][0]) != str(track.release_date): tagConflict = True
        if "BPM" in options["Selected Tags (L)"] and len(audio["tmpo"]) != 0 and str(audio["tmpo"][0]) != str(track.bpm): tagConflict = True
        # key is stored in byte form for m4A files, value cannot be casted to string directly
        if "Key" in options["Selected Tags (L)"] and len(audio["----:com.apple.iTunes:INITIALKEY"]) != 0 and str(audio["----:com.apple.iTunes:INITIALKEY"][0].decode('utf-8')) != track.key: tagConflict = True
        if "Genre" in options["Selected Tags (L)"] and len(audio["\xa9gen"]) != 0 and str(audio["\xa9gen"][0]) != track.genre: tagConflict = True
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
                # avoid printing the underscore
                if list[i] == "Release_Date":
                    if len(audio[informalTagDict[list[i]]]) > 0: currentTagDict[i + 1] = tk.Label(leftTags, text="Release Date: " + str(audio[informalTagDict[list[i]]][0]), font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    else: currentTagDict[i + 1] = tk.Label(leftTags, text="Release Date: ", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    currentTagDict[i + 1].pack(pady=(0, 0), anchor='w')
                # decode key
                elif list[i] == "Key":
                    if len(audio[informalTagDict[list[i]]]) == 0: currentTagDict[i + 1] = tk.Label(leftTags, text="Key: ", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    else: currentTagDict[i + 1] = tk.Label(leftTags, text="Key: " + str(audio[informalTagDict[list[i]]][0].decode('utf-8')), font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    currentTagDict[i + 1].pack(pady=(0, 0), anchor='w')
                else:
                    if len(audio[informalTagDict[list[i]]]) > 0: currentTagDict[i + 1] = tk.Label(leftTags, text=list[i] + ": " + str(audio[informalTagDict[list[i]]][0]), font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    else: currentTagDict[i + 1] = tk.Label(leftTags, text=list[i] + ": ", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
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
            tk.Button(optionButtons, text="Overwrite All", command=lambda: overwriteAllOption(audio, track, options, conflictPopup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            tk.Button(optionButtons, text="Overwrite Blanks", command=lambda: overwriteBlanksOption(audio, track, options, conflictPopup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            tk.Button(optionButtons, text="Skip", command=lambda: skipOption(audio, track, options, conflictPopup), font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg).pack(side="left", padx=(20, 20))
            conflictPopup.attributes("-topmost", True)
            conflictPopup.iconbitmap(resource_path('favicon.ico'))
            conflictPopup.wait_window()
    else:
        if "Release_Date" in options["Selected Tags (L)"]: audio["\xa9day"] = str(track.release_date)
        if "BPM" in options["Selected Tags (L)"]: audio["tmpo"] = str(track.bpm)
        if "Key" in options["Selected Tags (L)"]: audio["----:com.apple.iTunes:INITIALKEY"] = track.key
        if "Genre" in options["Selected Tags (L)"]: audio["\xa9gen"] = track.genre
        audio.save()

    # image conflict
    if imageCounter - initialCounter >= 1:
        buttons = []
        conflictPopup = tk.Toplevel()
        conflictPopup.title("Conflicting Images")
        ws = conflictPopup.winfo_screenwidth()  # width of the screen
        hs = conflictPopup.winfo_screenheight()  # height of the screen
        y = (hs / 2) - (803 / 2)
        x = (ws / 2) - ((350 + (200 * min((imageCounter - initialCounter), options["Number of Images Per Page (I)"].get()))) / 2)
        conflictPopup.geometry('%dx%d+%d+%d' % (350 + (200 * min((imageCounter - initialCounter), options["Number of Images Per Page (I)"].get())), 730, x, y))
        conflictPopup.config(bg=bg)
        # print current thumbnail
        tk.Label(conflictPopup, text="Current artwork", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(pady=(20, 10))
        thumbnailFrame = tk.Frame(conflictPopup, bg=bg)
        thumbnailFrame.pack()
        image = audio["covr"]
        if len(image) > 0:
            stream = BytesIO(image[0])
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
            fileImageImport = Image.open(resource_path('Thumbnail.png'))
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

        # print images as buttons
        start = initialCounter
        end = imageCounter
        resolutionsFrame = tk.Frame(conflictPopup, bg=bg)
        resolutionsFrame.pack(side="top")
        loadImageButtons(start, end, imageFrame, images, resolutionsFrame, conflictPopup, track, buttons, page, options)

        # page indicator
        pageFrame = tk.Frame(conflictPopup, bg=bg)
        pageFrame.pack()
        # load navigational buttons and page number
        loadNavigation(start, end, pageFrame, imageFrame, images, resolutionsFrame, conflictPopup, thumbnailFrame, track, thumbnail, page, "load", options)
        # select button
        tk.Button(conflictPopup, text="Select", font=("Proxima Nova Rg", 11), fg="white", bg=bg, command=lambda: saveImage(track, audio, conflictPopup)).pack(side="top", pady=(25, 10))
        conflictPopup.attributes("-topmost", True)
        conflictPopup.iconbitmap(resource_path('favicon.ico'))
        conflictPopup.wait_window()

# overwrite existing tags with all non-blank scraped tag fields
def overwriteAllOption(audio, track, options, window):
    if "Release_Date" in options["Selected Tags (L)"] and str(track.release_date) != '': audio["\xa9day"] = str(track.release_date)
    if "BPM" in options["Selected Tags (L)"] and str(track.bpm) != '': audio["tmpo"] = [int(track.bpm)]
    if "Key" in options["Selected Tags (L)"] and track.key != '': audio["----:com.apple.iTunes:INITIALKEY"] = track.key.encode('utf-8')
    if "Genre" in options["Selected Tags (L)"] and track.genre != '': audio["\xa9gen"] = track.genre
    audio.save()
    window.destroy()

# overwrite existing blank tags with all scraped tag fields
def overwriteBlanksOption(audio, track, options, window):
    if "Release_Date" in options["Selected Tags (L)"]:
        if audio["\xa9day"] == ['']: audio["\xa9day"] = str(track.release_date)
        else:
            if len(audio["\xa9day"]) > 0: track.release_date = str(audio["\xa9day"][0])
            else: track.release_date = ''
    if "BPM" in options["Selected Tags (L)"]:
        if len(audio["tmpo"]) == 0: audio["tmpo"] = [int(track.bpm)]
        else:
            if len(audio["tmpo"]) > 0: track.bpm = str(audio["tmpo"][0])
            else: track.bpm = ['']
    if "Key" in options["Selected Tags (L)"]:
        if audio["----:com.apple.iTunes:INITIALKEY"] == ['']: audio["----:com.apple.iTunes:INITIALKEY"] = track.key.encode('utf-8')
        else:
            if len(audio["----:com.apple.iTunes:INITIALKEY"]) > 0: track.key = str(audio["----:com.apple.iTunes:INITIALKEY"][0].decode('utf-8'))
            else: track.key = ''
    if "Genre" in options["Selected Tags (L)"]:
        if audio["\xa9gen"] == ['']: audio["\xa9gen"] = track.genre
        else:
            if len(audio["\xa9gen"]) > 0: track.genre = str(audio["\xa9gen"][0])
            else: track.genre = ''
    audio.save()
    window.destroy()

# ignore scraped tags entirely, leave current tags untouched
def skipOption(audio, track, options, window):
    if "Release_Date" in options["Selected Tags (L)"]:
        if len(audio["\xa9day"]) > 0: track.release_date = str(audio["\xa9day"][0])
        else:  track.release_date = ''
    if "BPM" in options["Selected Tags (L)"]:
        if len(audio["tmpo"]) > 0: track.bpm = str(audio["tmpo"][0])
        else: track.bpm = ''
    if "Key" in options["Selected Tags (L)"]:
        if len(audio["----:com.apple.iTunes:INITIALKEY"]) > 0: track.key = audio["----:com.apple.iTunes:INITIALKEY"][0].decode('utf-8')
        else: track.key = ''
    if "Genre" in options["Selected Tags (L)"]:
        if len(audio["\xa9gen"]) > 0: track.genre = str(audio["\xa9gen"][0])
        else: track.genre = ''
    window.destroy()

#saving image to file
def saveImage(track, audio, window):
    # store image data, width, and height from downloaded image into imageSelection field
    if track.imageSelection != "THUMB":
        # first clear all images from audio file
        audio["covr"] = ''
        # file image import will be used as a thumbnail in various windows
        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(track.imageSelection) + ".jpg")
        width, height = fileImageImport.size
        fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
        with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(track.imageSelection) + ".jpg", 'rb') as f: audio["covr"] = [f.read()]
        audio.save()
        track.imageSelection = [fileImageImport, width, height]
    # check if current track has artwork image
    else:
        if len(audio["covr"])!=0:
            stream = BytesIO(audio["covr"][0])
            image = Image.open(stream).convert("RGBA")
            stream.close()
            width, height = image.size
            image = image.resize((200, 200), Image.ANTIALIAS)
            track.imageSelection = [image, width, height]
        else:
            image = Image.open(resource_path('Thumbnail.png'))
            track.imageSelection = [image, '', '']
    window.destroy()