import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter.tix import *
import webbrowser
import time
import random
import threading
import concurrent.futures
import queue

def TESTING(token, que):
    print('LA')
    print(token)
    time.sleep(5)
    print("HERE")
    que.put("Five")

def junodownloadSearch(artist, title, yearList, BPMList, genreList, imageList, artistVariations, titleVariations, headers, search, frame, window):
#FIRST QUERY - JUNO DOWNLOAD
    Label(frame.scrollable_frame, text="\nSearching Juno Download for " + str(artist) + " - " + str(title), font=("TkDefaultFont", 9, 'bold')).pack(anchor='w')
    window.update()
    url = "https://www.google.co.in/search?q=" + search + " Junodownload"

    que = queue.Queue()
    thread = threading.Thread(target=TESTING, args=('Z',que, ))
    thread.start()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(sendRequest, url, headers, frame, window)
        soup = future.result()
    if soup!=False:
        for link in soup.find_all('div', class_="ZINbbc xpd O9g5cc uUPGi"):
            if 'junodownload.com' and 'products' in link.find('a').get('href').split('&')[0].lower() and (any(variation in link.find('div', class_="BNeawe s3v9rd AP7Wnd").get_text().lower() for variation in artistVariations) or any(variation in link.find('div', class_="BNeawe s3v9rd AP7Wnd").get_text().lower() for variation in titleVariations) or any(variation in link.find('div', class_="BNeawe vvjwJb AP7Wnd").get_text().lower() for variation in artistVariations) or any(variation in link.find('div', class_="BNeawe vvjwJb AP7Wnd").get_text().lower() for variation in titleVariations)):
                link = link.find('a').get('href').split('&')[0][7:]
                label = Label(frame.scrollable_frame, text="\n" + str(link), cursor="hand2")
                label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
                label.pack(anchor='w')
                # label.pack(anchor='w')
                # label.bind("<Button-1>", lambda e: webbrowser.open_new(link))
                window.update()
                threading.Thread(target=sendRequest, args=(url, headers, frame, window, que)).start()
                soup = que.get()
                if soup!=False:
                    #scrape release date and genre
                    found = False
                    for link in soup.find_all('div',class_="row gutters-sm align-items-center product-tracklist-track"):
                        name = link.find('span').get_text()
                        if ' - ' in name:
                            trackArtist = link.find('span').get_text().split(' - ')[0]
                            trackTitle = link.find('span').get_text().split(' - ')[1]
                        else:
                            trackArtist = ''
                            trackTitle = link.find('span').get_text()
                        if title.lower() == trackTitle.lower():
                            found = True
                            for value in link.find_all('div', class_="col-1 d-none d-lg-block text-center"):
                                #ensure that value being scraped is BPM and not length, only store if BPM value is non-blank
                                if ":" not in value.get_text() and value.get_text() != '\xa0':
                                    BPM = value.get_text()
                                    Label(frame.scrollable_frame, text="BPM: " + str(BPM)).pack(anchor='w')
                                    window.update()
                                    BPMList.append(int(BPM))
                        else:
                            # test 1: compare tracklist title with the track title word for word
                            #trim common phrases like extended mix or original mix out of the strings
                            if " (extended mix)" in title.lower():
                                title = title[0:title.lower().index(" (extended mix")]
                            elif " (original mix)" in title.lower():
                                title = title[0:title.lower().index(" (original mix")]
                            if " (extended mix)" in name.lower():
                                name = name[0:name.lower().index(" (extended mix")]
                            elif " (original mix)" in name.lower():
                                name = name[0:name.lower().index(" (original mix")]
                            tokens = name.split(" ")
                            for i in range(len(tokens)):
                                if "(" in tokens[i]:
                                    tokens[i] = str(tokens[i][0:tokens[i].index("(")]) + str(
                                        tokens[i][tokens[i].index("(") + 1:])
                                elif ")" in tokens[i]:
                                    tokens[i] = str(tokens[i][0:tokens[i].index(")")]) + str(
                                        tokens[i][tokens[i].index(")") + 1:])
                            mismatch = False
                            mismatch = compareTokens(title, name, mismatch)
                            if mismatch == False:
                                found = True
                                for value in link.find_all('div', class_="col-1 d-none d-lg-block text-center"):
                                    if ":" not in value.get_text():
                                        BPM = value.get_text()
                                        Label(frame.scrollable_frame, text="BPM: " + str(BPM)).pack(anchor='w')
                                        window.update()
                                        BPMList.append(int(BPM))
                            #only push release and genre from header if title is found in tracklist
                    if found==True:
                        # scrape release date and genre
                        for link in soup.select('div[class=mb-3]'):
                            release = link.find("span", itemprop="datePublished").get_text()
                            Label(frame.scrollable_frame, text="Year: " + str(release)).pack(anchor='w')
                            yearList.append(int(release[-4:]))
                            genre = link.find("a").get_text()
                            Label(frame.scrollable_frame, text="Genre: " + str(genre)).pack(anchor='w')
                            genreList.append(genre)
                            link = soup.find('div', class_="jw-page")
                            link = link.find('img')
                            Label(frame.scrollable_frame, text="Image Link: " + link['src']).pack(anchor='w')
                            imageList.append(link['src'])
                            window.update()
            elif "junodownload" and "products" in link.find('a').get('href').split('&')[0].lower():
                attemptList = []
                descriptions = soup.find_all('div', class_="BNeawe s3v9rd AP7Wnd")
                for description in descriptions:
                    if description.find('span', class_="r0bn4c rQMQod"):
                        if title.lower() in description.get_text().lower() and link not in attemptList:
                            attemptList.append(link)
                            sublink = link.find('a').get('href').split('&')[0][7:]
                            label = Label(frame.scrollable_frame, text="\n" + str(sublink), cursor="hand2")
                            label.bind("<Button-1>", lambda e, link=sublink: webbrowser.open_new(link))
                            label.pack(anchor='w')
                            # label.pack(anchor='w')
                            # label.bind("<Button-1>", lambda e: webbrowser.open_new(link))
                            window.update()
                            threading.Thread(target=sendRequest, args=(url, headers, frame, window, que)).start()
                            soup = que.get()
                            if soup != False:
                                # scrape release date and genre
                                found = False
                                for sublink in soup.find_all('div', class_="row gutters-sm align-items-center product-tracklist-track"):
                                    name = sublink.find('span').get_text()
                                    if ' - ' in name:
                                        trackArtist = sublink.find('span').get_text().split(' - ')[0]
                                        trackTitle = sublink.find('span').get_text().split(' - ')[1]
                                    else:
                                        trackArtist = ''
                                        trackTitle = sublink.find('span').get_text()
                                    if title.lower() == trackTitle.lower():
                                        found = True
                                        for value in sublink.find_all('div', class_="col-1 d-none d-lg-block text-center"):
                                            # ensure that value being scraped is BPM and not length, only store if BPM value is non-blank
                                            if ":" not in value.get_text() and value.get_text() != '\xa0':
                                                BPM = value.get_text()
                                                Label(frame.scrollable_frame, text="BPM: " + str(BPM)).pack(anchor='w')
                                                window.update()
                                                BPMList.append(int(BPM))
                                    else:
                                        # test 1: compare tracklist title with the track title word for word
                                        # trim common phrases like extended mix or original mix out of the strings
                                        if " (extended mix)" in title.lower():
                                            title = title[0:title.lower().index(" (extended mix")]
                                        elif " (original mix)" in title.lower():
                                            title = title[0:title.lower().index(" (original mix")]
                                        if " (extended mix)" in name.lower():
                                            name = name[0:name.lower().index(" (extended mix")]
                                        elif " (original mix)" in name.lower():
                                            name = name[0:name.lower().index(" (original mix")]
                                        tokens = name.split(" ")
                                        for i in range(len(tokens)):
                                            if "(" in tokens[i]:
                                                tokens[i] = str(tokens[i][0:tokens[i].index("(")]) + str(
                                                    tokens[i][tokens[i].index("(") + 1:])
                                            elif ")" in tokens[i]:
                                                tokens[i] = str(tokens[i][0:tokens[i].index(")")]) + str(
                                                    tokens[i][tokens[i].index(")") + 1:])
                                        mismatch = False
                                        mismatch = compareTokens(title, name, mismatch)
                                        if mismatch == False:
                                            found = True
                                            for value in sublink.find_all('div', class_="col-1 d-none d-lg-block text-center"):
                                                if ":" not in value.get_text():
                                                    BPM = value.get_text()
                                                    Label(frame.scrollable_frame, text="BPM: " + str(BPM)).pack(anchor='w')
                                                    window.update()
                                                    BPMList.append(int(BPM))
                                        # only push release and genre from header if title is found in tracklist
                                if found == True:
                                    # scrape release date and genre
                                    for sublink in soup.select('div[class=mb-3]'):
                                        release = sublink.find("span", itemprop="datePublished").get_text()
                                        Label(frame.scrollable_frame, text="Year: " + str(release)).pack(anchor='w')
                                        yearList.append(int(release[-4:]))
                                        genre = sublink.find("a").get_text()
                                        Label(frame.scrollable_frame, text="Genre: " + str(genre)).pack(anchor='w')
                                        genreList.append(genre)
                                        sublink = soup.find('div', class_="jw-page")
                                        sublink = sublink.find('img')
                                        Label(frame.scrollable_frame, text="Image Link: " + sublink['src']).pack(anchor='w')
                                        imageList.append(sublink['src'])
                                        window.update()
    return yearList, BPMList, genreList, imageList

def compareTokens(title, name, mismatch):
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

def sendRequest(url, headers, frame, window, que):
    print("HERE")
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # generate random waiting time to avoid being blocked
        threading.Thread(time.sleep(random.uniform(1.5, 4.5))).start()
        que.put(soup)
    except requests.exceptions.ConnectionError:
        Label(frame.scrollable_frame, text="Connection refused").pack(anchor='w')
        window.update()
        # generate random waiting time to avoid being blocked
        threading.Thread(time.sleep(random.uniform(1.5, 4.5))).start()
        que.put(False)
