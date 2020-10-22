import tkinter as tk
from statistics import mode, multimode
from collections import Counter

#import methods
from track_scraping.conflictPopup.FLAC_conflict import FLAC_conflict
from track_scraping.conflictPopup.ID3_conflict import ID3_conflict
from track_scraping.conflictPopup.Vorbis_conflict import Vorbis_conflict
from track_scraping.conflictPopup.M4A_conflict import M4A_conflict

# main bg color
bg = "#282f3b"
# secondary color
secondary_bg = "#364153"

def handleTrackReport(track, audio, filename, webScrapingWindow, characters, options, initialCounter, imageCounter, images, informalTagDict):
    conflict = False
    # check year for false values
    if "Release_Date" in options["Selected Tags (L)"] and len(track.yearList) != 0:
        commonYearList = [word for word, word_count in Counter(track.yearList).most_common(5)]
        commonYear = commonYearList[0]
        if len(commonYearList) > 1:
            for i in range(len(commonYearList) - 1):
                # prioritize older years to avoid quoting re-releases
                if len(track.yearList) <= 5 and int(commonYearList[0]) > int(commonYearList[i + 1]) and track.yearList.count(commonYearList[0]) <= track.yearList.count(commonYearList[i + 1]) * 2: commonYear = commonYearList[i + 1]
                elif int(commonYearList[0]) > int(commonYearList[i + 1]) and track.yearList.count(commonYearList[0]) <= track.yearList.count(commonYearList[i + 1]) * 2 and track.yearList.count(commonYearList[0]) > 1: commonYear = commonYearList[i + 1]
        if track.release_date != str(commonYear):
            track.release_date = str(commonYear)
            conflict = True
    # check BPM for false values
    if "BPM" in options["Selected Tags (L)"] and len(track.BPMList) != 0:
        commonBPMList = ([word for word, word_count in Counter(track.BPMList).most_common(3)])
        commonBPM = commonBPMList[0]
        if len(commonBPMList) > 1 and int(commonBPMList[0]) * 2 == int(commonBPMList[1]) and int(commonBPMList[0]) < 85: commonBPM = commonBPMList[1]
        if track.bpm != str(commonBPM):
            track.bpm = str(commonBPM)
            conflict = True
    if "Key" in options["Selected Tags (L)"] and len(track.keyList) != 0:
        if len(multimode(track.keyList)) == 1:
            if track.key != str(mode(track.keyList)):
                track.key = str(mode(track.keyList))
                conflict = True
        else:
            modeConflict(track, track.keyList, "key")
            conflict = True
    if "Genre" in options["Selected Tags (L)"] and len(track.genreList) != 0:
        if len(multimode(track.genreList)) == 1:
            if track.genre != str(mode(track.genreList)):
                track.genre = str(mode(track.genreList))
                conflict = True
        else:
            modeConflict(track, track.genreList, "genre")
            conflict = True

    #update audio tags
    if conflict == True or imageCounter > 0:
        if filename.endswith(".flac"): FLAC_conflict(audio, track, options, initialCounter, imageCounter, images, informalTagDict)
        elif filename.endswith(".aiff") or filename.endswith(".mp3") or filename.endswith(".wav"): ID3_conflict(audio, track, options, initialCounter, imageCounter, images, informalTagDict)
        elif filename.endswith(".ogg"): Vorbis_conflict(audio, track, options, initialCounter, imageCounter, images, informalTagDict)
        elif filename.endswith(".m4a"): M4A_conflict(audio, track, options, initialCounter, imageCounter, images, informalTagDict)
    if len(str(track.artist) + " - " + str(track.title)) > characters: characters = len(str(track.artist) + " - " + str(track.title))

    title = str(track.artist) + " - " + str(track.title)
    results = ""
    if "Release_Date" in options["Selected Tags (L)"]: results += "\nYear: " + str(track.release_date)
    if "BPM" in options["Selected Tags (L)"]: results += "\nBPM: " + str(track.bpm)
    if "Key" in options["Selected Tags (L)"]: results += "\nKey: " + str(track.key)
    if "Genre" in options["Selected Tags (L)"]: results += "\nGenre: " + str(track.genre)
    return title, results, webScrapingWindow, characters, track.imageSelection

# enter when the mode returns two or more values for any parameter
def modeConflict(track, list, type):
    popup = tk.Toplevel()
    popup.title("Genre Conflict")
    popup.configure(bg=bg)
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    initialWidth = 550
    y = (hs / 2) - (253 / 2)
    for i in range(len(multimode(list))):
        initialWidth += (len(multimode(list)[i])) * 7
    x = (ws / 2) - (initialWidth / 2)
    popup.geometry('%dx%d+%d+%d' % (initialWidth, 230, x, y))
    tk.Label(popup, text=type.capitalize() + " Conflict", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="top", pady=(30, 15))
    tk.Label(popup, text="The search returned equal instances of multiple more than one " + type, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="top", pady=(10, 20))
    radioFrame = tk.Frame(popup)
    radioFrame.config(bg=bg)
    radioFrame.pack()
    selection = tk.StringVar()
    selection.set(None)
    for i in range(len(multimode(list))):
        option = tk.Radiobutton(radioFrame, value=list[i], variable=selection, command=lambda i=i: selectOption(track, list, i, selection, selectButton, type), activebackground=bg, selectcolor=bg, bg=bg, fg="white")
        option.deselect()
        option.pack(padx=(20, 0), side="left")
        tk.Label(radioFrame, text=list[i], font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    selectButton = tk.Button(popup, text="Select", font=("Proxima Nova Rg", 11), state=tk.DISABLED, fg="white", bg=bg, command=popup.destroy)
    selectButton.pack(pady=(30, 0))
    originalGenre = track.genre
    popup.attributes("-topmost", True)
    popup.protocol("WM_DELETE_WINDOW", lambda track=track, popup=popup, genre=originalGenre: onExit(track, genre, popup, type))
    popup.wait_window()

def selectOption(track, list, i, selection, selectButton, type):
    selectButton.config(state=tk.NORMAL)
    selection.set(list[i])
    if type == "genre": track.genre = list[i]

def onExit(track, genre, popup, type):
    if type == "genre": track.genre = genre
    popup.destroy()