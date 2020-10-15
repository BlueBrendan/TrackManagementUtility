import tkinter as tk
from tkinter.tix import *
import requests
import getpass
from PIL import Image, ImageTk
import webbrowser

#import methods
from track_scraping.compareTokens import compareTokens
from track_scraping.reverseImageSearch import reverseImageSearch
from web_scrapers.webScrapingWindowControl import rerenderControls
from web_scrapers.webScrapingWindowControl import resetLeftRightFrames
from web_scrapers.sendRequest import prepareRequest
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
    pageFrame.pack(side="right", pady=(20, 0))
    if len(var) > 60: tk.Label(searchFrame, text="\nSearching Beatport for " + str(var)[0:59] + "...", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="left", padx=(10, 0), anchor='w')
    else: tk.Label(searchFrame, text="\nSearching Beatport for " + str(var), font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="left", padx=(10, 0), anchor='w')
    # page counter and navigation buttons
    rerenderControls(pageFrame, webScrapingPage)

    componentFrame = tk.Frame(webScrapingWindow, bg=bg)
    componentFrame.pack(fill=X, pady=(10, 0))
    leftComponentFrame, rightComponentFrame = resetLeftRightFrames(componentFrame)
    refresh(webScrapingWindow)
    url = "https://www.google.co.in/search?q=" + search + " Beatport"
    soup = prepareRequest(url, headers, webScrapingWindow, leftComponentFrame)
    if soup == False:
        Label(leftComponentFrame, text="Connection Failure", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(anchor='w')
        refresh(webScrapingWindow)
        return yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame
    for link in soup.find_all('a'):
        if "www.beatport.com" in link.get('href').split('&')[0]:
            lastForwardslashIndex = link.get('href').split('&')[0].lower().index('/', link.get('href').split('&')[0].lower().rfind('/'))
            content = link.get('href').split('&')[0].lower()[link.get('href').split('&')[0].lower().index('beatport.com') + len("beatport.com"):lastForwardslashIndex]
            if content.count('/') > 1:
                content = content[content.index('/', 1)+1:].replace('-', ' ')
                contentVariations = [content]
                if 'extended remix' in content.lower(): contentVariations.append(content.replace('extended remix', 'remix'))
                mismatch = True
                if '/' not in content:
                    for variation in titleVariations:
                        for content in contentVariations:
                            if variation in content:
                                mismatch = False
                                break
                            else:
                                mismatch = compareTokens(variation, content)
                                if not mismatch: break
                        if not mismatch:break
                if mismatch == False:
                    link = link.get('href').split('&')[0].split('=')[1]
                    if "remix" in link and "remix" in title.lower() or "remix" not in title.lower() and "remix" not in link:
                        # clear component frames of existing content
                        widgetList = allWidgets(componentFrame)
                        for item in widgetList: item.pack_forget()
                        widgetList = allWidgets(pageFrame)
                        for item in widgetList: item.pack_forget()
                        webScrapingPage += 1
                        leftComponentFrame, rightComponentFrame = resetLeftRightFrames(componentFrame)

                        # page counter and navigation buttons
                        rerenderControls(pageFrame, webScrapingPage)
                        if len(link) > 75: label = tk.Label(leftComponentFrame, text="\n" + str(link)[0:74] + "...", cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                        else: label = tk.Label(leftComponentFrame, text="\n" + str(link), cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                        label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
                        label.pack(padx=(10, 0), pady=(0, 25), anchor='w')
                        webScrapingLeftPane[webScrapingPage] = leftComponentFrame
                        # assume match will fail and no image will be found
                        webScrapingRightPane[webScrapingPage] = "NA"
                        webScrapingLinks[webScrapingPage] = link
                        refresh(webScrapingWindow)
                        soup = prepareRequest(link, headers, webScrapingWindow, leftComponentFrame)
                        if soup != False and "Oops... the page you were looking for could not be found" not in str(soup):
                            #check if page is a track (single) or a release (album)
                            #case 1: release
                            if link[25:32] == "release": yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane = beatportRelease(soup, titleVariations, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
                            #case 2: track
                            elif link[25:30] == "track": yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane = beatportTrack(soup, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
                        else: tk.Label(leftComponentFrame, text="Track failed due to dead link or territory restriction", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
    return yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame

#search beatport releases, filter individual tracks
def beatportRelease(soup, titleVariations, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter):
    for link in soup.find_all('li', class_="bucket-item ec-item track"):
        # find all tracks in the release that contain the title
        link = link.find('p', class_="buk-track-title")
        if link.find('a')['href'].lower() in titleVariations:
            url = "https://www.beatport.com" + str(link.find('a')['href'])
            soup = prepareRequest(url, headers, webScrapingWindow, leftComponentFrame)
            if soup == False:
                tk.Label(leftComponentFrame, text="Connection Failure", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(anchor='w')
                refresh(webScrapingWindow)
                return yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane
            yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane = beatportTrack(soup, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
    return yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane

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
                if compareTokens(remix, trackMix) == False: yearList, BPMList, keyList, genreList, URLList, imageCounter, webScrapingLeftPane, webScrapingRightPane = extractInfo(soup, yearList, BPMList, keyList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
                else:
                    tk.Label(leftComponentFrame, text="Track failed string comparison test, likely a remix or a different track entirely", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
                    refresh(webScrapingWindow)
            else: yearList, BPMList, keyList, genreList, URLList, imageCounter, webScrapingLeftPane, webScrapingRightPane = extractInfo(soup, yearList, BPMList, keyList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
        else:
            tk.Label(leftComponentFrame, text="Track failed runtime comparison test", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
            refresh(webScrapingWindow)
    else: tk.Label(leftComponentFrame, text="Track failed due to dead link or territory restriction", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
    return yearList, BPMList, keyList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane

#extract year, BPM, key, and genre
def extractInfo(soup, yearList, BPMList, keyList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter):
    for link in soup.find_all('ul', class_="interior-track-content-list"):
        # extract release date
        if "Release_Date" in options["Selected Tags (L)"]:
            release = link.find('li', class_="interior-track-content-item interior-track-released")
            release = release.find('span', class_="value").get_text()
            tk.Label(leftComponentFrame, text="Year: " + str(release[0:4]), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
            refresh(webScrapingWindow)
            yearList.append(int(release[0:4]))
        # extract BPM
        if "BPM" in options["Selected Tags (L)"]:
            BPM = link.find('li', class_="interior-track-content-item interior-track-bpm")
            BPM = BPM.find('span', class_="value").get_text()
            tk.Label(leftComponentFrame, text="BPM: " + str(BPM), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
            refresh(webScrapingWindow)
            BPMList.append(int(BPM))
        # extract key
        if "Key" in options["Selected Tags (L)"]:
            key = link.find('li', class_="interior-track-content-item interior-track-key")
            key = key.find('span', class_="value").get_text()
            tk.Label(leftComponentFrame, text="Key: " + str(key), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
            refresh(webScrapingWindow)
            keyList.append(key)
        # extract genre
        if "Genre" in options["Selected Tags (L)"]:
            genre = link.find('li', class_="interior-track-content-item interior-track-genre")
            if genre.find('span', class_="value sep"):
                firstGenre = genre.find('span', class_="value")
                firstGenre = firstGenre.find('a').get_text()
                secondGenre = genre.find('span', class_="value sep")
                secondGenre = secondGenre.find('a').get_text()
                tk.Label(leftComponentFrame, text="Genre: " + str(firstGenre) + ' | ' + str(secondGenre), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
                refresh(webScrapingWindow)
                genreList.append(firstGenre)
                genreList.append(secondGenre)
            else:
                genre = genre.find('span', class_="value")
                genre = genre.find('a').get_text()
                tk.Label(leftComponentFrame, text="Genre: " + str(genre), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
                refresh(webScrapingWindow)
                genreList.append(genre)
    webScrapingLeftPane[webScrapingPage] = leftComponentFrame
    #extract image
    if options["Extract Image from Website (B)"].get() == True:
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
            refresh(webScrapingWindow)
            imageCounter+=1
            webScrapingRightPane[webScrapingPage] = rightComponentFrame
            # perform image scraping if enabled in options
            if options["Reverse Image Search (B)"].get() == True:
                imageCounter, URLList = reverseImageSearch(link, headers, webScrapingWindow, imageCounter, URLList, options)
    return yearList, BPMList, keyList, genreList, URLList, imageCounter, webScrapingLeftPane, webScrapingRightPane

def refresh(webScrapingWindow):
    webScrapingWindow.update()




