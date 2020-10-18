import tkinter as tk
from tkinter.tix import *
import requests
import getpass
from PIL import Image, ImageTk
from skimage.metrics import structural_similarity
from skimage.transform import resize
import matplotlib.pyplot as plt
import webbrowser

#import methods
from track_scraping.compareTokens import compareTokens
from track_scraping.reverseImageSearch import reverseImageSearch
from web_scrapers.webScrapingWindowControl import rerenderControls
from web_scrapers.webScrapingWindowControl import resetLeftRightFrames
from web_scrapers.sendRequest import prepareRequest
from web_scrapers.compareRuntime import compareRuntime
from track_scraping.conflictPopup.commonOperations import allWidgets

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

def beatportSearch(filename, track, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, labelFrame, searchFrame, pageFrame, componentFrame, audio, options, imageCounter):
    #SECOND QUERY - BEATPORT
    widgetList = allWidgets(searchFrame)
    for item in widgetList: item.pack_forget()
    if len(filename) > 60: tk.Label(searchFrame, text="\nSearching Beatport for " + str(filename)[0:59] + "...", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="left", padx=(10, 0), anchor='w')
    else: tk.Label(searchFrame, text="\nSearching Beatport for " + str(filename), font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="left", padx=(10, 0), anchor='w')

    leftComponentFrame, rightComponentFrame = resetLeftRightFrames(componentFrame)
    refresh(webScrapingWindow)
    url = "https://www.google.co.in/search?q=" + search + " Beatport"
    soup = prepareRequest(url, headers, webScrapingWindow, leftComponentFrame)
    if soup == False:
        Label(leftComponentFrame, text="Connection Failure", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(anchor='w')
        refresh(webScrapingWindow)
        return track, imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame
    for link in soup.find_all('a'):
        if "www.beatport.com" in link.get('href').split('&')[0]:
            content = link.find('div', class_="BNeawe vvjwJb AP7Wnd").get_text().lower()
            # all Beatport headers contain suffix "by [artistName] on Beatport"
            for i in range(4): content = content[:content.rfind(' ')]
            mismatch = True
            for variation in titleVariations:
                if variation in content:
                    mismatch = False
                    break
                else:
                    mismatch = compareTokens(variation, content)
                    if not mismatch: break
            if mismatch == False:
                link = link.get('href').split('&')[0].split('=')[1]
                if "remix" in link and "remix" in track.title.lower() or "remix" not in track.title.lower() and "remix" not in link:
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
                        if link[25:32] == "release": imageCounter, webScrapingLeftPane, webScrapingRightPane = beatportRelease(soup, titleVariations, track, headers, audio, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
                        #case 2: track
                        elif link[25:30] == "track": imageCounter, webScrapingLeftPane, webScrapingRightPane = beatportTrack(soup, track, headers, audio, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
                    else: tk.Label(leftComponentFrame, text="Track failed due to dead link or territory restriction", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
    return track, imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame

#search beatport releases, filter individual tracks
def beatportRelease(soup, titleVariations, track, headers, audio, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter):
    for link in soup.find_all('li', class_="bucket-item ec-item track"):
        # find all tracks in the release that contain the title
        link = link.find('p', class_="buk-track-title")
        if link.find('a')['href'].lower() in titleVariations:
            url = "https://www.beatport.com" + str(link.find('a')['href'])
            soup = prepareRequest(url, headers, webScrapingWindow, leftComponentFrame)
            if soup == False:
                tk.Label(leftComponentFrame, text="Connection Failure", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(anchor='w')
                refresh(webScrapingWindow)
                return track, imageCounter, webScrapingLeftPane, webScrapingRightPane
            imageCounter, webScrapingLeftPane, webScrapingRightPane = beatportTrack(soup, track, headers, audio, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
    return imageCounter, webScrapingLeftPane, webScrapingRightPane

#search beatport tracks, extract info in the event of a match
def beatportTrack(soup, track, headers, audio, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter):
    link = soup.find('div', class_="interior-track-content")
    if link is not None:
        # check runtime
        length = soup.find('li', class_="interior-track-content-item interior-track-length")
        length = length.find('span', class_="value").get_text()
        if compareRuntime(length, audio) == False:
            trackHeader = soup.find('div', class_="interior-title")
            trackName = trackHeader.find('h1').get_text()
            trackMix = trackHeader.find('h1', class_="remixed").get_text()
            if trackMix != '' and 'original' not in trackMix.lower() and '(' in track.title and ')' in track.title:
                remix = track.title[track.title.rfind('(') + 1:track.title.rfind(')')]
                if compareTokens(remix, trackMix) == False: imageCounter, webScrapingLeftPane, webScrapingRightPane = extractInfo(soup, track, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
                else:
                    tk.Label(leftComponentFrame, text="Track failed string comparison test, likely a remix or a different track entirely", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
                    refresh(webScrapingWindow)
            else: imageCounter, webScrapingLeftPane, webScrapingRightPane = extractInfo(soup, track, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
        else:
            tk.Label(leftComponentFrame, text="Track failed runtime comparison test", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
            refresh(webScrapingWindow)
    else: tk.Label(leftComponentFrame, text="Track failed due to dead link or territory restriction", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
    return imageCounter, webScrapingLeftPane, webScrapingRightPane

#extract year, BPM, key, and genre
def extractInfo(soup, track, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter):
    for link in soup.find_all('ul', class_="interior-track-content-list"):
        # extract release date
        if "Release_Date" in options["Selected Tags (L)"]:
            release = link.find('li', class_="interior-track-content-item interior-track-released")
            release = release.find('span', class_="value").get_text()
            tk.Label(leftComponentFrame, text="Year: " + str(release[0:4]), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
            refresh(webScrapingWindow)
            track.yearList.append(int(release[0:4]))
        # extract BPM
        if "BPM" in options["Selected Tags (L)"]:
            BPM = link.find('li', class_="interior-track-content-item interior-track-bpm")
            BPM = BPM.find('span', class_="value").get_text()
            tk.Label(leftComponentFrame, text="BPM: " + str(BPM), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
            refresh(webScrapingWindow)
            track.BPMList.append(int(BPM))
        # extract key
        if "Key" in options["Selected Tags (L)"]:
            key = link.find('li', class_="interior-track-content-item interior-track-key")
            key = key.find('span', class_="value").get_text()
            tk.Label(leftComponentFrame, text="Key: " + str(key), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
            refresh(webScrapingWindow)
            track.keyList.append(key)
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
                track.genreList.append(firstGenre)
                track.genreList.append(secondGenre)
            else:
                genre = genre.find('span', class_="value")
                genre = genre.find('a').get_text()
                tk.Label(leftComponentFrame, text="Genre: " + str(genre), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
                refresh(webScrapingWindow)
                track.genreList.append(genre)
    webScrapingLeftPane[webScrapingPage] = leftComponentFrame
    #extract image
    if options["Extract Image from Website (B)"].get() == True:
        link = soup.find('img', class_="interior-track-release-artwork")
        if link!=None:
            link = link['src']
            # write beatport image to drive
            with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg", "wb") as file:
                file.write(requests.get(link, headers=headers).content)
            track.URLList.append(link)
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
            if options["Reverse Image Search (B)"].get() == True and not track.stop:
                duplicate = False
                # compare image with other scraped images
                imageOne = resize(plt.imread(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter - 1) + ".jpg").astype(float), (2 ** 8, 2 ** 8))
                for i in range(imageCounter - 1):
                    imageTwo = resize(plt.imread(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg").astype(float), (2 ** 8, 2 ** 8))
                    score, diff = structural_similarity(imageOne, imageTwo, full=True, multichannel=True)
                    if score > 0.6:
                        widthOne, heightOne = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter - 1) + ".jpg").size
                        widthTwo, heightTwo = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(i) + ".jpg").size
                        if abs(widthTwo - widthOne) <= 200 and abs(heightTwo - heightTwo) <= 200: duplicate = True
                if not duplicate: imageCounter, track = reverseImageSearch(link, headers, webScrapingWindow, imageCounter, track, options)
    return imageCounter, webScrapingLeftPane, webScrapingRightPane

def refresh(webScrapingWindow):
    webScrapingWindow.update()




