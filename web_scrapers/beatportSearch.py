from track_scraping.compareTokens import compareTokens
import requests
from bs4 import BeautifulSoup
import getpass
from tkinter import *
from PIL import Image, ImageTk
import webbrowser
import time
import random

#import methods
from track_scraping.reverseImageSearch import reverseImageSearch
from web_scrapers.compareRuntime import compareRuntime

def beatportSearch(artist, title, var, yearList, BPMList, keyList, genreList, URLList, artistVariations, titleVariations, headers, search, frame, window, audio, options, imageCounter):
    #SECOND QUERY - BEATPORT
    Label(frame.scrollable_frame, text="\nSearching Beatport for " + str(var), font=("TkDefaultFont", 9, 'bold')).pack(anchor='w')
    window.update()
    url = "https://www.google.co.in/search?q=" + search + " Beatport"
    soup = sendRequest(url, headers, frame, window)
    if soup == False:
        Label(frame.scrollable_frame, text="Connection Failed").pack(anchor='w')
        refresh(frame.scrollable_frame, window)
        return yearList, BPMList, keyList, genreList
    for link in soup.find_all('a'):
        if "www.beatport.com" in link.get('href').split('&')[0]:
            lastForwardslashIndex = link.get('href').split('&')[0].lower().index('/', link.get('href').split('&')[0].lower().rfind('/'))
            content = link.get('href').split('&')[0].lower()[link.get('href').split('&')[0].lower().index('beatport.com') + len("beatport.com"):lastForwardslashIndex]
            content = content[content.index('/', 1)+1:].replace('-', ' ')
            contentVariations = [content]
            if 'extended remix' in content.lower():
                contentVariations.append(content.replace('extended remix', 'remix'))
            mismatch = True
            if '/' not in content:
                for variation in titleVariations:
                    variation = variation.replace('-', ' ')
                    for content in contentVariations:
                        if variation in content:
                            mismatch = False
                            break
                        else:
                            mismatch = compareTokens(variation, content)
                            if not mismatch:break
                    if not mismatch:break
            if mismatch == False:
                link = link.get('href').split('&')[0].split('=')[1]
                if "remix" in link and "remix" in title.lower() or "remix" not in title.lower() and "remix" not in link:
                    label = Label(frame.scrollable_frame, text="\n" + str(link), cursor="hand2")
                    label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
                    label.pack(anchor='w')
                    window.update()
                    soup = sendRequest(link, headers, frame, window)
                    if soup != False and "Oops... the page you were looking for could not be found" not in str(soup):
                        #check if page is a track (single) or a release (album)
                        #case 1: release
                        if link[25:32] == "release": yearList, BPMList, keyList, genreList, imageCounter, URLList = beatportRelease(soup, titleVariations, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, headers, frame, window, options, imageCounter)
                        #case 2: track
                        elif link[25:30] == "track": yearList, BPMList, keyList, genreList, imageCounter, URLList = beatportTrack(soup, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, frame, window, options, imageCounter)
    return yearList, BPMList, keyList, genreList, imageCounter, URLList

#search beatport releases, filter individual tracks
def beatportRelease(soup, titleVariations, yearList, BPMList, keyList, genreList, URLList, audio, title, headers, frame, window, options, imageCounter):
    for link in soup.find_all('li', class_="bucket-item ec-item track"):
        # find all tracks in the release that contain the title
        link = link.find('p', class_="buk-track-title")
        if link.find('a')['href'] in titleVariations:
            url = "https://www.beatport.com" + str(link.find('a')['href'])
            soup = sendRequest(url, headers, frame, window)
            if soup == False:
                Label(frame.scrollable_frame, text="Connection Failed").pack(anchor='w')
                refresh(frame.scrollable_frame, window)
                return yearList, BPMList, keyList, genreList, imageCounter
            yearList, BPMList, keyList, genreList, imageCounter, URLList = beatportTrack(soup, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, frame, window, options, imageCounter)
    return yearList, BPMList, keyList, genreList, imageCounter, URLList

#search beatport tracks, extract info in the event of a match
def beatportTrack(soup, yearList, BPMList, keyList, genreList, URLList, headers, audio, title, frame, window, options, imageCounter):
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
                if compareTokens(remix, trackMix) == False:
                    yearList, BPMList, keyList, genreList, URLList, imageCounter = extractInfo(soup, yearList, BPMList, keyList, genreList, URLList, headers, frame, window, options, imageCounter)
            else:
                yearList, BPMList, keyList, genreList, URLList, imageCounter = extractInfo(soup, yearList, BPMList, keyList, genreList, URLList, headers, frame, window, options, imageCounter)
    return yearList, BPMList, keyList, genreList, imageCounter, URLList

#extract year, BPM, key, and genre
def extractInfo(soup, yearList, BPMList, keyList, genreList, URLList, headers, frame, window, options, imageCounter):
    for link in soup.find_all('ul', class_="interior-track-content-list"):
        release = link.find('li', class_="interior-track-content-item interior-track-released")
        release = release.find('span', class_="value").get_text()
        Label(frame.scrollable_frame, text="Year: " + str(release[0:4])).pack(anchor='w')
        refresh(frame, window)
        yearList.append(int(release[0:4]))
        BPM = link.find('li', class_="interior-track-content-item interior-track-bpm")
        BPM = BPM.find('span', class_="value").get_text()
        Label(frame.scrollable_frame, text="BPM: " + str(BPM)).pack(anchor='w')
        refresh(frame, window)
        BPMList.append(int(BPM))
        key = link.find('li', class_="interior-track-content-item interior-track-key")
        key = key.find('span', class_="value").get_text()
        Label(frame.scrollable_frame, text="Key: " + str(key)).pack(anchor='w')
        refresh(frame.scrollable_frame, window)
        keyList.append(key)
        genre = link.find('li', class_="interior-track-content-item interior-track-genre")
        if genre.find('span', class_="value sep"):
            firstGenre = genre.find('span', class_="value")
            firstGenre = firstGenre.find('a').get_text()
            secondGenre = genre.find('span', class_="value sep")
            secondGenre = secondGenre.find('a').get_text()
            Label(frame.scrollable_frame, text="Genre: " + str(firstGenre) + ' | ' + str(secondGenre)).pack(anchor='w')
            refresh(frame.scrollable_frame, window)
            genreList.append(firstGenre)
            genreList.append(secondGenre)
        else:
            genre = genre.find('span', class_="value")
            genre = genre.find('a').get_text()
            Label(frame.scrollable_frame, text="Genre: " + str(genre)).pack(anchor='w')
            refresh(frame.scrollable_frame, window)
            genreList.append(genre)
    if options["Reverse Image Search (B)"].get() == True:
        link = soup.find('img', class_="interior-track-release-artwork")
        if link!=None:
            link = link['src']
            # write beatport image to drive
            with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg", "wb") as file:
                file.write(requests.get(link, headers=headers).content)
            URLList.append(link)
            # load file icon
            fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg")
            fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(fileImageImport)
            fileImage = Label(frame.scrollable_frame, image=photo)
            fileImage.image = photo
            fileImage.pack(anchor="w")
            window.update()
            imageCounter+=1
            imageCounter, URLList = reverseImageSearch(link, headers, window, imageCounter, URLList, options)
    return yearList, BPMList, keyList, genreList, URLList, imageCounter

def sendRequest(url, headers, frame, window):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return soup
    except requests.exceptions.ConnectionError:
        Label(frame.scrollable_frame, text="Connection refused").pack(anchor='w')
        window.update()
        # generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return False

def refresh(frame, window):
    window.update()


