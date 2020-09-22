import requests
from bs4 import BeautifulSoup
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

def junodownloadSearch(artist, title, var, yearList, BPMList, genreList, URLList, artistVariations, titleVariations, headers, search, frame, window, audio, options, imageCounter):
#FIRST QUERY - JUNO DOWNLOAD
    Label(frame.scrollable_frame, text="\nSearching Juno Download for " + str(var), font=("TkDefaultFont", 9, 'bold')).pack(anchor='w')
    window.update()
    url = "https://www.google.co.in/search?q=" + search + " Junodownload"
    soup = sendRequest(url, headers, frame, window)
    if soup!=False:
        for result in soup.find_all('div', class_="ZINbbc xpd O9g5cc uUPGi"):
            if 'junodownload.com' and 'products' in result.find('a').get('href').split('&')[0].lower():
                for variation in titleVariations:
                    variation = variation.replace('-', ' ')
                    if variation.lower() in str(result).lower():
            # if (any(variation in link.find('div', class_="BNeawe s3v9rd AP7Wnd").get_text().lower() for variation in artistVariations) or any(variation in link.find('div', class_="BNeawe s3v9rd AP7Wnd").get_text().lower() for variation in titleVariations) or any(variation in link.find('div', class_="BNeawe vvjwJb AP7Wnd").get_text().lower() for variation in artistVariations) or any(variation in link.find('div', class_="BNeawe vvjwJb AP7Wnd").get_text().lower() for variation in titleVariations)):
                        link = result.find('a').get('href').split('&')[0][7:]
                        label = Label(frame.scrollable_frame, text="\n" + str(link), cursor="hand2")
                        label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
                        label.pack(anchor='w')
                        # label.pack(anchor='w')
                        # label.bind("<Button-1>", lambda e: webbrowser.open_new(link))
                        window.update()
                        soup = sendRequest(link, headers, frame, window)
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
                                                Label(frame.scrollable_frame, text="BPM: " + str(BPM)).pack(anchor='w')
                                                window.update()
                                                BPMList.append(int(BPM))
                                                BPMList.append(int(BPM))
                                        #only push release and genre from header if title is found in tracklist
                                        # scrape release date and genre
                                        for link in soup.select('div[class=mb-3]'):
                                            release = link.find("span", itemprop="datePublished").get_text()
                                            Label(frame.scrollable_frame, text="Year: " + str(release)).pack(anchor='w')
                                            yearList.append(int(release[-4:]))
                                            genre = link.find("a").get_text()
                                            Label(frame.scrollable_frame, text="Genre: " + str(genre)).pack(anchor='w')
                                            genreList.append(genre)
                                            # extract image if image scraping is enabled in options
                                            if options["Reverse Image Search (B)"].get()==True:
                                                link = soup.find('div', class_="jw-page")
                                                link = link.find('img').get('data-src-full')
                                                # write junodownload image to drive
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
                                                imageCounter += 1
                                                imageCounter, URLList = reverseImageSearch(link, headers, window, imageCounter, URLList, options)
    return yearList, BPMList, genreList, imageCounter, URLList

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
