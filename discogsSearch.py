import requests
from bs4 import BeautifulSoup
from tkinter import *
import webbrowser

def discogsSearch(artist, title, yearList, genreList, imageList, artistVariations, titleVariations, headers, search, frame, window):
    # THIRD QUERY - DISCOGS
    Label(frame.scrollable_frame, text="\nSearching Discogs for " + str(artist) + " - " + str(title), font=("TkDefaultFont", 9, 'bold')).pack(anchor='w')
    window.update()
    url = "https://www.google.co.in/search?q=" + search + " Discogs"
    soup = sendRequest(url, headers, frame, window)
    if soup!='':
        for link in soup.find_all('a'):
            if "https://www.discogs" in link.get('href').lower().split('&')[0] and (any(variation in link.get('href').split('&')[0].lower() for variation in artistVariations) or any(variation in link.get('href').split('&')[0].lower() for variation in titleVariations)):
                link = link.get('href').split('&')[0].split('=')[1]
                label = Label(frame.scrollable_frame, text="\n" + str(link), cursor="hand2")
                label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
                label.pack(anchor='w')
                window.update()
                try:
                    response = requests.get(link, headers=headers)
                except requests.exceptions.ConnectionError:
                    print("Connection refused")
                    break
                soup = BeautifulSoup(response.text, "html.parser")
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
                            tokens = name.split(" ")
                            mismatch = False
                            mismatch = compareTokens(title, name, mismatch)
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

def sendRequest(url, headers, frame, window):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.exceptions.ConnectionError:
        Label(frame.scrollable_frame, text="Connection refused").pack(anchor='w')
        window.update()
        return