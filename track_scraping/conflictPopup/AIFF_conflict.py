import tkinter as tk
from mutagen.id3._frames import *
from mutagen import id3
from PIL import Image, ImageTk
from io import BytesIO
import getpass

def AIFF_conflict(audio, track, options, initialCounter, imageCounter, webScrapingWindow):
    if audio["TDRC"] != '' or audio["TBPM"] != '' or audio["TKEY"] != '' or audio["TCON"] != '':
        buttons = []
        #tag conflict
        if str(audio["TDRC"]) != str(track.year) or str(audio["TBPM"]) != str(track.bpm) or str(audio["TKEY"]) != track.key or str(audio["TCON"]) != track.genre:
            conflictPopup = tk.Toplevel()
            conflictPopup.attributes("-topmost", True)
            conflictPopup.title("Conflicting Tags")
            canvas = tk.Canvas(conflictPopup)
            window = tk.Frame(canvas)
            scrollbar = tk.Scrollbar(conflictPopup, orient="vertical", command=canvas.yview)
            canvas.create_window(0, 0, window=window)
            ws = conflictPopup.winfo_screenwidth()  # width of the screen
            hs = conflictPopup.winfo_screenheight()  # height of the screen
            x = (ws / 2) - (550 / 2)
            y = (hs / 2) - (242 / 2)
            conflictPopup.geometry('%dx%d+%d+%d' % (550, 220, x, y))
            if len(str(track.artist) + " - " + str(track.title)) > 30:
                x = (ws / 2) - ((550 + (len(str(track.artist) + " - " + str(track.title)) * 1.5)) / 2)
                conflictPopup.geometry('%dx%d+%d+%d' % (550 + (len(str(track.artist) + " - " + str(track.title)) * 1.5), 220, x, y))
            # tags and images
            if options["Reverse Image Search (B)"].get() == True and (imageCounter - initialCounter) >= 1:
                y = (hs / 2) - (880 / 2)
                x = (ws / 2) - ((400 + (200 * (min(imageCounter - initialCounter, 4)))) / 2)
                conflictPopup.geometry('%dx%d+%d+%d' % (400 + (200 * (min(imageCounter - initialCounter, 4))), 800, x, y))
                tk.Label(window, text="Conflicting tags in " + str(track.artist) + " - " + str(track.title), font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(20, 5))
                tags = tk.Frame(window)
                tags.pack(side="top")
                # tags
                tk.Label(tags,text="CURRENT TAGS:\nYear: " + str(audio["TDRC"]) + "\nBPM: " + str(audio["TBPM"]) + "\nKey: " + str(audio["TKEY"]) + "\nGenre: " + str(audio["TCON"]), justify="left").pack(side="left", padx=(0, 40), pady=(10, 10))
                tk.Label(tags, text="NEW TAGS:\nYear: " + str(track.year) + "\nBPM: " + str(track.bpm) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre), justify="left").pack(side="right",  padx=(40, 0), pady=(10, 10))

                # load current thumbnail
                thumbnail = tk.Frame(window)
                thumbnail.pack(side="top")
                tk.Label(thumbnail, text="Current artwork", font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(20, 10))
                image = audio["APIC:"]
                if image != '':
                    stream = BytesIO(image.data)
                    image = Image.open(stream).convert("RGBA")
                    stream.close()
                    width, height = image.size
                    thumbnailImageImport = image.resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(thumbnailImageImport)
                    thumbnailImage = tk.Label(thumbnail, image=photo)
                    thumbnailImage.image = photo
                    thumbnailButton = tk.Button(thumbnail, image=photo, bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, window))
                    thumbnailButton.pack(side="top")
                    buttons.append(thumbnailButton)
                    tk.Label(thumbnail, text=str(width) + "x" + str(height)).pack(side="top", pady=(5, 10))
                else:
                    thumbnailButton = tk.Button(window, text="No Artwork Found", bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, thumbnail), height=12, width=28)
                    thumbnailButton.pack(side="top", pady=(5, 10))
                    buttons.append(thumbnailButton)
                # print images as buttons
                images = tk.Frame(window)
                images.pack(side="top")
                imageButtons = {}
                imageResolutions = []
                tk.Label(images, text="Artwork from search", font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(10, 5))
                for i in range(initialCounter, imageCounter):
                    imageRow = tk.Frame(images)
                    imageRow.pack(side="top")
                    start = initialCounter
                    end = min(initialCounter + 4, imageCounter)
                    for j in range(start, end):
                        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(j) + ".jpg")
                        fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(fileImageImport)
                        fileImage = tk.Label(imageRow, image=photo)
                        fileImage.image = photo
                        imageButtons[j] = tk.Button(imageRow, image=photo, highlightthickness=3, command=lambda j=j: selectImage(j, track, imageButtons[j], buttons, images))
                        imageButtons[j].pack(side="left", padx=(10, 10))
                        buttons.append(imageButtons[j])
                        im = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(j) + ".jpg")
                        width, height = im.size
                        imageResolutions.append(str(height) + "x" + str(width))
                        initialCounter += 1
                    resolutionRow = tk.Frame(images)
                    resolutionRow.pack(side="top")
                    # print resolutions underneath respective images
                    for j in range(start, end):
                        tk.Label(resolutionRow, text=imageResolutions[j]).pack(side="left", padx=(90, 90), pady=(5, 10))
                # load option buttons
                optionButtons = tk.Frame(window)
                optionButtons.pack(side="top")
                tk.Button(optionButtons, text="Overwrite", command=lambda: overwriteOption(audio, track, conflictPopup, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25, 10))
                tk.Button(optionButtons, text="Merge (favor scraped data)",command=lambda: mergeScrapeOption(audio, track, conflictPopup, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25, 10))
                tk.Button(optionButtons, text="Merge (favor source data)", command=lambda: mergeSourceOption(audio, track, conflictPopup, webScrapingWindow)).pack(side="left", padx=(15, 15),pady=(25, 10))
                tk.Button(optionButtons, text="Skip", command=lambda: skipOption(audio, track, conflictPopup, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25, 10))
                canvas.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrollbar.set)
                canvas.pack(fill='both', expand=True, side='left')
                scrollbar.pack(side="right", fill="y")
                conflictPopup.lift()
                conflictPopup.wait_window()
            # tags only
            else:
                tk.Label(window, text="Conflicting tags in " + str(track.artist) + " - " + str(track.title), font=("TkDefaultFont", 9, 'bold')).grid(row=0, column=0, columnspan=4, pady=(10, 0))
                tk.Label(window, text="CURRENT TAGS:\nYear: " + str(audio["TDRC"]) + "\nBPM: " + str(audio["TBPM"]) + "\nKey: " + str(audio["TKEY"]) + "\nGenre: " + str(audio["TCON"]), justify="left").grid(row=1,column=1,pady=(10, 35))
                tk.Label(window, text="NEW TAGS: \nYear: " + str(track.year) + "\nBPM: " + str(track.bpm) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre)).grid(row=1, column=2, pady=(10, 35))
                tk.Button(window, text="Overwrite", command=lambda: overwriteOption(audio, track, window, webScrapingWindow, )).grid(row=2, column=0)
                tk.Button(window, text="Merge (favor scraped data)", command=lambda: mergeScrapeOption(audio, track, window, webScrapingWindow)).grid(row=2, column=1)
                tk.Button(window, text="Merge (favor source data)", command=lambda: mergeSourceOption(track, audio, window, webScrapingWindow)).grid(row=2, column=2)
                tk.Button(window, text="Skip", command=lambda: skipOption(track, audio, window, webScrapingWindow)).grid(row=2, column=3)
                window.wait_window()
        # images only
        elif imageCounter >= 1:
            window = tk.Toplevel()
            window.attributes("-topmost", True)
            window.title("Multiple Images Found")
            ws = window.winfo_screenwidth()  # width of the screen
            hs = window.winfo_screenheight()  # height of the screen
            y = (hs / 2) - (715 / 2)
            x = (ws / 2) - ((250 + (200 * (imageCounter - initialCounter))) / 2)
            window.geometry('%dx%d+%d+%d' % (250 + (200 * (imageCounter - initialCounter)), 650, x, y))

            # print current thumbnail
            tk.Label(window, text="Current artwork", font=("TkDefaultFont", 9, 'bold')).pack(pady=(20, 10))
            image = audio["APIC:"]
            if image != '':
                stream = BytesIO(image.data)
                image = Image.open(stream).convert("RGBA")
                stream.close()
                width, height = image.size
                thumbnailImageImport = image.resize((200, 200), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(thumbnailImageImport)
                thumbnailImage = tk.Label(window, image=photo)
                thumbnailImage.image = photo
                thumbnailButton = tk.Button(window, image=photo, bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, window))
                thumbnailButton.pack(side="top")
                buttons.append(thumbnailButton)
                tk.Label(window, text=str(width) + "x" + str(height)).pack(side="top", pady=(5, 10))
            else:
                thumbnailButton = tk.Button(window, text="No Artwork Found", bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, window), height=12, width=28)
                thumbnailButton.pack(side="top", pady=(5, 10))
                buttons.append(thumbnailButton)

            tk.Label(window, text="Select a cover image", font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(15, 10))
            images = tk.Frame(window)
            images.pack(side="top")
            tags = tk.Frame(window)
            tags.pack(side="top")
            optionButtons = tk.Frame(window)
            imageButtons = {}
            imageResolutions = []
            # print images as buttons
            for i in range(initialCounter, imageCounter):
                window.columnconfigure(i, weight=1)
                fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg")
                fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(fileImageImport)
                fileImage = tk.Label(images, image=photo)
                fileImage.image = photo
                imageButtons[i] = tk.Button(images, image=photo, highlightthickness=3, command=lambda i=i: selectImage(i, track, imageButtons[i], buttons, window))
                imageButtons[i].pack(side="left", padx=(10, 10))
                buttons.append(imageButtons[i])
                im = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg")
                width, height = im.size
                imageResolutions.append(str(height) + "x" + str(width))
            resolutions = tk.Frame(window)
            resolutions.pack(side="top")
            # print resolutions underneath respective images
            for i in imageResolutions:
                tk.Label(resolutions, text=i).pack(side="left", padx=(90, 90), pady=(5, 5))
            optionButtons.pack(side="top")
            tk.Button(optionButtons, text="Select", command=lambda: saveImage(track, audio, window, webScrapingWindow)).pack(side="top", pady=(25, 10))
            window.lift()
            window.wait_window()
    else:
        audio["TDRC"] = TDRC(encoding=3, text=str(track.year))
        audio["TBPM"] = TBPM(encoding=3, text=str(track.bpm))
        audio["TKEY"] = TKEY(encoding=3, text=track.key)
        audio["TCON"] = TCON(encoding=3, text=track.genre)
        audio.save()

#four button options
def overwriteOption(audio, track, window, webScrapingWindow):
    audio["TDRC"] = TDRC(encoding=3, text=str(track.year))
    audio["TBPM"] = TBPM(encoding=3, text=str(track.bpm))
    audio["TKEY"] = TKEY(encoding=3, text=track.key)
    audio["TCON"] = TCON(encoding=3, text=track.genre)
    audio.save()
    if track.imageSelection!="THUMB":
        saveImage(track, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

def mergeScrapeOption(audio, track, window, webScrapingWindow):
    if str(track.year) != '': audio["TDRC"] = TDRC(encoding=3, text=str(track.year))
    if str(track.bpm) != '': audio["TBPM"] = TBPM(encoding=3, text=str(track.bpm))
    if track.key != '': audio["TKEY"] = TKEY(encoding=3, text=track.key)
    if track.genre != '': audio["TCON"] = TCON(encoding=3, text=track.genre)
    audio.save()
    if track.imageSelection!="THUMB":
        saveImage(track, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

def mergeSourceOption(audio, track, window, webScrapingWindow):
    if audio["TDRC"] == '': audio["TDRC"] = TDRC(encoding=3, text=str(track.year))
    else: track.year = str(audio["TDRC"])
    if audio["TBPM"] == '': audio["TBPM"] = TBPM(encoding=3, text=str(track.bpm))
    else: track.bpm = str(audio["TBPM"])
    if audio["TKEY"] == '': audio["TKEY"] = TKEY(encoding=3, text=track.key)
    else: track.key = str(audio["TKEY"])
    if audio["TCON"] == '': audio["TCON"] = TCON(encoding=3, text=track.genre)
    else: track.genre = str(audio["TCON"])
    audio.save()
    if track.imageSelection!="THUMB":
        saveImage(track, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

def skipOption(audio, track, window, webScrapingWindow):
    track.year = str(audio["TDRC"])
    track.bpm = str(audio["TBPM"])
    track.key = str(audio["TKEY"])
    track.genre = str(audio["TCON"])
    webScrapingWindow.lift()
    if track.imageSelection!="THUMB":
        saveImage(track, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

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
        audio.pop("APIC:")
        with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(track.imageSelection) + ".jpg", 'rb') as f:
            audio["APIC:"] = APIC(encoding=3, mime=u"image/jpeg", type=id3.PictureType.COVER_FRONT, data=f.read())
        audio.save()
    window.destroy()
    webScrapingWindow.lift()