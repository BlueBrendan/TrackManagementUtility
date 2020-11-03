import tkinter as tk
import getpass
import os
from PIL import Image, ImageTk
from matplotlib import font_manager
import pyglet

# import methods
from compareDrives import compareDrives
from track_preparation.scanTagsOnline import scanTagsOnline
from options.updatePreferences import updatePreferences
from commonOperations import resource_path

proximaNovaRegular = False
proximaNovaBold = False
# check if font proxima nova is installed
for font in font_manager.win32InstalledFonts():
    if 'proxima nova bold' in font.lower(): proximaNovaBold = True
    elif 'proxima nova' in font.lower(): proximaNovaRegular = True
if not proximaNovaRegular: pyglet.font.add_file(resource_path('Proxima Nova Regular.ttf'))
if not proximaNovaBold: pyglet.font.add_file(resource_path('Proxima Nova Bold.ttf'))

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

#global variables
window = False

#MAIN DRIVER CODEd
root = tk.Tk()
root.title("Track Management Utility V1.0")
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
x = (ws/2) - (1000/2)
y = (hs/2) - (660/2)
root.geometry('%dx%d+%d+%d' % (1000, 600, x, y))
root.configure(bg=bg)
root.iconbitmap(resource_path('favicon.ico'))

def createConfigFile(flag):
    CONFIG_FILE = r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt"
    if flag=='F' or (flag=="N" and not os.path.exists(CONFIG_FILE)):
        # create settings folder
        if not os.path.isdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility"):
            path = r"C:/Users/" + str(getpass.getuser()) + "/Documents"
            os.mkdir(path + "/Track Management Utility")
        # create setttings file
        file = open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt", 'w')
        file.write("-GENERAL-\nSubdirectories (B):True\nClose Scraping Window (B):True\nFirst Default Directory (S):\nSecond Default Directory (S):\nCopy Directory Contents (B):True\n\n"
                   "-SCRAPING SETTINGS-\nScrape Junodownload (B):True\nScrape Beatport (B):True\nScrape Discogs (B):True\nExtract Image from Website (B):True\nLimit Number of Matches per Site (B):True\nMatch Limit (I):4\n\n"
                   "-IMAGE SCRAPING-\nReverse Image Search (B):True\nDelete Stored Images (B):True\nImage Load Wait Time (I):5\nNumber of Images Per Page (I):3\nStop Search After Conditions (B):True\nStop Search After Finding Image of Resolution (S):2000x2000\nHide Selenium Browser (B):True\n\n"
                   "-TAGGING-\nScan Filename and Tags (B):True\nCheck for Numbering Prefix (B):True\nCheck for Extraneous Hyphens (B):True\nCheck for Underscores (B):True\nCheck for Capitalization (B):True\nAlways Capitalize (L):\nNever Capitalize (L):\nAudio naming format (S):Dynamic\nSelected Tags (L):Artist, BPM, Genre, Image, Key, Release_Date, ReplayGain, Title\nDelete Unselected Tags (B):False\n")
        file.close()
    return CONFIG_FILE

def compareDirectories(CONFIG_FILE):
    config_file = open(CONFIG_FILE, 'r').read()
    term = "First Default Directory (S):"
    firstDefaultDirectory = config_file[config_file.index(term) + len(term):config_file.index('\n', config_file.index(term) + len(term))]
    term = "Second Default Directory (S):"
    secondDefaultDirectory = config_file[config_file.index(term) + len(term):config_file.index('\n', config_file.index(term) + len(term))]
    compareDrives(CONFIG_FILE, firstDefaultDirectory, secondDefaultDirectory, options, root)

def readValuesFromConfig(CONFIG_FILE):
    config_file = open(CONFIG_FILE, 'r').read()
    terms = ["Subdirectories (B)", "Close Scraping Window (B)", "First Default Directory (S)", "Second Default Directory (S)", "Copy Directory Contents (B)",
             "Scrape Junodownload (B)", "Scrape Beatport (B)", 'Scrape Discogs (B)', "Extract Image from Website (B)", "Limit Number of Matches per Site (B)", "Match Limit (I)",
             "Reverse Image Search (B)", "Delete Stored Images (B)", "Image Load Wait Time (I)", "Number of Images Per Page (I)", "Stop Search After Conditions (B)", "Stop Search After Finding Image of Resolution (S)", "Hide Selenium Browser (B)",
             "Scan Filename and Tags (B)", "Check for Numbering Prefix (B)", "Check for Extraneous Hyphens (B)", "Check for Underscores (B)", "Check for Capitalization (B)", "Always Capitalize (L)", "Never Capitalize (L)", "Audio naming format (S)", "Selected Tags (L)", "Delete Unselected Tags (B)"]
    options = {}
    for term in terms:
        if term in config_file:
            #boolean
            if (term[len(term) - 2:len(term) - 1]) == 'B':
                try: options[term] = tk.BooleanVar(value=config_file[config_file.index(term) + len(term) + 1:config_file.find('\n', config_file.index(term) + len(term))])
                except:
                    os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt")
                    CONFIG_FILE = createConfigFile("F")
                    readValuesFromConfig(CONFIG_FILE)
            #string
            elif (term[len(term) - 2:len(term) - 1]) == 'S':
                try: options[term] = tk.StringVar(value=config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))])
                except:
                    os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt")
                    CONFIG_FILE = createConfigFile("F")
                    readValuesFromConfig(CONFIG_FILE)
            #integer
            elif (term[len(term) - 2:len(term) - 1]) == 'I':
                try:options[term] = tk.IntVar(value=config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))])
                except:
                    os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt")
                    CONFIG_FILE = createConfigFile("F")
                    readValuesFromConfig(CONFIG_FILE)
            #list
            elif (term[len(term) - 2:len(term) - 1]) == 'L':
                try:
                    if (config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))].split(', ')) == ['']:options[term] = []
                    else: options[term] = config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))].split(', ')
                except:
                    os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt")
                    CONFIG_FILE = createConfigFile("F")
                    readValuesFromConfig(CONFIG_FILE)
        else:
            os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt")
            CONFIG_FILE = createConfigFile("F")
            readValuesFromConfig(CONFIG_FILE)
    return options

def openPreferences(CONFIG_FILE, root):
    options = readValuesFromConfig(CONFIG_FILE)
    updatePreferences(options, CONFIG_FILE, root)

def selectSearchTags(CONFIG_FILE):
    global window
    options = readValuesFromConfig(CONFIG_FILE)
    webScrapingWindow = scanTagsOnline(options, CONFIG_FILE, window)
    if type(webScrapingWindow)!=bool: window = webScrapingWindow

def selectCompare(CONFIG_FILE):
    options = readValuesFromConfig(CONFIG_FILE)
    compareDirectories(CONFIG_FILE)

# set preferences
CONFIG_FILE = createConfigFile("N")
options = readValuesFromConfig(CONFIG_FILE)

#file topmenu button
optionMenu = tk.Frame(root, bg=bg)
optionMenu.pack(fill="both")
menufile = tk.Menubutton(optionMenu, text="File", font=('Proxima Nova Rg', 10), fg="white", bg=bg, anchor="w")
menufile.menu = tk.Menu(menufile, tearoff=0)
menufile["menu"] = menufile.menu
updates = tk.IntVar()
exit = tk.IntVar()
menufile.menu.add_command(label="Exit", font=('Proxima Nova Rg', 10), command=root.destroy)

#option topmenu button
menuoption = tk.Menubutton(optionMenu, text="Option", font=('Proxima Nova Rg', 10), fg="white", bg=bg)
menuoption.menu = tk.Menu(menuoption, tearoff=0)
menuoption['menu'] = menuoption.menu
menuoption.menu.add_command(label="Preferences", font=('Proxima Nova Rg', 10),command=lambda: openPreferences(CONFIG_FILE, root))
menufile.pack(side="left")
menuoption.pack(side="left")

main = tk.Frame(root, bg=bg)
main.pack(fill="both")

imageContainer = tk.Frame(main, bg=bg)
imageContainer.pack(side="left", padx=(20, 0))
fileImageImport = Image.open(resource_path("Vinyl.png"))
fileImageImport = fileImageImport.resize((300, 300), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(fileImageImport)
fileImage = tk.Label(imageContainer, image=photo, bg=bg)
fileImage.image = photo
fileImage.pack(side="left", anchor="w")

textContainer = tk.Frame(main, bg=bg)
textContainer.pack(side="left", padx=(35, 0))
titleLabel = tk.Label(textContainer, text="TRACK\nMANAGEMENT\nUTILITY", font=('Proxima Nova Bold', 55), fg="#ffdd33", bg=bg, justify="left").pack(pady=(25,45))

buttons = tk.Frame(root, bg=bg)
buttons.pack(fill="both")

# Scans for files in a directory and find their tags online
tk.Button(buttons, text="Perform Tag Analysis", command=lambda: selectSearchTags(CONFIG_FILE), font=('Proxima Nova Rg', 13), fg="white", bg=secondary_bg, width=18, height=1).pack(pady=(0,15))
tk.Label(buttons, text="Scan for files in a directory and find their tags online", font=('Proxima Nova Rg', 12), fg="white", bg=bg).pack(pady=(0,35))
# Scans for differences in files between two separate directories
tk.Button(buttons, text="Compare Directories", command=lambda: selectCompare(CONFIG_FILE), font=('Proxima Nova Rg', 13), fg="white", bg=secondary_bg, width=18, height=1).pack(pady=(0,15))
tk.Label(buttons, text="Scan for differences in files and folders between\ntwo separate directories", font=('Proxima Nova Rg', 12), fg="white", bg=bg).pack()
root.mainloop()











