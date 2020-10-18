import tkinter as tk
from tkinter.tix import *
import requests
from PIL import Image, ImageTk
from skimage.metrics import structural_similarity
from skimage.transform import resize
import matplotlib.pyplot as plt
import getpass
import webbrowser

#import methods
from track_scraping.compareTokens import compareTokens
from track_scraping.reverseImageSearch import reverseImageSearch
from web_scrapers.webScrapingWindowControl import resetLeftRightFrames
from web_scrapers.sendRequest import prepareRequest
from web_scrapers.webScrapingWindowControl import rerenderControls
from web_scrapers.compareRuntime import compareRuntime
from track_scraping.conflictPopup.commonOperations import allWidgets

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

def discogsSearch(filename, track, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, labelFrame, searchFrame, pageFrame, componentFrame, audio, options, imageCounter):
    # THIRD QUERY - DISCOGS
    widgetList = allWidgets(searchFrame)
    for item in widgetList: item.pack_forget()
    if len(filename) > 60: tk.Label(searchFrame, text="\nSearching Discogs for " + str(filename)[0:59] + "...", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="left", padx=(10, 0), anchor='w')
    else: tk.Label(searchFrame, text="\nSearching Discogs for " + str(filename), font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="left", padx=(10, 0), anchor='w')
    leftComponentFrame, rightComponentFrame = resetLeftRightFrames(componentFrame)
    refresh(webScrapingWindow)
    url = "https://www.google.co.in/search?q=" + search + " Discogs"
    soup = prepareRequest(url, headers, webScrapingWindow, leftComponentFrame)
    if soup != False:
        #result includes link and description
        for result in soup.find_all('div', class_="ZINbbc xpd O9g5cc uUPGi"):
            if "www.discogs.com" in str(result.find('a').get('href')).lower().split('&')[0]:
                searchTitle = track.title
                if ' (' in track.title and ')' in track.title: searchTitle = track.title[:track.title.index(' (')]
                if searchTitle.lower() in str(result).lower(): imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = searchQuery(track, result, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, leftComponentFrame, rightComponentFrame, componentFrame, titleVariations, audio, options, imageCounter)
                else:
                    for variation in titleVariations:
                        variation = variation.replace('-', ' ')
                        if variation.lower() in str(result).lower(): imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = searchQuery(track, result, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, leftComponentFrame, rightComponentFrame, componentFrame, titleVariations, audio, options, imageCounter)
    return track, imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame

def searchQuery(track, result, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, leftComponentFrame, rightComponentFrame, componentFrame, titleVariations, audio, options, imageCounter):
    link = str(result.find('a').get('href')).split('&')[0].split('=')[1]
    soup = prepareRequest(link, headers, webScrapingWindow, leftComponentFrame)
    if soup != False:
        # first check if the title is in the tracklist, push data if it is
        link = soup.find('table', class_="playlist")
        # handle 404 links
        if link != None:
            # post link to web scraping window
            widgetList = allWidgets(componentFrame)
            for item in widgetList: item.pack_forget()
            widgetList = allWidgets(pageFrame)
            for item in widgetList: item.pack_forget()
            webScrapingPage += 1
            leftComponentFrame, rightComponentFrame = resetLeftRightFrames(componentFrame)
            # page counter and navigation buttons
            rerenderControls(pageFrame, webScrapingPage)
            weblink = str(result.find('a').get('href')).split('&')[0].split('=')[1]
            label = tk.Label(leftComponentFrame, text="\n" + str(weblink), cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
            label.bind("<Button-1>", lambda e, link=weblink: webbrowser.open_new(link))
            label.pack(padx=(10, 0), pady=(0, 25), anchor="w")
            webScrapingLeftPane[webScrapingPage] = leftComponentFrame
            webScrapingRightPane[webScrapingPage] = "NA"
            webScrapingLinks[webScrapingPage] = weblink
            refresh(webScrapingWindow)
            finalMatch = False

            #artist + title format
            if link.find('td', class_="track tracklist_track_title mini_playlist_track_has_artist")!=None:
                for temp in link.find_all('td', class_="track tracklist_track_title mini_playlist_track_has_artist"):
                    name = temp.find('span', class_="tracklist_track_title").get_text()
                    #extra tags attached
                    for tag in temp.find_all('span', class_="tracklist_extra_artist_span"):
                        if 'Remix' in tag.get_text():
                            remix = tag.find('a').get_text()
                            if remix.lower() not in name.lower() and '(' in name: name = name[0:name.index('(') + 1] + remix + " " + name[name.index("(") + 1:]
                    if track.title.lower() == name.lower():
                        finalMatch = True
                        imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = discogsRelease(soup, track, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, webScrapingLinks, leftComponentFrame, rightComponentFrame, options, imageCounter)
                        break
                    else:
                        for title in titleVariations:
                            title = title.replace('-', ' ')
                            mismatch = compareTokens(title, name)
                            if mismatch == False:
                                finalMatch = True
                                imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = discogsRelease(soup, track, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, webScrapingLinks, leftComponentFrame, rightComponentFrame, options, imageCounter)
                                break
            #title format
            elif link.find('td', class_="track tracklist_track_title")!=None:
                tracks = link.find_all('td', class_="track tracklist_track_title")
                runtimes = link.find_all('td', class_="tracklist_track_duration")
                for i in range(len(tracks)):
                    name = tracks[i].find('span', class_="tracklist_track_title").get_text()
                    runtime = runtimes[i].find('span').get_text()
                    if tracks[i].find('span', class_="tracklist_extra_artist_span") != None:
                        remix = tracks[i].find('span', class_="tracklist_extra_artist_span")
                        remix = remix.find('a').get_text()
                        if remix.lower() not in name.lower() and '(' in name: name = name[0:name.index('(') + 1] + remix + " " + name[name.index("(") + 1:]
                    # check if title and name are exact matches
                    if track.title.lower() == name.lower() and not compareRuntime(runtime, audio):
                        finalMatch = True
                        imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = discogsRelease(soup, track, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, webScrapingLinks, leftComponentFrame, rightComponentFrame, options, imageCounter)
                        break
                    else:
                        for title in titleVariations:
                            title = title.replace('-', ' ')
                            mismatch = compareTokens(title, name)
                            if mismatch == False and not compareRuntime(runtime, audio):
                                finalMatch = True
                                imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = discogsRelease(soup, track, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, webScrapingLinks, leftComponentFrame, rightComponentFrame, options, imageCounter)
                                break
            if not finalMatch:
                tk.Label(leftComponentFrame, text="Track did not match with any of the listings", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
                refresh(webScrapingWindow)
    return imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage

def discogsRelease(soup, track, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, webScrapingLinks, leftComponentFrame, rightComponentFrame, options, imageCounter):
    # in case of multiple genres
    scrapedGenreList = []
    for link in soup.find_all('div', class_="content"):
        for link in link.find_all('a'):
            header = link['href']
            # extract release date
            if "year" in header and "Release_Date" in options["Selected Tags (L)"]:
                # Discogs releases tend to have more credible tags, so each instance counts twice
                tk.Label(leftComponentFrame, text="Year: " + str(link.get_text().strip()), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
                if " " in link.get_text().strip():
                    track.yearList.append(int(link.get_text().strip()[-4:]))
                    track.yearList.append(int(link.get_text().strip()[-4:]))
                else:
                    track.yearList.append(int(link.get_text().strip()))
                    track.yearList.append(int(link.get_text().strip()))
            # extract genre
            elif "style" in header and "Genre" in options["Selected Tags (L)"]:
                genre = str(link.get_text()).strip()
                scrapedGenreList.append(genre)
                track.genreList.append(genre)
    genre = ', '.join(scrapedGenreList)
    if len(genre) >= 75: tk.Label(leftComponentFrame, text="Genre: " + genre[0:74] + "...", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
    else: tk.Label(leftComponentFrame, text="Genre: " + genre, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
    webScrapingLeftPane[webScrapingPage] = leftComponentFrame
    refresh(webScrapingWindow)
    image = soup.find('div', class_="image_gallery image_gallery_large")['data-images']
    # extract image
    if "full" in image and ".jpg" in image and options["Extract Image from Website (B)"].get() == True:
        link = image[image.index('full": ')+8:image.index(".jpg", image.index("full"))+4]
        # check
        if link[len(link)-5:len(link)-4]!='g': link = link + '.jpg'
        # write discogs image to drive
        with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg", "wb") as file: file.write(requests.get(link, headers=headers).content)
        track.URLList.append(link)
        # load file icon
        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg")
        fileImageImport = fileImageImport.resize((180, 180), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(fileImageImport)
        fileImage = tk.Label(rightComponentFrame, image=photo, bg=bg)
        fileImage.image = photo
        fileImage.pack(padx=(0, 100), anchor="e")
        imageCounter += 1
        refresh(webScrapingWindow)
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
    else:
        tk.Label(leftComponentFrame, text="Track failed runtime comparison test", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
        webScrapingLeftPane[webScrapingPage] = leftComponentFrame
        refresh(webScrapingWindow)
    return imageCounter, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage

def refresh(webScrapingWindow):
    webScrapingWindow.update()