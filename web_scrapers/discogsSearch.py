from track_scraping.compareTokens import compareTokens
import requests
from bs4 import BeautifulSoup
from tkinter import *
import getpass
import webbrowser
import time
import random

#import methods
from track_scraping.reverseImageSearch import reverseImageSearch

def discogsSearch(artist, title, var, yearList, genreList, artistVariations, titleVariations, headers, search, frame, window, options, imageCounter):
    # THIRD QUERY - DISCOGS
    Label(frame.scrollable_frame, text="\nSearching Discogs for " + str(var), font=("TkDefaultFont", 9, 'bold')).pack(anchor='w')
    window.update()
    url = "https://www.google.co.in/search?q=" + search + " Discogs"
    soup = sendRequest(url, headers, frame, window)
    if soup != False:
        #result includes link and description
        for result in soup.find_all('div', class_="ZINbbc xpd O9g5cc uUPGi"):
            if "www.discogs.com" in str(result.find('a').get('href')).lower().split('&')[0]:
                searchTitle = title
                if ' (' in title and ')' in title:
                    searchTitle = title[:title.index(' (')]
                if searchTitle.lower() in str(result).lower():
                    yearList, genreList, frame, imageCounter = searchQuery(title, result, headers, frame, window, yearList, genreList, titleVariations, options, imageCounter)
                else:
                    for variation in titleVariations:
                        variation = variation.replace('-', ' ')
                        if variation.lower() in str(result).lower():
                            yearList, genreList, frame, imageCounter = searchQuery(title, result, headers, frame, window, yearList, genreList, titleVariations, options, imageCounter)
    return yearList, genreList, imageCounter

def searchQuery(title, result, headers, frame, window, yearList, genreList, titleVariations, options, imageCounter):
    link = str(result.find('a').get('href')).split('&')[0].split('=')[1]
    label = Label(frame.scrollable_frame, text="\n" + str(link), cursor="hand2")
    label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
    label.pack(anchor='w')
    window.update()
    soup = sendRequest(link, headers, frame, window)
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
                            if remix.lower() not in name.lower():
                                if '(' in name:
                                    name = name[0:name.index('(') + 1] + remix + " " + name[name.index("(") + 1:]
                    mismatch = True
                    if title.lower() == name.lower():
                        yearList, genreList, frame, imageCounter = discogsRelease(soup, yearList, genreList, frame, window, options, imageCounter)
                        break
                    else:
                        for title in titleVariations:
                            title = title.replace('-', ' ')
                            mismatch = compareTokens(title, name)
                            if mismatch == False:
                                yearList, genreList, frame, imageCounter = discogsRelease(soup, yearList, genreList, frame, window, options, imageCounter)
                                break
                    if not mismatch:break
            #title format
            elif link.find('td', class_="track tracklist_track_title")!=None:
                for temp in link.find_all('td', class_="track tracklist_track_title"):
                    name = temp.find('span', class_="tracklist_track_title").get_text()
                    if temp.find('span', class_="tracklist_extra_artist_span") != None:
                        remix = temp.find('span', class_="tracklist_extra_artist_span")
                        remix = remix.find('a').get_text()
                        if remix.lower() not in name.lower():
                            if '(' in name:
                                name = name[0:name.index('(') + 1] + remix + " " + name[name.index("(") + 1:]
                    # check if title and name are exact matches
                    mismatch = True
                    if title.lower() == name.lower():
                        yearList, genreList, frame, imageCounter = discogsRelease(soup, yearList, genreList, frame, window, options, imageCounter)
                        break
                    else:
                        for title in titleVariations:
                            title = title.replace('-', ' ')
                            mismatch = compareTokens(title, name)
                            if mismatch == False:
                                yearList, genreList, frame, imageCounter = discogsRelease(soup, yearList, genreList, frame, window, options, imageCounter)
                                break
                    if not mismatch:break
    return yearList, genreList, frame, imageCounter

def discogsRelease(soup, yearList, genreList, frame, window, options, imageCounter):
    genre = ''
    for link in soup.find_all('div', class_="content"):
        for link in link.find_all('a'):
            header = link['href']
            if "year" in header:
                # Discog releases tend to have more credible tags, so each instance counts twice
                Label(frame.scrollable_frame, text="Year: " + str(link.get_text().strip())).pack(anchor='w')
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
    Label(frame.scrollable_frame, text="Genre: " + genre).pack(anchor='w')
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
                file.write(requests.get(link).content)
            imageCounter+=1
            imageCounter = reverseImageSearch(link, frame, window, imageCounter)
    return yearList, genreList, frame, imageCounter

def sendRequest(url, headers, frame, window):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        #generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return soup
    except requests.exceptions.ConnectionError:
        Label(frame.scrollable_frame, text="Connection refused").pack(anchor='w')
        window.update()
        # generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return False