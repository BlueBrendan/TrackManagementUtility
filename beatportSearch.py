import requests
from bs4 import BeautifulSoup
from tkinter import *
import webbrowser
import time
import random
import threading

def beatportSearch(artist, title, yearList, BPMList, keyList, genreList, imageList, artistVariations, titleVariations, headers, search, frame, window):
#SECOND QUERY - BEATPORT

    Label(frame.scrollable_frame, text="\nSearching Beatport for " + str(artist) + " - " + str(title), font=("TkDefaultFont", 9, 'bold')).pack(anchor='w')
    window.update()
    url = "https://www.google.co.in/search?q=" + search + " Beatport"
    soup = sendRequest(url, headers, frame, window)
    if soup != False:
        for link in soup.find_all('a'):
            if "beatport.com" in link.get('href').split('&')[0] and (any(variation in link.get('href').split('&')[0].lower() for variation in artistVariations) or any(variation in link.get('href').split('&')[0].lower() for variation in titleVariations)):
                link = link.get('href').split('&')[0].split('=')[1]
                if "remix" in link and "remix" in title.lower() or "remix" not in title.lower() and "remix" not in link:
                    label = Label(frame.scrollable_frame, text="\n" + str(link), cursor="hand2")
                    label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
                    label.pack(anchor='w')
                    # refresh(frame, window)
                    window.update()
                    soup = sendRequest(link, headers, frame, window)
                    if soup != False and "Oops... the page you were looking for could not be found" not in str(soup):
                        #check if page is track (single), release (album), or classic beatport format
                        #case 1: release
                        if link[25:32] == "release":
                            for link in soup.find_all('li', class_="bucket-item ec-item track"):
                                #find all tracks in the release that contain the title
                                link = link.find('p', class_="buk-track-title")
                                #print(link.find('span', class_="buk-track-primary-title").get_text())
                                if link.find('a')['href'] in titleVariations:
                                    url = "https://www.beatport.com" + str(link.find('a')['href'])
                                    soup = sendRequest(url, headers, frame, window)
                                    if soup !=False:
                                        yearList, BPMList, keyList, genreList, imageList = beatportSingle(soup, yearList, BPMList, keyList, genreList, imageList, frame, window)
                        #case 2: classic
                        elif link[7:14] == "classic":
                            #case 2.1: chart
                            if link[28:34] == "classic page charts":
                                for link in soup.find_all('tr', {"class": ["track-grid-content altRow-0 playRow autoscroll", "track-grid-content altRow-1 playRow autoscroll"]}):
                                    link = link.find('td', class_="secondColumn")
                                    link = link.find('a')
                                    if link['href'] in titleVariations:
                                        url = link['href']
                                        soup = sendRequest(url, headers, frame, window)
                                        if soup != False:
                                            yearList, BPMList, keyList, genreList, imageList = beatportClassicSingle(soup, yearList, BPMList, keyList, genreList, imageList, frame, window)
                            #case 2.2: classic page release
                            elif link[28:35] == "release":
                                for link in soup.find_all('table', class_="track-grid track-grid-release"):
                                    link = link.find('td', class_="titleColumn")
                                    if link.find('a', class_="txt-larger")['href'] in titleVariations:
                                        url = link.find('a', class_="txt-larger")['href']
                                        soup = sendRequest(url, headers, frame, window)
                                        if soup != False:
                                            yearList, BPMList, keyList, genreList, imageList = beatportClassicSingle(soup, yearList,BPMList, keyList, genreList, imageList, frame, window)
                            #case 2.3: classic page track
                            # verify that the page is correct
                            elif link[28:34] != "artist":
                                trackHeader = soup.find('h2', class_="txt-xxlarge")
                                trackName = trackHeader.get_text()
                                trackRemix = trackHeader.find('span').get_text()
                                if trackRemix != '':
                                    if '(' in title and ')' in title:
                                        remix = title[title.index('(') + 1:title.index(')')]
                                        mismatch = compareTokens(remix, trackRemix)
                                        if mismatch == False:
                                            yearList, BPMList, keyList, genreList, imageList = beatportClassicSingle(soup, yearList,BPMList, keyList, genreList, imageList, frame, window)
                        #case 3: track
                        else:
                            link = soup.find('div', class_="interior-track-content")
                            # case 3.1: individual track
                            if link is not None:
                                trackHeader = soup.find('div', class_="interior-title")
                                trackName = trackHeader.find('h1').get_text()
                                trackMix = trackHeader.find('h1', class_="remixed").get_text()
                                if trackMix != '' and 'original' not in trackMix.lower():
                                    # verify that the page is correct
                                    if '(' in title and ')' in title:
                                        remix = title[title.rfind('(') + 1:title.rfind(')')]
                                        mismatch = compareTokens(remix, trackMix)
                                        if mismatch == False:
                                            yearList, BPMList, keyList, genreList, imageList = beatportSingle(soup, yearList, BPMList, keyList,genreList, imageList, frame, window)
                                else:
                                    yearList, BPMList, keyList, genreList, imageList = beatportSingle(soup, yearList, BPMList, keyList, genreList, imageList, frame, window)
    return yearList, BPMList, keyList, genreList, imageList

def beatportSingle(soup, yearList, BPMList, keyList, genreList, imageList, frame, window):
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
    link = soup.find('img', class_="interior-track-release-artwork")
    if link!=None:
        link = link['src']
        Label(frame.scrollable_frame, text="Image Link: " + str(link)).pack(anchor='w')
        refresh(frame.scrollable_frame, window)
        imageList.append(link)
    return yearList, BPMList, keyList, genreList, imageList

def beatportClassicSingle(soup, yearList, BPMList, keyList, genreList, imageList, frame, window):
    for link in soup.find_all('div', class_="waveform-meta-container"):
        for link in link.find_all('li'):
            if link.find('span', class_="meta-label txt-grey fontCondensed").get_text() == "Release Date":
                release = link.find('span', class_="meta-value txt-dark-grey fontCondensed").get_text()
                Label(frame.scrollable_frame, text="Year: " + str(release[0:4])).pack(anchor='w')
                refresh(frame.scrollable_frame, window)
                yearList.append(int(release[0:4]))
            elif link.find('span', class_="meta-label txt-grey fontCondensed").get_text() == "BPM":
                BPM = link.find('span', class_="meta-value txt-dark-grey fontCondensed").get_text()
                Label(frame.scrollable_frame, text="BPM: " + str(BPM)).pack(anchor='w')
                refresh(frame.scrollable_frame, window)
                BPMList.append(int(BPM))
            elif link.find('span', class_="meta-label txt-grey fontCondensed").get_text() == "Key":
                key = link.find('span', class_="key").get_text()
                # HTML code for ♭ symbol
                if '&#9837;' in key:
                    key = key[0:1] + "♭" + key[8:]
                # HTML code for ♯ symbol
                elif '&#9839;' in key:
                    key = key[0:1] + "♯" + key[8:]
                # Spacing
                if 'min' in key:
                    key = key[0:key.index('min')] + " " + key[key.index('min'):]
                elif 'maj' in key:
                    key = key[0:key.index('maj')] + " " + key[key.index('maj'):]
                Label(frame.scrollable_frame, text="Key: " + str(key)).pack(anchor='w')
                refresh(frame.scrollable_frame, window)
                keyList.append(key)
            elif link.find('span', class_="meta-label txt-grey fontCondensed").get_text() == "Genre":
                genre = link.find('span', class_="meta-value txt-dark-grey fontCondensed").get_text()
                Label(frame.scrollable_frame, text="Genre: " + str(genre)).pack(anchor='w')
                refresh(frame.scrollable_frame, window)
                genreList.append(genre)
    return yearList, BPMList, keyList, genreList, imageList

def compareTokens(title, name):
    mismatch = False
    tokens = name.split(' ')
    for i in range(len(tokens)):
        if "(" in tokens[i]:
            tokens[i] = str(tokens[i][0:tokens[i].index("(")]) + str(tokens[i][tokens[i].index("(") + 1:])
        elif ")" in tokens[i]:
            tokens[i] = str(tokens[i][0:tokens[i].index(")")]) + str(tokens[i][tokens[i].index(")") + 1:])
    difference = 0
    for var in tokens:
        if var.lower() not in title.lower():
            # edge case: mix and remix are synonymous
            if (var.lower() != "remix" and var.lower() != "mix") or ("remix" not in title.lower() and "mix" not in title.lower()):
                # edge case: original/extended mix is absent in one or another
                if ('extended' not in var.lower() and 'original' not in var.lower() and var.lower() != 'mix'):
                    # loop through each word in title, check if difference in strings is more than 2 characters
                    difference += len(var)
    if difference/len(title) > 0.10:
        mismatch = True
        return mismatch
    else:
        tokens = title.split(' ')
        for i in range(len(tokens)):
            if "(" in tokens[i]:
                tokens[i] = str(tokens[i][0:tokens[i].index("(")]) + str(tokens[i][tokens[i].index("(") + 1:])
            elif ")" in tokens[i]:
                tokens[i] = str(tokens[i][0:tokens[i].index(")")]) + str(tokens[i][tokens[i].index(")") + 1:])
        difference = 0
        for var in tokens:
            if var.lower() not in name.lower():
                # edge case: mix and remix are synonymous
                if (var.lower() != "remix" and var.lower() != "mix") or (
                        "remix" not in name.lower() and "mix" not in name.lower()):
                    # edge case: original/extended mix is absent in one or another
                    if ('extended' not in var.lower() and 'original' not in var.lower() and var.lower() != 'mix'):
                        # loop through each word in title, check if difference in strings is more than 2 characters
                        difference += len(var)
        if difference / len(title) > 0.10:
            mismatch = True
        return mismatch

def sendRequest(url, headers, frame, window):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # generate random waiting time to avoid being blocked
        threading.Thread(time.sleep(random.uniform(1.5, 4.5))).start()
        return soup
    except requests.exceptions.ConnectionError:
        Label(frame.scrollable_frame, text="Connection refused").pack(anchor='w')
        window.update()
        # generate random waiting time to avoid being blocked
        threading.Thread(time.sleep(random.uniform(1.5, 4.5))).start()
        return False

def refresh(frame, window):
    window.update()


