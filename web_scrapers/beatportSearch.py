import tkinter as tk
from tkinter.tix import *
import requests
from bs4 import BeautifulSoup
import getpass
from PIL import Image, ImageTk
import webbrowser
import time
import random

#import methods
from track_scraping.compareTokens import compareTokens
from track_scraping.reverseImageSearch import reverseImageSearch
from web_scrapers.webScrapingWindowControl import rerenderControls
from web_scrapers.compareRuntime import compareRuntime

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

def allWidgets(window):
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())
    return _list

def beatportSearch(title, var, yearList, BPMList, keyList, genreList, URLList, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, audio, options, imageCounter):
    #SECOND QUERY - BEATPORT
    widgetList = allWidgets(webScrapingWindow)
    for item in widgetList:
        item.pack_forget()

    # component for search label and page indicator
    labelFrame = tk.Frame(webScrapingWindow, bg=bg)
    labelFrame.pack(fill=X, pady=(10, 10))
    searchFrame = tk.Frame(labelFrame, bg=bg)
    searchFrame.pack(side="left")
    pageFrame = tk.Frame(labelFrame, bg=bg)
    pageFrame.pack(side="right", pady=(18, 0))
    tk.Label(searchFrame, text="\nSearching Beatport for " + str(var), font=("Proxima Nova Rg", 13), fg="white", bg=bg, anchor='w').pack(side="left", padx=(10, 0))
    # page counter and navigation buttons
    rerenderControls(pageFrame, webScrapingPage)

    componentFrame = tk.Frame(webScrapingWindow, bg=bg)
    componentFrame.pack(fill=X, pady=(10, 0))
    # component for text
    leftComponentFrame = tk.Frame(componentFrame, bg=bg)
    leftComponentFrame.pack(side="left", anchor="w", fill=Y)
    # component for image
    rightComponentFrame = tk.Frame(componentFrame, bg=bg)
    rightComponentFrame.pack(side="right", anchor="e", fill=Y)

    webScrapingWindow.update()
    webScrapingWindow.attributes("-topmost", 1)
    webScrapingWindow.attributes("-topmost", 0)
    url = "https://www.google.co.in/search?q=" + search + " Beatport"
    soup = sendRequest(url, headers, webScrapingWindow)
    if soup == False:
        Label(leftComponentFrame, text="Connection Failed").pack(anchor='w')
        refresh(webScrapingWindow)
        return yearList, BPMList, keyList, genreList
    for link in soup.find_all('a'):
        if "www.beatport.com" in link.get('href').split('&')[0]:
            lastForwardslashIndex = link.get('href').split('&')[0].lower().index('/', link.get('href').split('&')[0].lower().rfind('/'))
            content = link.get('href').split('&')[0].lower()[link.get('href').split('&')[0].lower().index('beatport.com') + len("beatport.com"):lastForwardslashIndex]
            content = content[content.index('/', 1)+1:].replace('-', ' ')
            contentVariations = [content]
            if 'extended remix' in content.lower():
                contentVariations.append(content.replace('extended remix', 'remix'))
            mismatch = True
            if '/' not in content:
                for variation in titleVariations:
                    variation = variation.replace('-', ' ')
                    for content in contentVariations:
                        if variation in content:
                            mismatch = False
                            break
                        else:
                            mismatch = compareTokens(variation, content)
                            if not mismatch:break
                    if not mismatch:break
            if mismatch == False:
                link = link.get('href').split('&')[0].split('=')[1]
                if "remix" in link and "remix" in title.lower() or "remix" not in title.lower() and "remix" not in link:
                    # clear component frames of existing content
                    widgetList = allWidgets(leftComponentFrame)
                    for item in widgetList: item.pack_forget()
                    widgetList = allWidgets(rightComponentFrame)
                    for item in widgetList: item.pack_forget()
                    widgetList = allWidgets(pageFrame)
                    for item in widgetList: item.pack_forget()
                    webScrapingPage += 1
                    # page counter and navigation buttons
                    rerenderControls(pageFrame, webScrapingPage)
                    if len(link) > 75: label = tk.Label(leftComponentFrame, text="\n" + str(link)[0:74] + "...", cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    else: label = tk.Label(leftComponentFrame, text="\n" + str(link), cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                    label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
                    label.pack(padx=(10, 0))
                    webScrapingLeftPane[webScrapingPage] = leftComponentFrame
                    webScrapingLinks[webScrapingPage] = link
                    webScrapingWindow.update()
                    webScrapingWindow.attributes("-topmost", 1)
                    webScrapingWindow.attributes("-topmost", 0)
                    soup = sendRequest(link, headers, webScrapingWindow)
                    if soup != False and "Oops... the page you were looking for could not be found" not in str(soup):
                        #check if page is a track (single) or a release (album)
                        #case 1: release
                        if link[25:32] == "release": yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingPage = beatportRelease(soup, titleVariations, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
                        #case 2: track
                        elif link[25:30] == "track": yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingPage = beatportTrack(soup, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
    return yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, componentFrame

#search beatport releases, filter individual tracks
def beatportRelease(soup, titleVariations, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter):
    for link in soup.find_all('li', class_="bucket-item ec-item track"):
        # find all tracks in the release that contain the title
        link = link.find('p', class_="buk-track-title")
        if link.find('a')['href'] in titleVariations:
            url = "https://www.beatport.com" + str(link.find('a')['href'])
            soup = sendRequest(url, headers, webScrapingWindow)
            if soup == False:
                tk.Label(webScrapingWindow, text="Connection Failed").pack(anchor='w')
                refresh(webScrapingWindow)
                return yearList, BPMList, keyList, genreList, imageCounter
            yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingPage = beatportTrack(soup, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
    return yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingPage

#search beatport tracks, extract info in the event of a match
def beatportTrack(soup, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter):
    link = soup.find('div', class_="interior-track-content")
    if link is not None:
        # check runtime
        length = soup.find('li', class_="interior-track-content-item interior-track-length")
        length = length.find('span', class_="value").get_text()
        if compareRuntime(length, audio) == False:
            trackHeader = soup.find('div', class_="interior-title")
            trackName = trackHeader.find('h1').get_text()
            trackMix = trackHeader.find('h1', class_="remixed").get_text()
            if trackMix != '' and 'original' not in trackMix.lower() and '(' in title and ')' in title:
                remix = title[title.rfind('(') + 1:title.rfind(')')]
                if compareTokens(remix, trackMix) == False:
                    yearList, BPMList, keyList, genreList, URLList, imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingPage = extractInfo(soup, yearList, BPMList, keyList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
            else:
                yearList, BPMList, keyList, genreList, URLList, imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingPage = extractInfo(soup, yearList, BPMList, keyList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
    return yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingPage

#extract year, BPM, key, and genre
def extractInfo(soup, yearList, BPMList, keyList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter):
    for link in soup.find_all('ul', class_="interior-track-content-list"):
        release = link.find('li', class_="interior-track-content-item interior-track-released")
        release = release.find('span', class_="value").get_text()
        tk.Label(leftComponentFrame, text="Year: " + str(release[0:4]), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(30, 0), anchor="w")
        webScrapingLeftPane[webScrapingPage] = leftComponentFrame
        refresh(webScrapingWindow)
        yearList.append(int(release[0:4]))
        BPM = link.find('li', class_="interior-track-content-item interior-track-bpm")
        BPM = BPM.find('span', class_="value").get_text()
        tk.Label(leftComponentFrame, text="BPM: " + str(BPM), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
        webScrapingLeftPane[webScrapingPage] = leftComponentFrame
        refresh(webScrapingWindow)
        BPMList.append(int(BPM))
        key = link.find('li', class_="interior-track-content-item interior-track-key")
        key = key.find('span', class_="value").get_text()
        tk.Label(leftComponentFrame, text="Key: " + str(key), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
        webScrapingLeftPane[webScrapingPage] = leftComponentFrame
        refresh(webScrapingWindow)
        keyList.append(key)
        genre = link.find('li', class_="interior-track-content-item interior-track-genre")
        if genre.find('span', class_="value sep"):
            firstGenre = genre.find('span', class_="value")
            firstGenre = firstGenre.find('a').get_text()
            secondGenre = genre.find('span', class_="value sep")
            secondGenre = secondGenre.find('a').get_text()
            tk.Label(leftComponentFrame, text="Genre: " + str(firstGenre) + ' | ' + str(secondGenre), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
            webScrapingLeftPane[webScrapingPage] = leftComponentFrame
            refresh(webScrapingWindow)
            genreList.append(firstGenre)
            genreList.append(secondGenre)
        else:
            genre = genre.find('span', class_="value")
            genre = genre.find('a').get_text()
            tk.Label(leftComponentFrame, text="Genre: " + str(genre), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
            webScrapingLeftPane[webScrapingPage] = leftComponentFrame
            refresh(webScrapingWindow)
            genreList.append(genre)
    link = soup.find('img', class_="interior-track-release-artwork")
    if link!=None:
        link = link['src']
        # write beatport image to drive
        with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg", "wb") as file:
            file.write(requests.get(link, headers=headers).content)
        URLList.append(link)
        # load file icon
        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg")
        fileImageImport = fileImageImport.resize((180, 180), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(fileImageImport)
        fileImage = Label(rightComponentFrame, image=photo, bg=bg)
        fileImage.image = photo
        fileImage.pack(padx=(0, 100), anchor="e")
        webScrapingWindow.update()
        imageCounter+=1
        webScrapingRightPane[webScrapingPage] = rightComponentFrame
        # perform image scraping if enabled in options
        if options["Reverse Image Search (B)"].get() == True:
            imageCounter, URLList = reverseImageSearch(link, headers, webScrapingWindow, imageCounter, URLList, options)
    return yearList, BPMList, keyList, genreList, URLList, imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingPage

def sendRequest(url, headers, window):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return soup
    except requests.exceptions.ConnectionError:
        tk.Label(window, text="Connection refused").pack(anchor='w')
        window.update()
        # generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return False

def refresh(window):
    window.update()


