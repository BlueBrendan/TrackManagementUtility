import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter.tix import *
from PIL import Image, ImageTk
import webbrowser
import getpass
import time
import random

#import methods
from track_scraping.compareTokens import compareTokens
from track_scraping.reverseImageSearch import reverseImageSearch
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

def junodownloadSearch(var, yearList, BPMList, genreList, URLList, artistVariations, titleVariations, headers, search, window, audio, options, imageCounter):
    #FIRST QUERY - JUNO DOWNLOAD
    widgetList = allWidgets(window)
    for item in widgetList:
        item.pack_forget()

    tk.Label(window, text="\nSearching Juno Download for " + str(var), font=("Proxima Nova Rg", 13), fg="white", bg=bg, anchor='w').pack(padx=(10, 0), pady=(10, 10), fill=X)
    componentFrame = tk.Frame(window, bg=bg)
    componentFrame.pack(fill=X, pady=(10, 0))
    #component for text
    leftComponentFrame = tk.Frame(componentFrame, bg=bg)
    leftComponentFrame.pack(side="left", fill=Y)
    #component for image
    rightComponentFrame = tk.Frame(componentFrame, bg=bg)
    rightComponentFrame.pack(side="left", fill=Y)

    window.update()
    window.lift()
    url = "https://www.google.co.in/search?q=" + search + " Junodownload"
    soup = sendRequest(url, headers, leftComponentFrame, window)
    if soup!=False:
        for result in soup.find_all('div', class_="ZINbbc xpd O9g5cc uUPGi"):
            if 'junodownload.com' and 'products' in result.find('a').get('href').split('&')[0].lower():
                for variation in titleVariations:
                    variation = variation.replace('-', ' ')
                    if variation.lower() in str(result).lower():
                        link = result.find('a').get('href').split('&')[0][7:]
                        #clear component frames of existing content
                        widgetList = allWidgets(leftComponentFrame)
                        for item in widgetList:
                            item.pack_forget()
                        widgetList = allWidgets(rightComponentFrame)
                        for item in widgetList:
                            item.pack_forget()

                        label = tk.Label(leftComponentFrame, text="\n" + str(link), cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                        label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
                        label.pack(padx=(10, 0))
                        # label.pack(anchor='w')
                        # label.bind("<Button-1>", lambda e: webbrowser.open_new(link))
                        window.update()
                        soup = sendRequest(link, headers, leftComponentFrame, window)
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
                                mismatch = True
                                for title in titleVariations:
                                    title = title.replace('-', ' ')
                                    mismatch = compareTokens(title, trackTitle)
                                    if not mismatch:break
                                if mismatch == False:
                                #check runtime to ensure track is correct
                                    runtime = link.find('div', class_="col-1 d-none d-lg-block text-center").get_text()
                                    if compareRuntime(runtime, audio) == False:
                                        for value in link.find_all('div', class_="col-1 d-none d-lg-block text-center"):
                                            if ":" not in value.get_text() and value.get_text()!='\xa0':
                                                BPM = value.get_text()
                                                tk.Label(leftComponentFrame, text="BPM: " + str(BPM), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(30, 0), anchor="w")
                                                window.update()
                                                BPMList.append(int(BPM))
                                                BPMList.append(int(BPM))
                                        #only push release and genre from header if title is found in tracklist
                                        # scrape release date and genre
                                        for link in soup.select('div[class=mb-3]'):
                                            release = link.find("span", itemprop="datePublished").get_text()
                                            tk.Label(leftComponentFrame, text="Year: " + str(release), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
                                            yearList.append(int(release[-4:]))
                                            genre = link.find("a").get_text()
                                            tk.Label(leftComponentFrame, text="Genre: " + str(genre), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
                                            genreList.append(genre)
                                            # extract image
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
                                            fileImage.pack(padx=(70, 0))
                                            window.update()
                                            imageCounter += 1
                                            # perform image scraping if enabled in options
                                            if options["Reverse Image Search (B)"].get() == True:
                                                imageCounter, URLList = reverseImageSearch(link, headers, window, imageCounter, URLList, options)
                                            time.sleep(1)
    return yearList, BPMList, genreList, imageCounter, URLList

def sendRequest(url, headers, frame, window):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return soup
    except requests.exceptions.ConnectionError:
        Label(frame, text="Connection refused", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), anchor='w')
        window.update()
        # generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return False
