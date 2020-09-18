#import methods
from track_scraping.buildTrackReport import buildTrackReport
from track_preparation.buildVariations import buildVariations
from web_scrapers.junodownloadSearch import junodownloadSearch
from web_scrapers.beatportSearch import beatportSearch
from web_scrapers.discogsSearch import discogsSearch

def scrapeWeb(track, audio, var, frame, webScrapingWindow, characters, options, imageCounter):
    initialCounter = imageCounter
    search = str(track.artist) + " - " + str(track.title)
    # clean search query of ampersands (query ends upon reaching ampersand symbol)
    if '&' in search:
        search = search.replace('&', 'and')
    #stores year/release dates
    yearList = []
    #stores BPM values
    BPMList = []
    #stores key values
    keyList = []
    #stores genre values
    genreList = []
    #stores artwork image URLs to avoid duplicates
    URLList = []
    # build list of artist and track title variations to prepare for scraping
    artistVariations, titleVariations = buildVariations(track.artist, track.title)

    # web scraping
    headers = {'User-Agent': "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1b3pre) Gecko/20090109 Shiretoko/3.1b3pre"}
    # headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",}

    # junodownload
    if options['Scrape Junodownload (B)'].get() == True:yearList, BPMList, genreList, imageCounter, URLList = junodownloadSearch(track.artist, track.title, var, yearList, BPMList, genreList, URLList, artistVariations, titleVariations, headers, search, frame, webScrapingWindow, audio, options, imageCounter)
    # beatport
    if options['Scrape Beatport (B)'].get() == True:yearList, BPMList, keyList, genreList, imageCounter, URLList = beatportSearch(track.artist, track.title, var, yearList, BPMList, keyList, genreList, URLList, artistVariations, titleVariations, headers, search, frame, webScrapingWindow, audio, options, imageCounter)
    # discogs
    if options['Scrape Discogs (B)'].get() == True:yearList, genreList, imageCounter, URLList = discogsSearch(track.artist, track.title, var, yearList, genreList, URLList, artistVariations, titleVariations, headers, search, frame, webScrapingWindow, options, imageCounter)
    # spotify
    # apple music
    finalResults, webScrapingWindow, characters, imageSelection = buildTrackReport(track, yearList, BPMList, keyList, genreList, audio, webScrapingWindow, characters, options, initialCounter, imageCounter)
    return finalResults, webScrapingWindow, characters, imageCounter, imageSelection