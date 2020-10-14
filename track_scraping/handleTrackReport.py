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

def handleTrackReport(track, yearList, BPMList, keyList, genreList, audio, filename, webScrapingWindow, characters, options, initialCounter, imageCounter, informalTagDict):
    conflict = False
    # check year for false values
    if "Release_Date" in options["Selected Tags (L)"] and len(yearList) != 0:
        commonYearList = [word for word, word_count in Counter(yearList).most_common(5)]
        commonYear = commonYearList[0]
        if len(commonYearList) > 1:
            for i in range(len(commonYearList) - 1):
                # prioritize older years to avoid quoting re-releases
                if len(yearList) <= 5:
                    if int(commonYearList[0]) > int(commonYearList[i + 1]) and yearList.count(commonYearList[0]) <= yearList.count(commonYearList[i + 1]) * 2: commonYear = commonYearList[i + 1]
                else:
                    if int(commonYearList[0]) > int(commonYearList[i + 1]) and yearList.count(commonYearList[0]) <= yearList.count(commonYearList[i + 1]) * 2 and yearList.count(commonYearList[0]) > 1: commonYear = commonYearList[i + 1]
        if track.release_date != str(commonYear):
            track.release_date = str(commonYear)
            conflict = True
    # check BPM for false values
    if "BPM" in options["Selected Tags (L)"] and len(BPMList) != 0:
        commonBPMList = ([word for word, word_count in Counter(BPMList).most_common(3)])
        commonBPM = commonBPMList[0]
        if len(commonBPMList) > 1 and int(commonBPMList[0]) * 2 == int(commonBPMList[1]) and int(commonBPMList[0]) < 85: commonBPM = commonBPMList[1]
        if track.bpm != str(commonBPM):
            track.bpm = str(commonBPM)
            conflict = True
    if "Key" in options["Selected Tags (L)"] and len(keyList) != 0:
        if len(multimode(keyList)) == 1:
            if track.key != str(mode(keyList)):
                track.key = str(mode(keyList))
                conflict = True
        else:
            modeConflict(track, keyList, "key")
            conflict = True
    if "Genre" in options["Selected Tags (L)"] and len(genreList) != 0:
        if len(multimode(genreList)) == 1:
            if track.genre != str(mode(genreList)):
                track.genre = str(mode(genreList))
                conflict = True
        else:
            modeConflict(track, genreList, "genre")
            conflict = True

    #update audio tags
    if conflict == True or imageCounter > 0:
        if filename.endswith(".flac"): FLAC_conflict(audio, track, options, initialCounter, imageCounter, informalTagDict, webScrapingWindow)
        elif filename.endswith(".aiff") or filename.endswith(".mp3") or filename.endswith(".wav"): ID3_conflict(audio, track, options, initialCounter, imageCounter, informalTagDict, webScrapingWindow)
        elif filename.endswith(".ogg"): Vorbis_conflict(audio, track, options, initialCounter, imageCounter, informalTagDict, webScrapingWindow)
        elif filename.endswith(".m4a"): M4A_conflict(audio, track, options, initialCounter, imageCounter, informalTagDict, webScrapingWindow)
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
    y = (hs / 2) - (242 / 2)
    x = (ws / 2) - (550 / 2)
    popup.geometry('%dx%d+%d+%d' % (500, 220, x, y))
    for i in range(len(multimode(list))):
        x += len(multimode(list)[i])
        popup.update_idletasks()
        popup.geometry('%dx%d+%d+%d' % (popup.winfo_width() + len(multimode(list)[i]), 220, x, y))
    tk.Label(popup, text= type.capitalize() + " Conflict", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="top", pady=(30, 15))
    tk.Label(popup, text= "The search returned equal instances of multiple more than one " + type, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="top", pady=(10, 20))
    radioFrame = tk.Frame(popup)
    radioFrame.config(bg=bg)
    radioFrame.pack()
    for i in range(len(multimode(list))):
        tk.Radiobutton(radioFrame, value=list[i], command=lambda i=i: selectOption(track, list, i, type), activebackground=bg, selectcolor=bg, bg=bg, fg="white").pack(padx=(20, 0), side="left")
        tk.Label(radioFrame, text=list[i], font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    tk.Button(popup, text="Select", font=("Proxima Nova Rg", 11), fg="white", bg=bg, command=popup.destroy).pack(pady=(20, 0))
    originalGenre = track.genre
    popup.lift()
    popup.protocol("WM_DELETE_WINDOW", lambda track=track, popup=popup, genre=originalGenre: onExit(track, genre, popup, type))
    popup.wait_window()

def selectOption(track, list, i, type):
    if type == "genre": track.genre = list[i]

def onExit(track, genre, popup, type):
    if type == "genre": track.genre = genre
    popup.destroy()