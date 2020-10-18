import threading
import queue
import time

#import methods
from track_scraping.handleTrackReport import handleTrackReport
from track_preparation.buildVariations import buildVariations
from web_scrapers.junodownloadSearch import junodownloadSearch
from web_scrapers.beatportSearch import beatportSearch
from web_scrapers.discogsSearch import discogsSearch

def scrapeWeb(track, audio, filename, webScrapingWindow, characters, options, imageCounter, informalTagDict, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, labelFrame, searchFrame, pageFrame, componentFrame):
    initialCounter = imageCounter
    search = str(track.artist) + " - " + str(track.title)
    # clean search query of ampersands (query ends upon reaching ampersand symbol)
    if '&' in search: search = search.replace('&', 'and')
    #lists for year/release date, BPM values, key, genre, and artowrk image URLs
    track.yearList, track.BPMList, track.keyList, track.genreList, track.URLList = [], [], [], [], []
    # build list of artist and track title variations to prepare for scraping
    artistVariations, titleVariations = buildVariations(track.artist, track.title)
    # web scraping
    headers = {'User-Agent': "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1b3pre) Gecko/20090109 Shiretoko/3.1b3pre"}
    # headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",}
    # junodownload
    if options['Scrape Junodownload (B)'].get() == True:
        track.yearList, track.BPMList, track.genreList, imageCounter, track.URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame = junodownloadSearch(filename, track.yearList, track.BPMList, track.genreList, track.URLList, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, labelFrame, searchFrame, pageFrame, componentFrame, audio, options, imageCounter)
    # beatport
    if options['Scrape Beatport (B)'].get() == True:
        track.yearList, track.BPMList, track.keyList, track.genreList, imageCounter, track.URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame = beatportSearch(track.title, filename, track.yearList, track.BPMList, track.keyList, track.genreList, track.URLList, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, labelFrame, searchFrame, pageFrame, componentFrame, audio, options, imageCounter)
    # discogs
    if options['Scrape Discogs (B)'].get() == True:
        track.yearList, track.genreList, imageCounter, track.URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame = discogsSearch(track.title, filename, track.yearList, track.genreList, track.URLList, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, labelFrame, searchFrame, pageFrame, componentFrame, audio, options, imageCounter)
    # spotify
    # apple music
    reportTitle, reportResults, webScrapingWindow, characters, imageSelection = handleTrackReport(track, track.yearList, track.BPMList, track.keyList, track.genreList, audio, filename, webScrapingWindow, characters, options, initialCounter, imageCounter, informalTagDict)
    return reportTitle, reportResults, webScrapingWindow, characters, imageCounter, imageSelection, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame

