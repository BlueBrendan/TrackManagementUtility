from tkinter import Toplevel, Button, Canvas, Frame, Scrollbar, Label
from mutagen.flac import Picture
from mutagen import id3
from PIL import Image, ImageTk
from io import BytesIO
import getpass
import base64

def Vorbis_conflict(audio, track, options, initialCounter, imageCounter, webScrapingWindow):
    if audio['date'][0] != '' or audio['bpm'][0] != '' or audio['initialkey'][0] != '' or audio['genre'][0] != '':
        buttons = []
        #tag conflict
        if str(audio['date'][0]) != str(track.release_date) or str(audio['bpm'][0]) != str(track.bpm) or str(audio['initialkey'][0]) != track.key or str(audio['genre'][0]) != track.genre:
            conflictPopup = Toplevel()
            conflictPopup.attributes("-topmost", True)
            conflictPopup.title("Conflicting Tags")
            canvas = Canvas(conflictPopup)
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
                Label(window, text="Conflicting tags in " + str(track.artist) + " - " + str(track.title), font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(20, 5))
                tags = Frame(window)
                tags.pack(side="top")
                # tags
                Label(tags,
                      text="CURRENT TAGS:\nYear: " + str(audio['date'][0]) + "\nBPM: " + str(audio['bpm'][0]) + "\nKey: " + str(audio['initialkey'][0]) + "\nGenre: " + str(audio['genre'][0]),
                      justify="left").pack(side="left", padx=(0, 40), pady=(10, 10))
                Label(tags, text="NEW TAGS:\nYear: " + str(track.release_date) + "\nBPM: " + str(track.bpm) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre), justify="left").pack(side="right",  padx=(40, 0), pady=(10, 10))

                # load current thumbnail
                thumbnail = Frame(window)
                thumbnail.pack(side="top")
                Label(thumbnail, text="Current artwork", font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(20, 10))
                images = audio["metadata_block_picture"]
                if len(images) > 0:
                    data = base64.b64decode(images[0])
                    image = Picture(data)
                    stream = BytesIO(image.data)
                    image = Image.open(stream).convert("RGBA")
                    stream.close()
                    width, height = image.size
                    thumbnailImageImport = image.resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(thumbnailImageImport)
                    thumbnailImage = Label(thumbnail, image=photo)
                    thumbnailImage.image = photo
                    thumbnailButton = Button(thumbnail, image=photo, bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, window))
                    thumbnailButton.pack(side="top")
                    buttons.append(thumbnailButton)
                    Label(thumbnail, text=str(width) + "x" + str(height)).pack(side="top", pady=(5, 10))
                else:
                    thumbnailButton = Button(window, text="No Artwork Found", bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, thumbnail), height=12, width=28)
                    thumbnailButton.pack(side="top", pady=(5, 10))
                    buttons.append(thumbnailButton)
                # print images as buttons
                images = Frame(window)
                images.pack(side="top")
                imageButtons = {}
                imageResolutions = []
                Label(images, text="Artwork from search", font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(10, 5))
                for i in range(initialCounter, imageCounter):
                    imageRow = Frame(images)
                    imageRow.pack(side="top")
                    start = initialCounter
                    end = min(initialCounter + 4, imageCounter)
                    for j in range(start, end):
                        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(j) + ".jpg")
                        fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(fileImageImport)
                        fileImage = Label(imageRow, image=photo)
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
                Label(tags, text="CURRENT TAGS:\nYear: " + str(audio['date'][0]) + "\nBPM: " + str(audio['bpm'][0]) + "\nKey: " + str(audio['initialkey'][0]) + "\nGenre: " + str(audio['genre'][0]), justify="left").pack(side="left", padx=(0, 40), pady=(10, 10))
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
            images = audio["metadata_block_picture"]
            if len(images) > 0:
                data = base64.b64decode(images[0])
                image = Picture(data)
                stream = BytesIO(image.data)
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
    if track.imageSelection!="THUMB":
        saveImage(track, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

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
    if track.imageSelection!="THUMB":
        saveImage(track, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

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
    if track.imageSelection!="THUMB":
        saveImage(track, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

def skipOption(audio, track, window, webScrapingWindow):
    track.release_date = str(audio['date'][0])
    track.bpm = str(audio['BPM'][0])
    track.key = str(audio['initialkey'][0])
    track.genre = str(audio['genre'][0])
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
    webScrapingWindow.lift()