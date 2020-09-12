from statistics import mode
from collections import Counter
from tkinter.tix import *
from PIL import Image, ImageTk
import getpass


def overwriteOption(audio, year, BPM, key, genre, window, webScrapingWindow):
    audio['date'] = str(year)
    audio['bpm'] = str(BPM)
    audio['initialkey'] = key
    audio['genre'] = genre
    audio.pprint()
    audio.save()
    window.destroy()
    webScrapingWindow.lift()

def mergeScrapeOption(audio, year, BPM, key, genre, window, webScrapingWindow):
    if str(year) != '':
        audio['date'] = str(year)
    if str(BPM) != '':
        audio['bpm'] = str(BPM)
    if key != '':
        audio['initialkey'] = key
    if genre != '':
        audio['genre'] = genre
    audio.pprint()
    audio.save()
    window.destroy()
    webScrapingWindow.lift()

def mergeSourceOption(track, audio, window, webScrapingWindow):
    if audio['date'] == ['']: audio['date'] = str(track.year)
    else: track.year = str(audio['date'])[2:-2]
    if audio['bpm'] == ['']: audio['bpm'] = str(track.BPM)
    else: track.BPM = str(audio['BPM'])[2:-2]
    if audio['initialkey'] == ['']: audio['initialkey'] = track.key
    else: track.key = str(audio['initialkey'])[2:-2]
    if audio['genre'] == ['']: audio['genre'] = track.genre
    else: track.genre = str(audio['genre'])[2:-2]
    audio.pprint()
    audio.save()
    window.destroy()
    webScrapingWindow.lift()

def skipOption(track, audio, window, webScrapingWindow):
    track.year = str(audio['date'])[2:-2]
    track.BPM = str(audio['BPM'])[2:-2]
    track.key = str(audio['initialkey'])[2:-2]
    track.genre = str(audio['genre'])[2:-2]
    webScrapingWindow.lift()
    window.destroy()

def buildTrackReport(track, yearList, BPMList, keyList, genreList, audio, webScrapingWindow, characters, options, imageCounter):
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
            if str(audio['date'])[2:-2]!=str(track.year) or str(audio['bpm'])[2:-2]!=str(track.BPM) or str(audio['initialkey'])[2:-2]!=track.key or str(audio['genre'])[2:-2]!=track.genre:
                window = Toplevel()
                window.attributes("-topmost", True)
                window.title("Conflicting Tags")
                ws = window.winfo_screenwidth()  # width of the screen
                hs = window.winfo_screenheight()  # height of the screen
                x = (ws / 2) - (550 / 2)
                y = (hs / 2) - (320 / 2)
                if len(str(track.artist) + " - " + str(track.title)) <= 30:
                    window.geometry('%dx%d+%d+%d' % (550, 220, x, y))
                else:
                    x = (ws / 2) - ((550 + (len(str(track.artist) + " - " + str(track.title)) * 1.5)) / 2)
                    window.geometry('%dx%d+%d+%d' % (550 + (len(str(track.artist) + " - " + str(track.title)) * 1.5), 220, x, y))
                window.columnconfigure(0, weight=1)
                window.columnconfigure(1, weight=1)
                window.columnconfigure(2, weight=1)
                window.columnconfigure(3, weight=1)
                if options["Reverse Image Search (B)"].get()==True and imageCounter >= 1:
                    y = (hs / 2) - (550 / 2)
                    x = (ws / 2) - ((550 + (150*imageCounter)) / 2)
                    window.geometry('%dx%d+%d+%d' % (550 + (150*imageCounter), 440, x, y))
                    Label(window, text="Conflicting tags in " + str(track.artist) + " - " + str(track.title), font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(10,5))
                    tags = Frame(window)
                    tags.pack(side=TOP)
                    Label(tags, text="CURRENT TAGS: \nYear: " + str(audio['date'])[2:-2] + "\nBPM: " + str(audio['bpm'])[2:-2] + "\nKey: " + str(audio['initialkey'])[2:-2] + "\nGenre: " + str(audio['genre'])[2:-2]).pack(side="left", padx=(5, 35), pady=(10,15))
                    Label(tags, text="NEW TAGS: \nYear: " + str(track.year) + "\nBPM: " + str(track.BPM) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre)).pack(side="right", padx=(35, 5), pady=(10,15))
                    images = Frame(window)
                    images.pack(side=TOP)
                    for i in range(imageCounter):
                        window.columnconfigure(i, weight=1)
                        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg")
                        fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(fileImageImport)
                        fileImage = Label(images, image=photo)
                        fileImage.image = photo
                        Button(images, image=photo, command=lambda i=i:print(i)).pack(side="left", padx=(10,10))
                    buttons = Frame(window)
                    buttons.pack(side=TOP)
                    Button(buttons, text="Overwrite", command=lambda: overwriteOption(audio, track.year, track.BPM, track.key, track.genre, window, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25,10))
                    Button(buttons, text="Merge (favor scraped data)", command=lambda: mergeScrapeOption(audio, track.year, track.BPM, track.key, track.genre, window, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25,10))
                    Button(buttons, text="Merge (favor source data)", command=lambda: mergeSourceOption(track, audio, window, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25,10))
                    Button(buttons, text="Skip", command=lambda: skipOption(track, audio, window, webScrapingWindow)).pack(side="left", padx=(15, 15), pady=(25,10))
                    window.lift()
                    window.wait_window()
                else:
                    Label(window, text="Conflicting tags in " + str(track.artist) + " - " + str(track.title), font=("TkDefaultFont", 9, 'bold')).grid(row=0, column=0, columnspan=4, pady=(10,0))
                    Label(window, text="CURRENT TAGS: \nYear: " + str(audio['date'])[2:-2] + "\nBPM: " + str(audio['bpm'])[2:-2] + "\nKey: " + str(audio['initialkey'])[2:-2] + "\nGenre: " + str(audio['genre'])[2:-2]).grid(row=1, column=1, pady=(10,35))
                    Label(window, text="NEW TAGS: \nYear: " + str(track.year) + "\nBPM: " + str(track.BPM) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre)).grid(row=1, column=2, pady=(10,35))
                    Button(window, text="Overwrite", command=lambda: overwriteOption(audio, track.year, track.BPM, track.key, track.genre, window, webScrapingWindow)).grid(row=2, column=0)
                    Button(window, text="Merge (favor scraped data)", command=lambda: mergeScrapeOption(audio, track.year, track.BPM, track.key, track.genre, window, webScrapingWindow)).grid(row=2, column=1)
                    Button(window, text="Merge (favor source data)", command=lambda: mergeSourceOption(track, audio, window, webScrapingWindow)).grid(row=2, column=2)
                    Button(window, text="Skip", command=lambda: skipOption(track, audio, window, webScrapingWindow)).grid(row=2, column=3)
                    window.wait_window()
            elif imageCounter >= 1:
                window = Toplevel()
                window.attributes("-topmost", True)
                window.title("Multiple Images Found")
                ws = window.winfo_screenwidth()  # width of the screen
                hs = window.winfo_screenheight()  # height of the screen
                y = (hs / 2) - (550 / 2)
                x = (ws / 2) - ((550 + (150 * imageCounter)) / 2)
                window.geometry('%dx%d+%d+%d' % (550 + (150 * imageCounter), 440, x, y))
                Label(window, text="Select a cover image", font=("TkDefaultFont", 9, 'bold')).pack(side="top", pady=(10, 5))
                images = Frame(window)
                images.pack(side=TOP)
                tags = Frame(window)
                tags.pack(side=TOP)
                for i in range(imageCounter):
                    window.columnconfigure(i, weight=1)
                    fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg")
                    fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(fileImageImport)
                    fileImage = Label(images, image=photo)
                    fileImage.image = photo
                    Button(tags, image=photo, command=lambda i=i:print(i)).pack(side="left", padx=(10, 10))
                buttons = Frame(window)
                buttons.pack(side=TOP)
                Button(buttons, text="Select", command=lambda: window.destroy()).pack(side="left", padx=(15, 15),pady=(25, 10))
                Button(buttons, text="None", command=lambda: window.destroy()).pack(side="left", padx=(15, 15), pady=(25, 10))
                window.lift()
                window.wait_window()

        else:
            audio['date'] = str(track.year)
            audio['bpm'] = str(track.BPM)
            audio['initialkey'] = track.key
            audio['genre'] = track.genre
            audio.pprint()
            audio.save()
    # return "\nTrack: " + str(artist) + " - " + str(title) + "\nYear: " + str(year) + "\nBPM: " + str(BPM) + "\nKey: " + str(key) + "\nGenre: " + str(genre) + "\nImage Links: " + str(images)
    if len(str(track.artist) + " - " + str(track.title)) > characters:
        characters = len(str(track.artist) + " - " + str(track.title))
    return "\nTrack: " + str(track.artist) + " - " + str(track.title) + "\nYear: " + str(track.year) + "\nBPM: " + str(track.BPM) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre), webScrapingWindow, characters