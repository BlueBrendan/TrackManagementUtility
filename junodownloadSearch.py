from compareTokens import compareTokens
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter.tix import *
import webbrowser
import time
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import getpass


def junodownloadSearch(artist, title, yearList, BPMList, genreList, imageList, artistVariations, titleVariations, headers, search, frame, window, audio):
#FIRST QUERY - JUNO DOWNLOAD
    Label(frame.scrollable_frame, text="\nSearching Juno Download for " + str(artist) + " - " + str(title), font=("TkDefaultFont", 9, 'bold')).pack(anchor='w')
    window.update()
    url = "https://www.google.co.in/search?q=" + search + " Junodownload"
    soup = sendRequest(url, headers, frame, window)
    if soup!=False:
        for result in soup.find_all('div', class_="ZINbbc xpd O9g5cc uUPGi"):
            if 'junodownload.com' and 'products' in result.find('a').get('href').split('&')[0].lower():
                # print(soup.prettify())
                for variation in titleVariations:
                    variation = variation.replace('-', ' ')
                    # print("variation: " + str(variation))
                    # print("div: " + str(div))
                    if variation.lower() in str(result).lower():
            #     print(div)
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
                                    if compareRuntime(link, audio) == False:
                                        for value in link.find_all('div', class_="col-1 d-none d-lg-block text-center"):
                                            if ":" not in value.get_text():
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
                                            link = soup.find('div', class_="jw-page")
                                            link = link.find('img')
                                            label = Label(frame.scrollable_frame, text="Image Link: " + str(link['src']), cursor="hand2")
                                            label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new(link['src']))
                                            label.pack(anchor='w')
                                            imageList.append(link['src'])
                                            window.update()
                                            # extract image
                                            reverseImageSearch(link['src'])

    return yearList, BPMList, genreList, imageList

def compareRuntime(link, audio):
    runtime = link.find('div', class_="col-1 d-none d-lg-block text-center").get_text()
    minutes = int(runtime.split(':')[0])
    seconds = int(runtime.split(':')[1])
    runtime = minutes * 60 + seconds
    difference = abs(runtime - audio.info.length)
    #max difference of 5 seconds
    if difference > 5:return True
    else:return False

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

def reverseImageSearch(link):
    url = "https://images.google.com/searchbyimage?image_url=" + link
    if "https://" in link:
        link = link.replace("https://", '')
    elif "http://" in link:
        link = link.replace("http://", '')
    browser = webdriver.Firefox(executable_path=r'C:/Users/' + str(getpass.getuser()) + '/Documents/Track Management Utility/geckodriver.exe')
    browser.get(url)
    browser.maximize_window()
    text = browser.find_element_by_class_name("O1id0e")
    if 'Large' in text.get_attribute('innerHTML') or "All sizes" in text.get_attribute('innerHTML'):
        if 'Large' in text.get_attribute('innerHTML'):
            browser.find_element_by_link_text("Large").click()
        elif "All sizes" in text.get_attribute('innerHTML'):
            browser.find_element_by_link_text("All sizes").click()
        for i in range(3):
            images = browser.find_elements_by_class_name("rg_i.Q4LuWd")
            time.sleep(1)
            images[i].click()
            #wait for image to load
            time.sleep(1)
            subImages = browser.find_elements_by_xpath("//img[@class='n3VNCb']")
            for image in subImages:
                if 'data:image' not in image.get_attribute('src'):
                    browser.get(image.get_attribute('src'))
                    time.sleep(1)
                    browser.back()
                    break

    # browser.find_element_by_class_name("rg_i.Q4LuWd").click()
    # for i in range(4):
    #     actionChains.context_click(images[i]).perform()
    #     actionChains.send_keys(Keys.ARROW_DOWN).perform()
    #     actionChains.send_keys(Keys.ENTER).perform()

    # browser.quit()
