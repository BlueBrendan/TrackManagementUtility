from tkinter.tix import *

# import methods
from track_preparation.fileSelect import fileSelect
from commonOperations import resource_path

# global variables
imageCounter = 0

def scanTagsOnline(options, CONFIG_FILE, window):
    global imageCounter
    # delete all images stored in temp before proceeding
    if not os.path.isdir(resource_path('Temp/')): os.mkdir(resource_path('Temp/'))
    else:
        images = os.listdir(resource_path('Temp/'))
        for image in images: os.remove(resource_path('Temp/' + str(image)))
    webScrapingWindow, webScrapingPage = fileSelect(options, imageCounter, CONFIG_FILE, window)
    return webScrapingWindow, webScrapingPage




