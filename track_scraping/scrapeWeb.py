#import methods
from track_scraping.buildTrackReport import buildTrackReport
from track_preparation.buildVariations import buildVariations
from web_scrapers.junodownloadSearch import junodownloadSearch
from web_scrapers.beatportSearch import beatportSearch
from web_scrapers.discogsSearch import discogsSearch
from web_scrapers.webScrapingWindowControl import enableControls

def scrapeWeb(track, audio, filename, webScrapingWindow, characters, options, imageCounter):
    initialCounter = imageCounter
    search = str(track.artist) + " - " + str(track.title)
    # clean search query of ampersands (query ends upon reaching ampersand symbol)
    if '&' in search: search = search.replace('&', 'and')
    #lists for year/release date, BPM values, key, genre, and artowrk image URLs
    yearList, BPMList, keyList, genreList, URLList = [], [], [], [], []
    # build list of artist and track title variations to prepare for scraping
    artistVariations, titleVariations = buildVariations(track.artist, track.title)

    # web scraping
    headers = {'User-Agent': "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1b3pre) Gecko/20090109 Shiretoko/3.1b3pre"}
    # headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",}

    #dictionary to store web scraping window values
    webScrapingLeftPane = {}
    webScrapingRightPane = {}
    webScrapingLinks = {}
    webScrapingPage = 0
    componentFrame = 0
    pageFrame = 0
    # junodownload
    if options['Scrape Junodownload (B)'].get() == True:yearList, BPMList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, componentFrame = junodownloadSearch(filename, yearList, BPMList, genreList, URLList, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, audio, options, imageCounter)
    # beatport
    if options['Scrape Beatport (B)'].get() == True:yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, componentFrame = beatportSearch(track.title, filename, yearList, BPMList, keyList, genreList, URLList, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, audio, options, imageCounter)
    # discogs
    if options['Scrape Discogs (B)'].get() == True:yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, componentFrame = discogsSearch(track.title, filename, yearList, genreList, URLList, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, options, imageCounter)
    # spotify
    # apple music
    #enable controls in web scraping window
    enableControls(pageFrame, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, componentFrame)
    finalResults, webScrapingWindow, characters, imageSelection = buildTrackReport(track, yearList, BPMList, keyList, genreList, audio, filename, webScrapingWindow, characters, options, initialCounter, imageCounter)
    return finalResults, webScrapingWindow, characters, imageCounter, imageSelection