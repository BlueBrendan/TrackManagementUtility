from tkinter import Toplevel, Button, Canvas, Frame, Scrollbar, Label
from mutagen.flac import Picture
from mutagen import id3
from PIL import Image, ImageTk
from io import BytesIO
import getpass

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

def M4A_conflict(audio, track, options, initialCounter, imageCounter, webScrapingWindow):
    #M4A does not allow indexing of empty list, so we declare the tags as variables
    if len(audio["\xa9day"]) > 0:release_date = audio["\xa9day"][0]
    else:release_date = ''
    if len(audio["tmpo"]) > 0: tempo = audio["tmpo"][0]
    else:tempo = ''
    if len(audio["----:com.apple.iTunes:INITIALKEY"]) > 0: key =  audio["----:com.apple.iTunes:INITIALKEY"][0].decode('utf-8')
    else:key = ''
    if len(audio["\xa9gen"]) > 0: genre = audio["\xa9gen"][0]
    else: genre = ''

    if release_date != '' or tempo != '' or key != '' or genre != '':
        buttons = []
        #tag conflict
        if str(release_date) != [str(track.release_date)] or str(tempo) != [str(track.bpm)] or str(key) != [str(track.key)] or str(genre) != [track.genre]:
            conflictPopup = Toplevel()
            conflictPopup.attributes("-topmost", True)
            conflictPopup.title("Conflicting Tags")
            canvas = Canvas(conflictPopup, highlightthickness=0)
            window = Frame(canvas)
            scrollbar = Scrollbar(conflictPopup, orient="vertical", command=canvas.yview)
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
                Label(window, text="Conflicting tags in " + str(track.artist) + " - " + str(track.title), font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="top", pady=(20, 5))
                tags = Frame(window)
                tags.pack(side="top")
                # tags
                Label(tags, text="CURRENT TAGS:\nYear: " + str(release_date) + "\nBPM: " + str(tempo) + "\nKey: " + str(key) + "\nGenre: " + str(genre), font=("Proxima Nova Rg", 13), fg="white", bg=bg, justify="left").pack(side="left", padx=(0, 40), pady=(10, 10))
                Label(tags, text="NEW TAGS:\nYear: " + str(track.release_date) + "\nBPM: " + str(track.bpm) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre), font=("Proxima Nova Rg", 13), fg="white", bg=bg, justify="left").pack(side="right",  padx=(40, 0), pady=(10, 10))

                # load current thumbnail
                thumbnail = Frame(window, bg=bg)
                thumbnail.pack(side="top")
                Label(thumbnail, text="Current artwork", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="top", pady=(20, 10))
                image = audio["covr"]
                if len(image) != 0:
                    stream = BytesIO(image[0])
                    image = Image.open(stream).convert("RGBA")
                    stream.close()
                    width, height = image.size
                    thumbnailImageImport = image.resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(thumbnailImageImport)
                    thumbnailImage = Label(thumbnail, image=photo)
                    thumbnailImage.image = photo
                    thumbnailButton = Button(thumbnail, image=photo, font=("Proxima Nova Rg", 13), bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, window))
                    thumbnailButton.pack(side="top")
                    buttons.append(thumbnailButton)
                    Label(thumbnail, text=str(width) + "x" + str(height)).pack(side="top", pady=(5, 10))
                else:
                    thumbnailButton = Button(window, text="No Artwork Found", font=("Proxima Nova Rg", 13), bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, thumbnail), height=12, width=28)
                    thumbnailButton.pack(side="top", pady=(5, 10))
                    buttons.append(thumbnailButton)
                # print images as buttons
                images = Frame(window)
                images.pack(side="top")
                imageButtons = {}
                imageResolutions = []
                Label(images, text="Artwork from search", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="top", pady=(10, 5))
                for i in range(initialCounter, imageCounter):
                    imageRow = Frame(images)
                    imageRow.pack(side="top")
                    start = initialCounter
                    end = min(initialCounter + 4, imageCounter)
                    for j in range(start, end):
                        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(j) + ".jpg")
                        fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(fileImageImport)
                        fileImage = Label(imageRow, image=photo, bg=bg)
                        fileImage.image = photo
                        imageButtons[j] = Button(imageRow, image=photo, highlightthickness=3, command=lambda j=j: selectImage(j, track, imageButtons[j], buttons, images))
                        imageButtons[j].pack(side="left", padx=(10, 10))
                        buttons.append(imageButtons[j])
                        im = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(j) + ".jpg")
                        width, height = im.size
                        imageResolutions.append(str(height) + "x" + str(width))
                        initialCounter += 1
                    resolutionRow = Frame(images)
                    resolutionRow.pack(side="top")
                    # print resolutions underneath respective images
                    for j in range(start, end):
                        Label(resolutionRow, text=imageResolutions[j]).pack(side="left", padx=(90, 90), pady=(5, 10))
                # load option buttons
                optionButtons = Frame(window)
                optionButtons.pack(side="top")
                Button(optionButtons, text="Overwrite", command=lambda: overwriteOption(audio, track, conflictPopup, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25, 10))
                Button(optionButtons, text="Merge (favor scraped data)",command=lambda: mergeScrapeOption(audio, track, conflictPopup, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25, 10))
                Button(optionButtons, text="Merge (favor source data)", command=lambda: mergeSourceOption(audio, track, conflictPopup, webScrapingWindow)).pack(side="left", padx=(15, 15),pady=(25, 10))
                Button(optionButtons, text="Skip", command=lambda: skipOption(audio, track, conflictPopup, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25, 10))
                canvas.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrollbar.set)
                canvas.pack(fill='both', expand=True, side='left')
                scrollbar.pack(side="right", fill="y")
                conflictPopup.lift()
                conflictPopup.wait_window()
            # tags only
            else:
                Label(window, text="Conflicting tags in " + str(track.artist) + " - " + str(track.title), font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(20, 5))
                tags = Frame(window)
                tags.pack(side="top")
                # tags
                Label(tags, text="CURRENT TAGS:\nYear: " + str(release_date) + "\nBPM: " + str(tempo) + "\nKey: " + str(key) + "\nGenre: " + str(genre), justify="left").pack(side="left", padx=(0, 40), pady=(10, 10))
                Label(tags, text="NEW TAGS:\nYear: " + str(track.release_date) + "\nBPM: " + str(track.bpm) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre), justify="left").pack(side="right", padx=(40, 0),pady=(10, 10))
                # buttons
                optionButtons = Frame(window)
                optionButtons.pack(side="top")
                Button(optionButtons, text="Overwrite", command=lambda: overwriteOption(audio, track, conflictPopup, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25, 10))
                Button(optionButtons, text="Merge (favor scraped data)", command=lambda: mergeScrapeOption(audio, track, conflictPopup, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25, 10))
                Button(optionButtons, text="Merge (favor source data)", command=lambda: mergeSourceOption(audio, track, conflictPopup, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25, 10))
                Button(optionButtons, text="Skip", command=lambda: skipOption(audio, track, conflictPopup, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25, 10))
                canvas.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrollbar.set)
                canvas.pack(fill='both', expand=True, side='left')
                scrollbar.pack(side="right", fill="y")
                conflictPopup.lift()
                conflictPopup.wait_window()
        # images only
        elif imageCounter >= 1:
            window = Toplevel()
            window.attributes("-topmost", True)
            window.title("Multiple Images Found")
            ws = window.winfo_screenwidth()  # width of the screen
            hs = window.winfo_screenheight()  # height of the screen
            y = (hs / 2) - (715 / 2)
            x = (ws / 2) - ((250 + (200 * (imageCounter - initialCounter))) / 2)
            window.geometry('%dx%d+%d+%d' % (250 + (200 * (imageCounter - initialCounter)), 650, x, y))

            # print current thumbnail
            Label(window, text="Current artwork", font=("TkDefaultFont", 9, 'bold')).pack(pady=(20, 10))
            image = audio["covr"]
            if len(image) != 0:
                stream = BytesIO(image[0])
                image = Image.open(stream).convert("RGBA")
                stream.close()
                width, height = image.size
                thumbnailImageImport = image.resize((200, 200), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(thumbnailImageImport)
                thumbnailImage = Label(window, image=photo)
                thumbnailImage.image = photo
                thumbnailButton = Button(window, image=photo, bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, window))
                thumbnailButton.pack(side="top")
                buttons.append(thumbnailButton)
                Label(window, text=str(width) + "x" + str(height)).pack(side="top", pady=(5, 10))
            else:
                thumbnailButton = Button(window, text="No Artwork Found", bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, window), height=12, width=28)
                thumbnailButton.pack(side="top", pady=(5, 10))
                buttons.append(thumbnailButton)

            Label(window, text="Select a cover image", font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(15, 10))
            images = Frame(window)
            images.pack(side="top")
            tags = Frame(window)
            tags.pack(side="top")
            optionButtons = Frame(window)
            imageButtons = {}
            imageResolutions = []
            # print images as buttons
            for i in range(initialCounter, imageCounter):
                window.columnconfigure(i, weight=1)
                fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg")
                fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(fileImageImport)
                fileImage = Label(images, image=photo)
                fileImage.image = photo
                imageButtons[i] = Button(images, image=photo, highlightthickness=3, command=lambda i=i: selectImage(i, track, imageButtons[i], buttons, window))
                imageButtons[i].pack(side="left", padx=(10, 10))
                buttons.append(imageButtons[i])
                im = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg")
                width, height = im.size
                imageResolutions.append(str(height) + "x" + str(width))
            resolutions = Frame(window)
            resolutions.pack(side="top")
            # print resolutions underneath respective images
            for i in imageResolutions:
                Label(resolutions, text=i).pack(side="left", padx=(90, 90), pady=(5, 5))
            optionButtons.pack(side="top")
            Button(optionButtons, text="Select", command=lambda: saveImage(track, audio, window, webScrapingWindow)).pack(side="top", pady=(25, 10))
            window.lift()
            window.wait_window()
    else:
        audio["\xa9day"] = str(track.release_date)
        audio["tmpo"] = str(track.bpm)
        audio["----:com.apple.iTunes:INITIALKEY"] = track.key.encode('utf-8')
        audio["\xa9gen"] = track.genre
        audio.save()

#four button options
def overwriteOption(audio, track, window, webScrapingWindow):
    audio["\xa9day"] = str(track.release_date)
    #m4a format requires bpm to be an int in a list
    audio["tmpo"] = [int(track.bpm)]
    audio["----:com.apple.iTunes:INITIALKEY"] = track.key.encode('utf-8')
    audio["\xa9gen"] = track.genre
    audio.save()
    if track.imageSelection!="THUMB":
        saveImage(track, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

def mergeScrapeOption(audio, track, window, webScrapingWindow):
    if str(track.release_date) != '':
        audio["\xa9day"] = str(track.release_date)
    if str(track.bpm) != '':
        audio["tmpo"] = [int(track.bpm)]
    if track.key != '':
        audio["----:com.apple.iTunes:INITIALKEY"] = track.key.encode('utf-8')
    if track.genre != '':
        audio["\xa9gen"] = track.genre
    audio.save()
    if track.imageSelection!="THUMB":
        saveImage(track, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

def mergeSourceOption(audio, track, window, webScrapingWindow):
    if audio["\xa9day"] == ['']: audio["\xa9day"] = str(track.release_date)
    else:
        if len(audio["\xa9day"]) > 0: track.release_date = str(audio["\xa9day"][0])
        else: track.release_date = ''
    if audio["tmpo"] == ['']: audio["tmpo"] = [int(track.bpm)]
    else:
        if len(audio["tmpo"]) > 0: track.bpm = str(audio["tmpo"][0])
        else: track.bpm = [int('')]
    if audio["----:com.apple.iTunes:INITIALKEY"] == ['']: audio["----:com.apple.iTunes:INITIALKEY"] = track.key.encode('utf-8')
    else:
        if len(audio["----:com.apple.iTunes:INITIALKEY"]) > 0:
            track.key = str(audio["----:com.apple.iTunes:INITIALKEY"][0].decode('utf-8'))
        else: track.key = ''
    if audio["\xa9gen"] == ['']: audio["\xa9gen"] = track.genre
    else:
        if len(str(audio["\xa9gen"])) > 0: track.genre = str(audio["\xa9gen"][0])
        else: track.genre = ''
    audio.save()
    if track.imageSelection!="THUMB":
        saveImage(track, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

def skipOption(audio, track, window, webScrapingWindow):
    if len(audio["\xa9day"]) > 0: track.release_date = str(audio["\xa9day"][0])
    else:track.release_date = ''
    if len(str(audio["tmpo"])) > 0: track.bpm = str(audio["tmpo"][0])
    else: track.bpm = ''
    if len(str(audio["----:com.apple.iTunes:INITIALKEY"])) > 0: track.key = audio["----:com.apple.iTunes:INITIALKEY"][0].decode('utf-8')
    else: track.key = ''
    if len(str(audio["\xa9gen"])) > 0: track.genre = str(audio["\xa9gen"][0])
    else: track.genre = ''
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
        audio["covr"] = ''
        with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(track.imageSelection) + ".jpg", 'rb') as f:
            image = f.read()
        audio["covr"] = [image]
        audio.save()
    window.destroy()
    webScrapingWindow.lift()