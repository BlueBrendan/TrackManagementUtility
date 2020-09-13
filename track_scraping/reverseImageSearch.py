from tkinter import *
import time
import requests
from selenium import webdriver
import getpass
from PIL import Image, ImageTk

def reverseImageSearch(link, frame, window, imageCounter):
    url = "https://images.google.com/searchbyimage?image_url=" + link
    if "https://" in link:
        link = link.replace("https://", '')
    elif "http://" in link:
        link = link.replace("http://", '')
    browser = webdriver.Firefox(executable_path=r'C:/Users/' + str(getpass.getuser()) + '/Documents/Track Management Utility/geckodriver.exe')
    browser.get(url)
    text = browser.find_element_by_class_name("O1id0e")
    if 'Large' in text.get_attribute('innerHTML') or "All sizes" in text.get_attribute('innerHTML'):
        if 'Large' in text.get_attribute('innerHTML'):
            browser.find_element_by_link_text("Large").click()
        elif "All sizes" in text.get_attribute('innerHTML'):
            browser.find_element_by_link_text("All sizes").click()
        for i in range(1):
            images = browser.find_elements_by_class_name("rg_i.Q4LuWd")
            time.sleep(2)
            images[i].click()
            #wait for image to load
            time.sleep(3)
            subImages = browser.find_elements_by_xpath("//img[@class='n3VNCb']")
            for image in subImages:
                if 'data:image' not in image.get_attribute('src'):
                    browser.get(image.get_attribute('src'))
                    time.sleep(1)
                    with open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg", "wb") as file:
                        file.write(requests.get(browser.current_url).content)
                    # load file icon
                    fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(imageCounter) + ".jpg")
                    imageCounter+=1
                    fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(fileImageImport)
                    fileImage = Label(frame.scrollable_frame, image=photo)
                    fileImage.image = photo
                    fileImage.pack(anchor="w")
                    break
    browser.quit()
    return imageCounter