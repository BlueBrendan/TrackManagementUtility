import tkinter as tk
from tkinter.tix import *
from PIL import Image, ImageTk
import requests
import webbrowser
import getpass


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

def junodownloadSearch(filename, yearList, BPMList, genreList, URLList, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, audio, options, imageCounter):
    #FIRST QUERY - JUNO DOWNLOAD
    widgetList = allWidgets(webScrapingWindow)
    for item in widgetList: item.pack_forget()
    #component for search label and page indicator
    labelFrame = tk.Frame(webScrapingWindow, bg=bg)
    labelFrame.pack(fill=X, pady=(10, 10))
    searchFrame = tk.Frame(labelFrame, bg=bg)
    searchFrame.pack(side="left")
    pageFrame = tk.Frame(labelFrame, bg=bg)
    pageFrame.pack(side="right", pady=(20, 0))
    if len(filename) > 60: tk.Label(searchFrame, text="\nSearching Juno Download for " + str(filename)[0:59] + "...", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="left", padx=(10, 0), anchor='w')
    else: tk.Label(searchFrame, text="\nSearching Juno Download for " + str(filename), font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="left", padx=(10, 0), anchor='w')
    #page counter and navigation buttons
    rerenderControls(pageFrame, webScrapingPage)
    componentFrame = tk.Frame(webScrapingWindow, bg=bg)
    componentFrame.pack(fill=X, pady=(10, 0))
    leftComponentFrame, rightComponentFrame = resetLeftRightFrames(componentFrame)
    refresh(webScrapingWindow)
    url = "https://www.google.co.in/search?q=" + search + " Junodownload"
    soup = prepareRequest(url, headers, webScrapingWindow, leftComponentFrame)
    if soup!=False:
        for result in soup.find_all('div', class_="ZINbbc xpd O9g5cc uUPGi"):
            if 'junodownload.com' and 'products' in result.find('a').get('href').split('&')[0].lower():
                for variation in titleVariations:
                    variation = variation.replace('-', ' ')
                    if variation.lower() in str(result).lower():
                        link = result.find('a').get('href').split('&')[0][7:]
                        #clear component frames of existing content
                        widgetList = allWidgets(componentFrame)
                        for item in widgetList: item.pack_forget()
                        widgetList = allWidgets(pageFrame)
                        for item in widgetList: item.pack_forget()
                        #increment web scraping page and rerender count
                        webScrapingPage+=1
                        leftComponentFrame, rightComponentFrame = resetLeftRightFrames(componentFrame)
                        rerenderControls(pageFrame, webScrapingPage)
                        if len(link) >= 75: label = tk.Label(leftComponentFrame, text="\n" + str(link)[0:74] + "...", cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                        else: label = tk.Label(leftComponentFrame, text="\n" + str(link), cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                        label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
                        label.pack(padx=(10, 0), pady=(0, 25), anchor='w')
                        #update left component history frame
                        webScrapingLeftPane[webScrapingPage] = leftComponentFrame
                        # assume match will fail and no image will be found
                        webScrapingRightPane[webScrapingPage] = "NA"
                        #update link
                        webScrapingLinks[webScrapingPage] = link
                        refresh(webScrapingWindow)
                        soup = prepareRequest(link, headers, webScrapingWindow, leftComponentFrame)
                        if soup!=False:
                            #scrape release date and genre
                            for link in soup.find_all('div',class_="row gutters-sm align-items-center product-tracklist-track"):
                                name = link.find('span').get_text()
                                if ' - ' in name:
                                    trackArtist = link.find('span').get_text().split(' - ')[0]
                                    trackTitle = link.find('span').get_text().split(' - ')[1]
                                else:
                                    trackArtist = ''
                                    trackTitle = link.find('span').get_text()
                                if not compareTokens(variation, trackTitle):
                                    #check runtime to ensure track is correct
                                    runtime = link.find('div', class_="col-1 d-none d-lg-block text-center").get_text()
                                    if compareRuntime(runtime, audio) == False:
                                        for value in link.find_all('div', class_="col-1 d-none d-lg-block text-center"):
                                            # extract BPM
                                            if ":" not in value.get_text() and value.get_text()!='\xa0' and "BPM" in options["Selected Tags (L)"]:
                                                BPM = value.get_text()
                                                tk.Label(leftComponentFrame, text="BPM: " + str(BPM), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
                                                webScrapingLeftPane[webScrapingPage] = leftComponentFrame
                                                refresh(webScrapingWindow)
                                                BPMList.append(int(BPM))
                                                BPMList.append(int(BPM))
                                        #only push release and genre from header if title is found in tracklist
                                        for link in soup.select('div[class=mb-3]'):
                                            # extract release date
                                            if "Release_Date" in options["Selected Tags (L)"]:
                                                release = link.find("span", itemprop="datePublished").get_text()
                                                tk.Label(leftComponentFrame, text="Year: " + str(release), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
                                                yearList.append(int(release[-4:]))
                                            # extract genre
                                            if "Genre" in options["Selected Tags (L)"]:
                                                genre = link.find("a").get_text()
                                                tk.Label(leftComponentFrame, text="Genre: " + str(genre), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
                                                genreList.append(genre)
                                            webScrapingLeftPane[webScrapingPage] = leftComponentFrame
                                        # extract image
                                        if options["Extract Image from Website (B)"].get() == True:
                                            link = soup.find('div', class_="jw-page")
                                            link = link.find('img').get('data-src-full')
                                            # write junodownload image to drive
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
                                            # perform image scraping if enabled in options
                                            if options["Reverse Image Search (B)"].get() == True: imageCounter, URLList = reverseImageSearch(link, headers, webScrapingWindow, imageCounter, URLList, options)
                                    else:
                                        tk.Label(leftComponentFrame, text="Track failed runtime comparison test", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
                                        webScrapingLeftPane[webScrapingPage] = leftComponentFrame
                                        refresh(webScrapingWindow)
    return yearList, BPMList, genreList, imageCounter, URLList, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame

def refresh(webScrapingWindow):
    webScrapingWindow.update()
