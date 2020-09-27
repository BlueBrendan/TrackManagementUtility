from tkinter.tix import *
import getpass
from PIL import Image, ImageTk

#import methods
from track_preparation.fileSelect import fileSelect

#global variables
imageCounter = 0

#driver code
def scanTagsOnline(options, CONFIG_FILE):
    global imageCounter
    #delete all images stored in temp before proceeding
    if options["Reverse Image Search (B)"].get() == True:
        images = os.listdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/")
        for image in images:
            os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(image))
    fileSelect(options, imageCounter, CONFIG_FILE)




