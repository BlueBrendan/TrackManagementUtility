from mutagen.flac import Picture
from mutagen import id3
from io import BytesIO
from statistics import mode
from collections import Counter
from tkinter.tix import *
from PIL import Image, ImageTk
import getpass

#global variables
#imageSelection stores the index of thumbnail images collected by reverse image scraping
imageSelection = 'THUMB'

def buildTrackReport(track, yearList, BPMList, keyList, genreList, audio, webScrapingWindow, characters, options, initialCounter, imageCounter):
    global imageSelection
    imageSelection = 'THUMB'
    yearValue = False
    BPMValue = False
    keyValue = False
    genreValue = False
    # check year for false values
    if len(yearList) != 0:
        commonYear = [word for word, word_count in Counter(yearList).most_common(5)]
        track.year = commonYear[0]
        yearValue = True
        if len(commonYear) > 1:
            for i in range(len(commonYear) - 1):
                # prioritize older years to avoid quoting re-releases
                if len(yearList) <= 5:
                    if int(commonYear[0]) > int(commonYear[i + 1]) and yearList.count(
                            commonYear[0]) <= yearList.count(commonYear[i + 1]) * 2:
                        track.year = commonYear[i + 1]
                else:
                    if int(commonYear[0]) > int(commonYear[i + 1]) and yearList.count(
                            commonYear[0]) <= yearList.count(commonYear[i + 1]) * 2 and yearList.count(commonYear[0]) > 1:
                        track.year = commonYear[i + 1]
    # check BPM for false values
    if len(BPMList) != 0:
        commonBPM = ([word for word, word_count in Counter(BPMList).most_common(3)])
        track.BPM = commonBPM[0]
        BPMValue = True
        if len(commonBPM) > 1:
            if int(commonBPM[0]) * 2 == int(commonBPM[1]) and int(commonBPM[0]) < 85:
                track.BPM = commonBPM[1]
    if len(keyList)!=0:
        track.key = str(mode(keyList))
        keyValue = True
    if len(genreList)!=0:
        track.genre = str(mode(genreList))
        genreValue = True
    #update audio tags
    if yearValue == True or BPMValue == True or keyValue == True or genreValue == True:
        if audio['date']!=[''] or audio['bpm']!=[''] or audio['initialkey']!=[''] or audio['genre']!=['']:
            buttons = []
            if str(audio['date'])[2:-2]!=str(track.year) or str(audio['bpm'])[2:-2]!=str(track.BPM) or str(audio['initialkey'])[2:-2]!=track.key or str(audio['genre'])[2:-2]!=track.genre:
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
                if len(str(track.artist) + " - " + str(track.title)) <= 30:
                    conflictPopup.geometry('%dx%d+%d+%d' % (550, 220, x, y))
                else:
                    x = (ws / 2) - ((550 + (len(str(track.artist) + " - " + str(track.title)) * 1.5)) / 2)
                    conflictPopup.geometry('%dx%d+%d+%d' % (550 + (len(str(track.artist) + " - " + str(track.title)) * 1.5), 220, x, y))
                #tags and images
                if options["Reverse Image Search (B)"].get()==True and (imageCounter-initialCounter) >= 1:
                    y = (hs / 2) - (880 / 2)
                    x = (ws / 2) - ((400 + (200*(min(imageCounter-initialCounter,4)))) / 2)
                    conflictPopup.geometry('%dx%d+%d+%d' % (400 + (200 * (min(imageCounter-initialCounter,4))), 800, x, y))
                    Label(window, text="Conflicting tags in " + str(track.artist) + " - " + str(track.title), font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(20,5))
                    tags = Frame(window)
                    tags.pack(side=TOP)
                    #tags
                    Label(tags, text="CURRENT TAGS:\nYear: " + str(audio['date'])[2:-2] + "\nBPM: " + str(audio['bpm'])[2:-2] + "\nKey: " + str(audio['initialkey'])[2:-2] + "\nGenre: " + str(audio['genre'])[2:-2], justify=LEFT).pack(side="left", padx=(0, 40), pady=(10, 10))
                    Label(tags, text="NEW TAGS:\nYear: " + str(track.year) + "\nBPM: " + str(track.BPM) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre), justify=LEFT).pack(side="right", padx=(40, 0), pady=(10, 10))

                    #load current thumbnail
                    thumbnail = Frame(window)
                    thumbnail.pack(side=TOP)
                    Label(thumbnail, text="Current artwork", font=("TkDefaultFont", 9, 'bold')).pack(side=TOP, pady=(20, 10))
                    if len(audio.pictures) > 0:
                        stream = BytesIO(audio.pictures[0].data)
                        image = Image.open(stream).convert("RGBA")
                        stream.close()
                        width, height = image.size
                        thumbnailImageImport = image.resize((200, 200), Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(thumbnailImageImport)
                        thumbnailImage = Label(thumbnail, image=photo)
                        thumbnailImage.image = photo
                        thumbnailButton = Button(thumbnail, image=photo, bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: assignImage("THUMB", thumbnailButton, buttons, window))
                        thumbnailButton.pack(side=TOP)
                        buttons.append(thumbnailButton)
                        Label(thumbnail, text=str(width) + "x" + str(height)).pack(side=TOP, pady=(5, 10))
                    else:
                        thumbnailButton = Button(window, text="No Artwork Found", bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: assignImage("THUMB", thumbnailButton, buttons, thumbnail), height=12, width=28)
                        thumbnailButton.pack(side=TOP, pady=(5, 10))
                        buttons.append(thumbnailButton)
                    # print images as buttons
                    images = Frame(window)
                    images.pack(side=TOP)
                    imageButtons = {}
                    imageResolutions = []
                    Label(images, text="Artwork from search", font=("TkDefaultFont", 9, 'bold')).pack(side=TOP, pady=(10, 5))
                    for i in range(initialCounter, imageCounter):
                        imageRow = Frame(images)
                        imageRow.pack(side=TOP)
                        start = initialCounter
                        end = min(initialCounter+4, imageCounter)
                        for j in range(start, end):
                            fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(j) + ".jpg")
                            fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                            photo = ImageTk.PhotoImage(fileImageImport)
                            fileImage = Label(imageRow, image=photo)
                            fileImage.image = photo
                            imageButtons[j] = Button(imageRow, image=photo, highlightthickness=3, command=lambda j=j:assignImage(j, imageButtons[j], buttons, images))
                            imageButtons[j].pack(side="left", padx=(10,10))
                            buttons.append(imageButtons[j])
                            im = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(j) + ".jpg")
                            width, height = im.size
                            imageResolutions.append(str(height) + "x" + str(width))
                            initialCounter+=1
                        resolutionRow = Frame(images)
                        resolutionRow.pack(side=TOP)
                        # print resolutions underneath respective images
                        for j in range(start, end):
                            Label(resolutionRow, text=imageResolutions[j]).pack(side="left", padx=(90, 90), pady=(5,10))
                    #load option buttons
                    optionButtons = Frame(window)
                    optionButtons.pack(side=TOP)
                    Button(optionButtons, text="Overwrite", command=lambda: overwriteOption(audio, track.year, track.BPM, track.key, track.genre, conflictPopup, webScrapingWindow, imageSelection)).pack(side="left", padx=(15, 15), pady=(25,10))
                    Button(optionButtons, text="Merge (favor scraped data)", command=lambda: mergeScrapeOption(audio, track.year, track.BPM, track.key, track.genre, conflictPopup, webScrapingWindow, imageSelection)).pack(side="left", padx=(15, 15), pady=(25,10))
                    Button(optionButtons, text="Merge (favor source data)", command=lambda: mergeSourceOption(track, audio, conflictPopup, webScrapingWindow, imageSelection)).pack(side="left", padx=(15, 15), pady=(25,10))
                    Button(optionButtons, text="Skip", command=lambda: skipOption(track, audio, conflictPopup, webScrapingWindow, imageSelection)).pack(side="left", padx=(15, 15), pady=(25,10))
                    canvas.update_idletasks()
                    canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrollbar.set)
                    canvas.pack(fill='both', expand=True, side='left')
                    scrollbar.pack(side="right", fill=Y)
                    conflictPopup.lift()
                    conflictPopup.wait_window()
                #tags only
                else:
                    Label(window, text="Conflicting tags in " + str(track.artist) + " - " + str(track.title), font=("TkDefaultFont", 9, 'bold')).grid(row=0, column=0, columnspan=4, pady=(10,0))
                    Label(window, text="CURRENT TAGS: \nYear: " + str(audio['date'])[2:-2] + "\nBPM: " + str(audio['bpm'])[2:-2] + "\nKey: " + str(audio['initialkey'])[2:-2] + "\nGenre: " + str(audio['genre'])[2:-2]).grid(row=1, column=1, pady=(10,35))
                    Label(window, text="NEW TAGS: \nYear: " + str(track.year) + "\nBPM: " + str(track.BPM) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre)).grid(row=1, column=2, pady=(10,35))
                    Button(window, text="Overwrite", command=lambda: overwriteOption(audio, track.year, track.BPM, track.key, track.genre, window, webScrapingWindow, imageSelection)).grid(row=2, column=0)
                    Button(window, text="Merge (favor scraped data)", command=lambda: mergeScrapeOption(audio, track.year, track.BPM, track.key, track.genre, window, webScrapingWindow, imageSelection)).grid(row=2, column=1)
                    Button(window, text="Merge (favor source data)", command=lambda: mergeSourceOption(track, audio, window, webScrapingWindow, imageSelection)).grid(row=2, column=2)
                    Button(window, text="Skip", command=lambda: skipOption(track, audio, window, webScrapingWindow, imageSelection)).grid(row=2, column=3)
                    window.wait_window()
            #images only
            elif imageCounter >= 1:
                window = Toplevel()
                window.attributes("-topmost", True)
                window.title("Multiple Images Found")
                ws = window.winfo_screenwidth()  # width of the screen
                hs = window.winfo_screenheight()  # height of the screen
                y = (hs / 2) - (715 / 2)
                x = (ws / 2) - ((250 + (200 * (imageCounter-initialCounter))) / 2)
                window.geometry('%dx%d+%d+%d' % (250 + (200 * (imageCounter-initialCounter)), 650, x, y))

                #print current thumbnail
                Label(window, text="Current artwork", font=("TkDefaultFont", 9, 'bold')).pack(pady=(20, 10))
                if len(audio.pictures) > 0:
                    stream = BytesIO(audio.pictures[0].data)
                    image = Image.open(stream).convert("RGBA")
                    stream.close()
                    width, height = image.size
                    thumbnailImageImport = image.resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(thumbnailImageImport)
                    thumbnailImage = Label(window, image=photo)
                    thumbnailImage.image = photo
                    thumbnailButton = Button(window, image=photo, bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: assignImage("THUMB", thumbnailButton, buttons, window))
                    thumbnailButton.pack(side=TOP)
                    buttons.append(thumbnailButton)
                    Label(window, text=str(width) + "x" + str(height)).pack(side=TOP, pady=(5, 10))
                else:
                    thumbnailButton = Button(window, text="No Artwork Found", bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: assignImage("THUMB", thumbnailButton, buttons, window), height=12, width=28)
                    thumbnailButton.pack(side=TOP, pady=(5, 10))
                    buttons.append(thumbnailButton)

                Label(window, text="Select a cover image", font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(15, 10))
                images = Frame(window)
                images.pack(side=TOP)
                tags = Frame(window)
                tags.pack(side=TOP)
                optionButtons = Frame(window)
                imageButtons = {}
                imageResolutions = []
                #print images as buttons
                for i in range(initialCounter, imageCounter):
                    window.columnconfigure(i, weight=1)
                    fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg")
                    fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(fileImageImport)
                    fileImage = Label(images, image=photo)
                    fileImage.image = photo
                    imageButtons[i] = Button(images, image=photo, highlightthickness=3, command=lambda i=i: assignImage(i, imageButtons[i], buttons, window))
                    imageButtons[i].pack(side="left", padx=(10, 10))
                    buttons.append(imageButtons[i])
                    im = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg")
                    width, height = im.size
                    imageResolutions.append(str(height) + "x" + str(width))
                resolutions = Frame(window)
                resolutions.pack(side=TOP)
                #print resolutions underneath respective images
                for i in imageResolutions:
                    Label(resolutions, text=i).pack(side="left", padx=(90,90), pady=(5,5))
                optionButtons.pack(side=TOP)
                Button(optionButtons, text="Select", command=lambda: selectImage(imageSelection, audio, window, webScrapingWindow)).pack(side=TOP, pady=(25, 10))
                window.lift()
                window.wait_window()
        else:
            audio['date'] = str(track.year)
            audio['bpm'] = str(track.BPM)
            audio['initialkey'] = track.key
            audio['genre'] = track.genre
            audio.save()
    # return "\nTrack: " + str(artist) + " - " + str(title) + "\nYear: " + str(year) + "\nBPM: " + str(BPM) + "\nKey: " + str(key) + "\nGenre: " + str(genre) + "\nImage Links: " + str(images)
    if len(str(track.artist) + " - " + str(track.title)) > characters:
        characters = len(str(track.artist) + " - " + str(track.title))
    return "\nTrack: " + str(track.artist) + " - " + str(track.title) + "\nYear: " + str(track.year) + "\nBPM: " + str(track.BPM) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre), webScrapingWindow, characters, imageSelection

#four button options
def overwriteOption(audio, year, BPM, key, genre, window, webScrapingWindow, imageSelection):
    audio['date'] = str(year)
    audio['bpm'] = str(BPM)
    audio['initialkey'] = key
    audio['genre'] = genre
    audio.save()
    if imageSelection!="THUMB":
        selectImage(imageSelection, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

def mergeScrapeOption(audio, year, BPM, key, genre, window, webScrapingWindow, imageSelection):
    if str(year) != '':
        audio['date'] = str(year)
    if str(BPM) != '':
        audio['bpm'] = str(BPM)
    if key != '':
        audio['initialkey'] = key
    if genre != '':
        audio['genre'] = genre
    audio.save()
    if imageSelection!="THUMB":
        selectImage(imageSelection, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

def mergeSourceOption(track, audio, window, webScrapingWindow, imageSelection):
    if audio['date'] == ['']: audio['date'] = str(track.year)
    else: track.year = str(audio['date'])[2:-2]
    if audio['bpm'] == ['']: audio['bpm'] = str(track.BPM)
    else: track.BPM = str(audio['BPM'])[2:-2]
    if audio['initialkey'] == ['']: audio['initialkey'] = track.key
    else: track.key = str(audio['initialkey'])[2:-2]
    if audio['genre'] == ['']: audio['genre'] = track.genre
    else: track.genre = str(audio['genre'])[2:-2]
    audio.save()
    if imageSelection!="THUMB":
        selectImage(imageSelection, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

def skipOption(track, audio, window, webScrapingWindow, imageSelection):
    track.year = str(audio['date'])[2:-2]
    track.BPM = str(audio['BPM'])[2:-2]
    track.key = str(audio['initialkey'])[2:-2]
    track.genre = str(audio['genre'])[2:-2]
    webScrapingWindow.lift()
    if imageSelection!="THUMB":
        selectImage(imageSelection, audio, window, webScrapingWindow)
    else:
        window.destroy()
        webScrapingWindow.lift()

#selecting image to variable
def assignImage(i, button, buttons, window):
    global imageSelection
    imageSelection = i
    #unhighlight all buttons
    for item in buttons:
        item.config(bg="white", highlightcolor="white")
    #highlight selected button
    button.config(bg="yellow", highlightcolor="yellow")
    window.update()


#saving image to file
def selectImage(imageSelection, audio, window, webScrapingWindow):
    #first clear all images from audio file
    if imageSelection != "THUMB":
        image = Picture()
        audio.clear_pictures()
        with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageSelection) + ".jpg", 'rb') as f:
            image.data = f.read()
        image.type = id3.PictureType.COVER_FRONT
        image.mime = u"image/jpeg"
        audio.add_picture(image)
        audio.save()
    window.destroy()
    webScrapingWindow.lift()