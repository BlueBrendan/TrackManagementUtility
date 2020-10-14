from tkinter.tix import *
import getpass
from PIL import Image, ImageTk

#import methods
from track_preparation.fileSelect import fileSelect

#global variables
imageCounter = 0

def scanTagsOnline(options, CONFIG_FILE, window):
    global imageCounter
    #delete all images stored in temp before proceeding
    if not os.path.isdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/"): os.mkdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/")
    else:
        images = os.listdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/")
        for image in images: os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(image))
    webScrapingWindow = fileSelect(options, imageCounter, CONFIG_FILE, window)
    return webScrapingWindow




