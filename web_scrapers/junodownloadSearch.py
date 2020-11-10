import tkinter as tk
from tkinter.tix import *
from PIL import Image, ImageTk
import requests
import webbrowser

# import methods
from track_scraping.compareTokens import compareTokens
from track_scraping.reverseImageSearch import reverseImageSearch
from web_scrapers.webScrapingWindowControl import rerenderControls
from web_scrapers.webScrapingWindowControl import resetLeftRightFrames
from web_scrapers.sendRequest import prepareRequest
from web_scrapers.compareRuntime import compareRuntime
from commonOperations import performSearch
from commonOperations import allWidgets
from commonOperations import resource_path

# global variables
bg = "#282f3b"  # main bg color
secondary_bg = "#364153"    # secondary color
count = 0   # counter to store number of matches

def junodownloadSearch(filename, track, artistVariations, titleVariations, headers, search, webScrapingWindow, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, labelFrame, searchFrame, pageFrame, componentFrame, audio, options, initialCounter, imageCounter, images):
    global count
    count = 0
    widgetList = allWidgets(searchFrame)
    for item in widgetList: item.pack_forget()
    if len(filename) > 60: tk.Label(searchFrame, text="\nSearching Juno Download for " + str(filename)[0:59] + "...", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="left", padx=(10, 0), anchor='w')
    else: tk.Label(searchFrame, text="\nSearching Juno Download for " + str(filename), font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="left", padx=(10, 0), anchor='w')
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
                        refresh(webScrapingWindow)
                        soup = prepareRequest(link, headers, webScrapingWindow, leftComponentFrame)
                        if soup!=False:
                            # post link to web scraping window
                            widgetList = allWidgets(componentFrame)
                            for widget in widgetList: widget.pack_forget()
                            widgetList = allWidgets(pageFrame)
                            for widget in widgetList: widget.pack_forget()
                            # increment web scraping page and rerender count
                            webScrapingPage += 1
                            leftComponentFrame, rightComponentFrame = resetLeftRightFrames(componentFrame)
                            rerenderControls(pageFrame, webScrapingPage)
                            if len(link) >= 75: label = tk.Label(leftComponentFrame, text="\n" + str(link)[0:74] + "...", cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                            else: label = tk.Label(leftComponentFrame, text="\n" + str(link), cursor="hand2", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
                            label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link))
                            label.pack(padx=(10, 0), pady=(0, 25), anchor='w')
                            # update left component history frame
                            webScrapingLeftPane[webScrapingPage] = leftComponentFrame
                            # assume match will fail and no image will be found
                            webScrapingRightPane[webScrapingPage] = "NA"
                            # update link
                            webScrapingLinks[webScrapingPage] = link
                            finalMatch = False

                            # search individual listings in table
                            for item in soup.find_all('div',class_="row gutters-sm align-items-center product-tracklist-track"):
                                name = item.find('span').get_text()
                                if ' - ' in name:
                                    trackArtist = item.find('span').get_text().split(' - ')[0]
                                    trackTitle = item.find('span').get_text().split(' - ')[1]
                                else:
                                    trackArtist = ''
                                    trackTitle = item.find('span').get_text()
                                if not compareTokens(variation, trackTitle):
                                    # check runtime to ensure track is correct
                                    runtime = item.find('div', class_="col-1 d-none d-lg-block text-center").get_text()
                                    if not compareRuntime(runtime, audio):
                                        count+=1
                                        finalMatch = True
                                        for value in item.find_all('div', class_="col-1 d-none d-lg-block text-center"):
                                            # extract BPM
                                            if ":" not in value.get_text() and value.get_text()!='\xa0' and "BPM" in options["Selected Tags (L)"]:
                                                BPM = value.get_text()
                                                tk.Label(leftComponentFrame, text="BPM: " + str(BPM), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
                                                webScrapingLeftPane[webScrapingPage] = leftComponentFrame
                                                refresh(webScrapingWindow)
                                                track.BPMList.append(int(BPM))
                                                track.BPMList.append(int(BPM))
                                        # only push release and genre from header if title is found in tracklist
                                        for data in soup.select('div[class=mb-3]'):
                                            # extract release date
                                            if "Release_Date" in options["Selected Tags (L)"]:
                                                release = data.find("span", itemprop="datePublished").get_text()
                                                tk.Label(leftComponentFrame, text="Year: " + str(release), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
                                                track.yearList.append(int(release[-4:]))
                                            # extract genre
                                            if "Genre" in options["Selected Tags (L)"]:
                                                genre = data.find("a").get_text()
                                                tk.Label(leftComponentFrame, text="Genre: " + str(genre), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor='w')
                                                track.genreList.append(genre)
                                            webScrapingLeftPane[webScrapingPage] = leftComponentFrame
                                        # extract image
                                        if options["Extract Image from Website (B)"].get() == True and track.stop == False:
                                            try:
                                                item = soup.find('div', class_="jw-page")
                                                item = item.find('img').get('data-src-full')
                                                # write junodownload image to drive
                                                with open(resource_path('Temp/' + str(imageCounter) + '.jpg'), "wb") as file: file.write(requests.get(item, headers=headers).content)
                                                track.URLList.append(item)
                                                # load file icon
                                                fileImageImport = Image.open(resource_path('Temp/' + str(imageCounter) + '.jpg'))
                                                width, height = fileImageImport.size
                                                fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                                                images.append([fileImageImport, width, height])
                                                photo = ImageTk.PhotoImage(fileImageImport)
                                                fileImage = tk.Label(rightComponentFrame, image=photo, bg=bg)
                                                fileImage.image = photo
                                                fileImage.pack(padx=(0, 100), anchor="e")
                                                imageCounter += 1
                                                refresh(webScrapingWindow)
                                                webScrapingRightPane[webScrapingPage] = rightComponentFrame
                                                # perform image scraping if enabled in options
                                                if options["Reverse Image Search (B)"].get() == True and not track.stop:
                                                    if not performSearch(initialCounter, imageCounter): imageCounter, images, track = reverseImageSearch(item, headers, imageCounter, images, track, options)
                                            except: pass
                            # avoid counting the same entry twice
                            if not finalMatch:
                                tk.Label(leftComponentFrame, text="Track did not match with any of the listings", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")
                                refresh(webScrapingWindow)
                            break
                if options['Limit Number of Matches per Site (B)'].get() and count >= options['Match Limit (I)'].get(): break
    return track, imageCounter, images, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, searchFrame, pageFrame, componentFrame

def refresh(webScrapingWindow):
    webScrapingWindow.update()
