from statistics import mode
from collections import Counter

#global variables
#imageSelection stores the index of thumbnail images collected by reverse image scraping

#import methods
from track_scraping.conflictPopup.FLAC_conflict import FLAC_conflict
from track_scraping.conflictPopup.AIFF_conflict import ID3_conflict

def buildTrackReport(track, yearList, BPMList, keyList, genreList, audio, filename, webScrapingWindow, characters, options, initialCounter, imageCounter):
    conflict = False
    # check year for false values
    if len(yearList) != 0:
        commonYear = [word for word, word_count in Counter(yearList).most_common(5)]
        track.year = commonYear[0]
        conflict = True
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
        track.bpm = commonBPM[0]
        conflict = True
        if len(commonBPM) > 1:
            if int(commonBPM[0]) * 2 == int(commonBPM[1]) and int(commonBPM[0]) < 85:
                track.bpm = commonBPM[1]
    if len(keyList) != 0:
        track.key = str(mode(keyList))
        conflict = True
    if len(genreList) != 0:
        track.genre = str(mode(genreList))
        conflict = True
    #update audio tags
    if conflict == True:
        if filename.endswith(".flac"): FLAC_conflict(audio, track, options, initialCounter, imageCounter, webScrapingWindow)
        elif filename.endswith(".aiff") or filename.endswith(".mp3"): ID3_conflict(audio, track, options, initialCounter, imageCounter, webScrapingWindow)

    if len(str(track.artist) + " - " + str(track.title)) > characters: characters = len(str(track.artist) + " - " + str(track.title))
    return "\nTrack: " + str(track.artist) + " - " + str(track.title) + "\nYear: " + str(track.year) + "\nBPM: " + str(track.bpm) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre), webScrapingWindow, characters, track.imageSelection

