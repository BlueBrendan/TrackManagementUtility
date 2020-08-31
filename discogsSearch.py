from compareTokens import compareTokens
import requests
from bs4 import BeautifulSoup
from tkinter import *
import webbrowser
import time
import random

def discogsSearch(artist, title, yearList, genreList, imageList, artistVariations, titleVariations, headers, search, frame, window):
    # THIRD QUERY - DISCOGS
    Label(frame.scrollable_frame, text="\nSearching Discogs for " + str(artist) + " - " + str(title), font=("TkDefaultFont", 9, 'bold')).pack(anchor='w')
    window.update()
    url = "https://www.google.co.in/search?q=" + search + " Discogs"
    soup = sendRequest(url, headers, frame, window)
    if soup != False:
        for link in soup.find_all('a'):
            if "discogs.com" in link.get('href').lower().split('&')[0] and (any(variation in link.get('href').split('&')[0].lower() for variation in artistVariations) or any(variation in link.get('href').split('&')[0].lower() for variation in titleVariations)):
                link = link.get('href').split('&')[0].split('=')[1]
                label = Label(frame.scrollable_frame, text="\n" + str(link), cursor="hand2")
                label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
                label.pack(anchor='w')
                window.update()
                soup = sendRequest(link, headers, frame, window)
                if soup!=False:
                    # first check if the title is in the tracklist, push data if it is
                    link = soup.find('table', class_="playlist")
                    # handle 404 links
                    if link != None:
                        for link in link.find_all('td', class_="track tracklist_track_title"):
                            name = link.find('span', class_="tracklist_track_title").get_text()
                            if link.find('a') != None:
                                remix = link.find('a').get_text()
                                if remix.lower() not in name.lower():
                                    if '(' in name:
                                        name = name[0:name.index('(') + 1] + remix + " " + name[name.index("(") + 1:]
                            # check if title and name are exact matches
                            if title.lower() == name.lower():
                                yearList, genreList, frame = discogsRelease(soup, yearList, genreList, frame, window)
                                break
                            else:
                                # test 1: compare tracklist title with track title word for word
                                mismatch = compareTokens(title, name)
                                if mismatch == False:
                                    yearList, genreList, frame = discogsRelease(soup, yearList, genreList, frame, window)
                                    break
    return yearList, genreList, imageList, window

def discogsRelease(soup, yearList, genreList, frame, window):
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
                Label(frame.scrollable_frame, text="Genre: " + str(link.get_text().strip())).pack(anchor='w')
                window.update()
                genreList.append(link.get_text().strip())
    return yearList, genreList, frame

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