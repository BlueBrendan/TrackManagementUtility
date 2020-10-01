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
from web_scrapers.sendRequest import sendRequest
from web_scrapers.webScrapingWindowControl import rerenderControls

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

def discogsSearch(title, var, yearList, genreList, URLList, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, options, imageCounter):
    # THIRD QUERY - DISCOGS
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
    if len(var) > 60: tk.Label(searchFrame, text="\nSearching Discogs for " + str(var)[0:59] + "...", font=("Proxima Nova Rg", 13), fg="white", bg=bg, anchor='w').pack(side="left", padx=(10, 0))
    else: tk.Label(searchFrame, text="\nSearching Discogs for " + str(var), font=("Proxima Nova Rg", 13), fg="white", bg=bg, anchor='w').pack(side="left", padx=(10, 0))
    # page counter and navigation buttons
    rerenderControls(pageFrame, webScrapingPage)
    componentFrame = tk.Frame(webScrapingWindow, bg=bg)
    componentFrame.pack(fill=X, pady=(10, 0))
    leftComponentFrame, rightComponentFrame = resetLeftRightFrames(componentFrame)

    refresh(webScrapingWindow)
    url = "https://www.google.co.in/search?q=" + search + " Discogs"
    soup = sendRequest(url, headers, webScrapingWindow, leftComponentFrame)
    if soup != False:
        #result includes link and description
        for result in soup.find_all('div', class_="ZINbbc xpd O9g5cc uUPGi"):
            if "www.discogs.com" in str(result.find('a').get('href')).lower().split('&')[0]:
                searchTitle = title
                if ' (' in title and ')' in title:
                    searchTitle = title[:title.index(' (')]
                if searchTitle.lower() in str(result).lower():
                    yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = searchQuery(title, result, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, yearList, genreList, URLList, leftComponentFrame, rightComponentFrame, componentFrame, titleVariations, options, imageCounter)
                else:
                    for variation in titleVariations:
                        variation = variation.replace('-', ' ')
                        if variation.lower() in str(result).lower():
                            yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage = searchQuery(title, result, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, yearList, genreList, URLList, leftComponentFrame, rightComponentFrame, componentFrame, titleVariations, options, imageCounter)
    return yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame

def searchQuery(title, result, headers, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, pageFrame, yearList, genreList, URLList, leftComponentFrame, rightComponentFrame, componentFrame, titleVariations, options, imageCounter):
    widgetList = allWidgets(componentFrame)
    for item in widgetList: item.pack_forget()
    widgetList = allWidgets(pageFrame)
    for item in widgetList: item.pack_forget()
    webScrapingPage+=1
    leftComponentFrame, rightComponentFrame = resetLeftRightFrames(componentFrame)
    # page counter and navigation buttons
    rerenderControls(pageFrame, webScrapingPage)
    link = str(result.find('a').get('href')).split('&')[0].split('=')[1]
    label = tk.Label(leftComponentFrame, text="\n" + str(link), cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor="w")
    label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
    label.pack(padx=(10, 0), pady=(0, 25))
    webScrapingLeftPane[webScrapingPage] = leftComponentFrame
    # assume match will fail and no image will be found
    webScrapingRightPane[webScrapingPage] = "NA"
    webScrapingLinks[webScrapingPage] = link
    refresh(webScrapingWindow)

    soup = sendRequest(link, headers, webScrapingWindow, leftComponentFrame)
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
                        yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane = discogsRelease(soup, yearList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
                        break
                    else:
                        for title in titleVariations:
                            title = title.replace('-', ' ')
                            mismatch = compareTokens(title, name)
                            if mismatch == False:
                                yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane = discogsRelease(soup, yearList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
                                break
            #title format
            elif link.find('td', class_="track tracklist_track_title")!=None:
                for temp in link.find_all('td', class_="track tracklist_track_title"):
                    name = temp.find('span', class_="tracklist_track_title").get_text()
                    if temp.find('span', class_="tracklist_extra_artist_span") != None:
                        remix = temp.find('span', class_="tracklist_extra_artist_span")
                        remix = remix.find('a').get_text()
                        if remix.lower() not in name.lower() and '(' in name:
                            name = name[0:name.index('(') + 1] + remix + " " + name[name.index("(") + 1:]
                    # check if title and name are exact matches
                    if title.lower() == name.lower():
                        yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane = discogsRelease(soup, yearList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
                        break
                    else:
                        for title in titleVariations:
                            title = title.replace('-', ' ')
                            mismatch = compareTokens(title, name)
                            if mismatch == False:
                                yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane = discogsRelease(soup, yearList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter)
                                break
    return yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage

def discogsRelease(soup, yearList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingPage, options, imageCounter):
    genre = ''
    for link in soup.find_all('div', class_="content"):
        for link in link.find_all('a'):
            header = link['href']
            if "year" in header:
                # Discog releases tend to have more credible tags, so each instance counts twice
                tk.Label(leftComponentFrame, text="Year: " + str(link.get_text().strip()), font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor="w").pack(padx=(10, 0), pady=(5, 0))
                if " " in link.get_text().strip():
                    yearList.append(int(link.get_text().strip()[-4:]))
                    yearList.append(int(link.get_text().strip()[-4:]))
                else:
                    yearList.append(int(link.get_text().strip()))
                    yearList.append(int(link.get_text().strip()))
            elif "style" in header:
                #first genre
                if genre == '': genre = str(link.get_text()).strip()
                #multiple genres
                else: genre += ", " + str(link.get_text()).strip()
                genreList.append(link.get_text().strip())
    if len(genre) >= 75: tk.Label(leftComponentFrame, text="Genre: " + genre[0:74] + "...", font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor="w").pack(padx=(10, 0), pady=(5, 0))
    else: tk.Label(leftComponentFrame, text="Genre: " + genre, font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor="w").pack(padx=(10, 0), pady=(5, 0))
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
        fileImage = tk.Label(rightComponentFrame, image=photo)
        fileImage.image = photo
        fileImage.pack(padx=(70, 0), anchor="e")
        imageCounter+=1
        refresh(webScrapingWindow)
        webScrapingRightPane[webScrapingPage] = rightComponentFrame
        if options["Reverse Image Search (B)"].get() == True:
            imageCounter, URLList = reverseImageSearch(link, headers, webScrapingWindow, imageCounter, URLList, options)
    return yearList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane

def refresh(webScrapingWindow):
    webScrapingWindow.update()
    webScrapingWindow.attributes("-topmost", 1)
    webScrapingWindow.attributes("-topmost", 0)