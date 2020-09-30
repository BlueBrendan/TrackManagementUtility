from statistics import mode
from collections import Counter

#global variables
#imageSelection stores the index of thumbnail images collected by reverse image scraping

#import methods
from track_scraping.conflictPopup.FLAC_conflict import FLAC_conflict
from track_scraping.conflictPopup.ID3_conflict import ID3_conflict
from track_scraping.conflictPopup.Vorbis_conflict import Vorbis_conflict
from track_scraping.conflictPopup.M4A_conflict import M4A_conflict

def buildTrackReport(track, yearList, BPMList, keyList, genreList, audio, filename, webScrapingWindow, characters, options, initialCounter, imageCounter, informalTagDict):
    conflict = False
    # check year for false values
    if len(yearList) != 0:
        commonYearList = [word for word, word_count in Counter(yearList).most_common(5)]
        commonYear = commonYearList[0]
        if len(commonYearList) > 1:
            for i in range(len(commonYearList) - 1):
                # prioritize older years to avoid quoting re-releases
                if len(yearList) <= 5:
                    if int(commonYearList[0]) > int(commonYearList[i + 1]) and yearList.count(
                            commonYearList[0]) <= yearList.count(commonYearList[i + 1]) * 2:
                        commonYear = commonYearList[i + 1]
                else:
                    if int(commonYearList[0]) > int(commonYearList[i + 1]) and yearList.count(
                            commonYearList[0]) <= yearList.count(commonYearList[i + 1]) * 2 and yearList.count(commonYearList[0]) > 1:
                        commonYear = commonYearList[i + 1]
        if track.release_date != str(commonYear):
            track.release_date = str(commonYear)
            conflict = True
    # check BPM for false values
    if len(BPMList) != 0:
        commonBPMList = ([word for word, word_count in Counter(BPMList).most_common(3)])
        commonBPM = commonBPMList[0]
        if len(commonBPMList) > 1 and int(commonBPMList[0]) * 2 == int(commonBPMList[1]) and int(commonBPMList[0]) < 85: commonBPM = commonBPMList[1]
        if track.bpm != str(commonBPM):
            track.bpm = str(commonBPM)
            conflict = True
    if len(keyList) != 0 and track.key != str(mode(keyList)):
        track.key = str(mode(keyList))
        conflict = True
    if len(genreList) != 0 and track.genre != str(mode(genreList)):
        track.genre = str(mode(genreList))
        conflict = True
    #update audio tags
    if conflict == True or imageCounter > 0:
        if filename.endswith(".flac"): FLAC_conflict(audio, track, options, initialCounter, imageCounter, informalTagDict, webScrapingWindow)
        elif filename.endswith(".aiff") or filename.endswith(".mp3") or filename.endswith(".wav"): ID3_conflict(audio, track, options, initialCounter, imageCounter, webScrapingWindow)
        elif filename.endswith(".ogg"): Vorbis_conflict(audio, track, options, initialCounter, imageCounter, webScrapingWindow)
        elif filename.endswith(".m4a"): M4A_conflict(audio, track, options, initialCounter, imageCounter, webScrapingWindow)
    if len(str(track.artist) + " - " + str(track.title)) > characters: characters = len(str(track.artist) + " - " + str(track.title))
    return "\nTrack: " + str(track.artist) + " - " + str(track.title) + "\nYear: " + str(track.release_date) + "\nBPM: " + str(track.bpm) + "\nKey: " + str(track.key) + "\nGenre: " + str(track.genre), webScrapingWindow, characters, track.imageSelection

