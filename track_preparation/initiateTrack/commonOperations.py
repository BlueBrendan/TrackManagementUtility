import getpass
from PIL import Image

def saveThumbnail(image, thumbnails):
    if image != "NA":
        image = image.resize((200, 200), Image.ANTIALIAS)
        width, height = image.size
        thumbnails.append([image, width, height])
    else:
        fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Images/Thumbnail.png")
        fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
        thumbnails.append([fileImageImport, "NA", "NA"])
    return thumbnails