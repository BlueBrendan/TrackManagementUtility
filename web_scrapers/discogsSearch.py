import tkinter as tk
from tkinter.tix import *
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import getpass
import webbrowser
import time
import random

#import methods
from track_scraping.compareTokens import compareTokens
from track_scraping.reverseImageSearch import reverseImageSearch

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

def discogsSearch(title, var, yearList, genreList, URLList, artistVariations, titleVariations, headers, search, window, options, imageCounter):
    # THIRD QUERY - DISCOGS
    widgetList = allWidgets(window)
    for item in widgetList:
        item.pack_forget()

    tk.Label(window, text="\nSearching Discogs for " + str(var), font=("Proxima Nova Rg", 13), fg="white", bg=bg, anchor="w").pack(padx=(10, 0), pady=(10, 10), fill=X)
    componentFrame = tk.Frame(window, bg=bg)
    componentFrame.pack(fill=X, pady=(10, 0))
    # component for text
    leftComponentFrame = tk.Frame(componentFrame, bg=bg)
    leftComponentFrame.pack(side="left", fill=Y)
    # component for image
    rightComponentFrame = tk.Frame(componentFrame, bg=bg)
    rightComponentFrame.pack(side="left", fill=Y)

    window.update()
    window.lift()
    url = "https://www.google.co.in/search?q=" + search + " Discogs"
    soup = sendRequest(url, headers, window)
    if soup != False:
        #result includes link and description
        for result in soup.find_all('div', class_="ZINbbc xpd O9g5cc uUPGi"):
            if "www.discogs.com" in str(result.find('a').get('href')).lower().split('&')[0]:
                searchTitle = title
                if ' (' in title and ')' in title:
                    searchTitle = title[:title.index(' (')]
                if searchTitle.lower() in str(result).lower():
                    yearList, genreList, imageCounter, URLList = searchQuery(title, result, headers, window, yearList, genreList, URLList, leftComponentFrame, rightComponentFrame, titleVariations, options, imageCounter)
                else:
                    for variation in titleVariations:
                        variation = variation.replace('-', ' ')
                        if variation.lower() in str(result).lower():
                            yearList, genreList, imageCounter, URLList = searchQuery(title, result, headers, window, yearList, genreList, URLList, leftComponentFrame, rightComponentFrame, titleVariations, options, imageCounter)
    return yearList, genreList, imageCounter, URLList

def searchQuery(title, result, headers, window, yearList, genreList, URLList, leftComponentFrame, rightComponentFrame, titleVariations, options, imageCounter):
    widgetList = allWidgets(leftComponentFrame)
    for item in widgetList:
        item.pack_forget()
    leftComponentFrame.pack(side="left", fill=Y)
    for item in widgetList:
        item.pack_forget()

    link = str(result.find('a').get('href')).split('&')[0].split('=')[1]
    label = tk.Label(leftComponentFrame, text="\n" + str(link), cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
    label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
    label.pack(padx=(10, 0), anchor="w")
    window.update()
    soup = sendRequest(link, headers, window)
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
                        yearList, genreList, imageCounter, URLList = discogsRelease(soup, yearList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, window, options, imageCounter)
                        break
                    else:
                        for title in titleVariations:
                            title = title.replace('-', ' ')
                            mismatch = compareTokens(title, name)
                            if mismatch == False:
                                yearList, genreList, imageCounter, URLList = discogsRelease(soup, yearList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, window, options, imageCounter)
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
                        yearList, genreList, imageCounter, URLList = discogsRelease(soup, yearList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, window, options, imageCounter)
                        break
                    else:
                        for title in titleVariations:
                            title = title.replace('-', ' ')
                            mismatch = compareTokens(title, name)
                            if mismatch == False:
                                yearList, genreList, imageCounter, URLList = discogsRelease(soup, yearList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, window, options, imageCounter)
                                break
    return yearList, genreList, imageCounter, URLList

def discogsRelease(soup, yearList, genreList, URLList, headers, leftComponentFrame, rightComponentFrame, window, options, imageCounter):
    genre = ''
    for link in soup.find_all('div', class_="content"):
        for link in link.find_all('a'):
            header = link['href']
            if "year" in header:
                # Discog releases tend to have more credible tags, so each instance counts twice
                tk.Label(leftComponentFrame, text="Year: " + str(link.get_text().strip()), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(30, 0), anchor="w")
                window.update()
                if " " in link.get_text().strip():
                    yearList.append(int(link.get_text().strip()[-4:]))
                    yearList.append(int(link.get_text().strip()[-4:]))
                else:
                    yearList.append(int(link.get_text().strip()))
                    yearList.append(int(link.get_text().strip()))
            elif "style" in header:
                #first genre
                if genre == '':
                    genre = str(link.get_text()).strip()
                #multiple genres
                else:
                    genre += ", " + str(link.get_text()).strip()
                genreList.append(link.get_text().strip())
    if len(genre) >= 60: tk.Label(leftComponentFrame, text="Genre: " + genre[0:59] + "...", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
    else: tk.Label(leftComponentFrame, text="Genre: " + genre, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
    window.update()
    if options["Reverse Image Search (B)"].get()==True:
        image = soup.find('div', class_="image_gallery image_gallery_large")['data-images']
        if "full" in image and ".jpg" in image:
            link = image[image.index('full": ')+8:image.index(".jpg", image.index("full"))+4]
            #check
            if link[len(link)-5:len(link)-4]!='g':
                link = link + '.jpg'
            #write discogs image to drive
            with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg", "wb") as file:
                file.write(requests.get(link, headers=headers).content)
            URLList.append(link)
            # load file icon
            fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg")
            fileImageImport = fileImageImport.resize((180, 180), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(fileImageImport)
            fileImage = tk.Label(rightComponentFrame, image=photo)
            fileImage.image = photo
            fileImage.pack(padx=(70, 0))
            window.update()
            imageCounter+=1
            imageCounter, URLList = reverseImageSearch(link, headers, window, imageCounter, URLList, options)
    return yearList, genreList, imageCounter, URLList

def sendRequest(url, headers, window):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        #generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return soup
    except requests.exceptions.ConnectionError:
        tk.Label(window, text="Connection refused").pack(anchor='w')
        # generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return False