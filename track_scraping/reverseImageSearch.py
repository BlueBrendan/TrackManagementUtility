from tkinter import *
from tkinter.tix import *
from PIL import Image, ImageTk
import time
import requests
from selenium import webdriver
import getpass

def reverseImageSearch(link, headers, window, imageCounter, track, options):
    url = "https://images.google.com/searchbyimage?image_url=" + link
    if "https://" in link: link = link.replace("https://", '')
    elif "http://" in link: link = link.replace("http://", '')
    browser = webdriver.Firefox(executable_path=r'C:/Users/' + str(getpass.getuser()) + '/Documents/Track Management Utility/geckodriver.exe')
    browser.get(url)
    text = browser.find_elements_by_class_name("O1id0e")
    if len(text) > 0:
        text = text[0]
        sizes = []
        #append all sizes to list (in case of non-english language)
        imageLinks = text.find_elements_by_class_name('gl')
        if len(imageLinks) > 0:
            for image in imageLinks:
                text = image.text.replace('-', '').strip()
                sizes.append(text)
            #check for popups
            time.sleep(1)
            popups = browser.find_elements_by_xpath("//iframe")
            if len(popups) > 0:
                for popup in popups:
                    link = popup.get_attribute('src')
                    if 'consent.google.com/' in popup.get_attribute('src'):
                        link = popup.get_attribute('src').replace("consent.google.com/", "consent.google.com")
                        break
                #switch frames
                browser.switch_to.frame(browser.find_element_by_xpath("//iframe[@src='" + link + "']"))
                browser.find_element_by_xpath("//form[@class='A28uDc']").click()
                #return to original frame
                browser.switch_to.default_content()
            #search by the largest size
            browser.find_element_by_link_text(sizes[len(sizes)-1]).click()
            for i in range(1):
                images = browser.find_elements_by_class_name("rg_i.Q4LuWd")
                #make sure images have actually appeared
                if len(images) > 0:
                    images[i].click()
                    time.sleep(1)
                    counter = 0
                    subImages = browser.find_elements_by_xpath("//img[@class='n3VNCb']")
                    #wait for image to load with 1 second increments
                    while subImages==None and counter < int(options["Image Load Wait Time (I)"].get()):
                        time.sleep(1)
                        subImages = browser.find_elements_by_xpath("//img[@class='n3VNCb']")
                        counter+=1
                    for image in subImages:
                        counter=0
                        while 'data:image' in image.get_attribute('src') and counter < int(options["Image Load Wait Time (I)"].get()):
                            time.sleep(1)
                            counter+=1
                        if 'data:image' not in image.get_attribute('src'):
                            browser.get(image.get_attribute('src'))
                            # avoid duplicates
                            if browser.current_url not in track.URLList:
                                track.URLList.append(browser.current_url)
                                try:
                                    with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg", "wb") as file: file.write(requests.get(browser.current_url, headers=headers).content)
                                    fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg")
                                    imageCounter += 1
                                    # check image parameters
                                    width, height = fileImageImport.size
                                    if options["Stop Search After Conditions (B)"].get() and width >= int(options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[0]) and height >= int(options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[1]): track.stop = True
                                except: pass
                            break
    browser.quit()
    window.attributes("-topmost", 1)
    window.attributes("-topmost", 0)
    return imageCounter, track