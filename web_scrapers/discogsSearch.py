import tkinter as tk
from tkinter.tix import *
import requests
from PIL import Image, ImageTk
import getpass
import webbrowser

#import methods
from track_scraping.compareTokens import compareTokens
from track_scraping.reverseImageSearch import reverseImageSearch
from web_scrapers.webScrapingWindowControl import resetLeftRightFrames
from web_scrapers.sendRequest import prepareRequest
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

def discogsSearch(title, var, yearList, genreList, URLList, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, labelFrame, searchFrame, pageFrame, componentFrame, audio, options, imageCounter):
    # THIRD QUERY - DISCOGS
    widgetList = allWidgets(searchFrame)
    for item in widgetList: item.pack_forget()
    if len(var) > 60: tk.Label(searchFrame, text="\nSearching Discogs for " + str(var)[0:59] + "...", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="left", padx=(10, 0), anchor='w')
    else: tk.Label(searchFrame, text="\nSearching Discogs for " + str(var), font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="left", padx=(10, 0), anchor='w')
    leftComponentFrame, rightComponentFrame = resetLeftRightFrames(componentFrame)
    refresh(webScrapingWindow)
    url = "https://www.google.co.in/search?q=" + search + " Discogs"
    soup = prepareRequest(url, headers, webScrapingWindow, leftComponentFrame)
    if soup != False:
        #result includes link and description
        for result in soup.find_all('div', class_="ZINbbc xpd O9g5cc uUPGi"):
            if "www.discogs.com" in str(result.find('a').get('href')).lower().split('&')[0]:
                searchTitle = title
                if ' (' in title and ')' in title: searchTitle = title[:title.index(' (')]
                if searchTitle.lower() in str(result).lower(): yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = searchQuery(title, result, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, yearList, genreList, URLList, leftComponentFrame, rightComponentFrame, componentFrame, titleVariations, audio, options, imageCounter)
                else:
                    for variation in titleVariations:
                        variation = variation.replace('-', ' ')
                        if variation.lower() in str(result).lower(): yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = searchQuery(title, result, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, yearList, genreList, URLList, leftComponentFrame, rightComponentFrame, componentFrame, titleVariations, audio, options, imageCounter)
    return yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame

def searchQuery(title, result, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, yearList, genreList, URLList, leftComponentFrame, rightComponentFrame, componentFrame, titleVariations, audio, options, imageCounter):
    link = str(result.find('a').get('href')).split('&')[0].split('=')[1]
    soup = prepareRequest(link, headers, webScrapingWindow, leftComponentFrame)
    if soup != False:
        # first check if the title is in the tracklist, push data if it is
        link = soup.find('table', class_="playlist")
        # handle 404 links
        if link != None:
            #artist + title format
            if link.find('td', class_="track tracklist_track_title mini_playlist_track_has_artist")!=None:
                for temp in link.find_all('td', class_="track tracklist_track_title mini_playlist_track_has_artist"):
                    name = temp.find('span', class_="tracklist_track_title").get_text()
                    #extra tags attached
                    for tag in temp.find_all('span', class_="tracklist_extra_artist_span"):
                        if 'Remix' in tag.get_text():
                            remix = tag.find('a').get_text()
                            if remix.lower() not in name.lower() and '(' in name:
                                name = name[0:name.index('(') + 1] + remix + " " + name[name.index("(") + 1:]
                    if title.lower() == name.lower():
                        yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = discogsRelease(soup, result, yearList, genreList, URLList, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, webScrapingLinks, pageFrame, componentFrame, options, imageCounter, audio)
                        break
                    else:
                        for title in titleVariations:
                            title = title.replace('-', ' ')
                            mismatch = compareTokens(title, name)
                            if mismatch == False:
                                yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = discogsRelease(soup, result, yearList, genreList, URLList, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, webScrapingLinks, pageFrame, componentFrame, options, imageCounter, audio)
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
                        if remix.lower() not in name.lower() and '(' in name:
                            name = name[0:name.index('(') + 1] + remix + " " + name[name.index("(") + 1:]
                    # check if title and name are exact matches
                    if title.lower() == name.lower() and not compareRuntime(runtime, audio):
                        yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = discogsRelease(soup, result, yearList, genreList, URLList, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, webScrapingLinks, pageFrame, componentFrame, options, imageCounter, audio)
                        break
                    else:
                        for title in titleVariations:
                            title = title.replace('-', ' ')
                            mismatch = compareTokens(title, name)
                            if mismatch == False and not compareRuntime(runtime, audio):
                                yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = discogsRelease(soup, result, yearList, genreList, URLList, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, webScrapingLinks, pageFrame, componentFrame, options, imageCounter, audio)
                                break
    return yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage

def discogsRelease(soup, result, yearList, genreList, URLList, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, webScrapingLinks, pageFrame, componentFrame, options, imageCounter, audio):
    widgetList = allWidgets(componentFrame)
    for item in widgetList: item.pack_forget()
    widgetList = allWidgets(pageFrame)
    for item in widgetList: item.pack_forget()
    webScrapingPage += 1
    leftComponentFrame, rightComponentFrame = resetLeftRightFrames(componentFrame)
    # page counter and navigation buttons
    rerenderControls(pageFrame, webScrapingPage)
    link = str(result.find('a').get('href')).split('&')[0].split('=')[1]
    label = tk.Label(leftComponentFrame, text="\n" + str(link), cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
    label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
    label.pack(padx=(10, 0), pady=(0, 25), anchor="w")
    webScrapingLeftPane[webScrapingPage] = leftComponentFrame
    webScrapingRightPane[webScrapingPage] = "NA"
    webScrapingLinks[webScrapingPage] = link
    refresh(webScrapingWindow)

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
                    yearList.append(int(link.get_text().strip()[-4:]))
                    yearList.append(int(link.get_text().strip()[-4:]))
                else:
                    yearList.append(int(link.get_text().strip()))
                    yearList.append(int(link.get_text().strip()))
            # extract genre
            elif "style" in header and "Genre" in options["Selected Tags (L)"]:
                genre = str(link.get_text()).strip()
                scrapedGenreList.append(genre)
                genreList.append(genre)
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
        with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg", "wb") as file:
            file.write(requests.get(link, headers=headers).content)
        URLList.append(link)
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
        if options["Reverse Image Search (B)"].get() == True: imageCounter, URLList = reverseImageSearch(link, headers, webScrapingWindow, imageCounter, URLList, options)
    else:
        tk.Label(leftComponentFrame, text="Track failed runtime comparison test", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
        webScrapingLeftPane[webScrapingPage] = leftComponentFrame
        refresh(webScrapingWindow)
    return yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage

def refresh(webScrapingWindow):
    webScrapingWindow.update()