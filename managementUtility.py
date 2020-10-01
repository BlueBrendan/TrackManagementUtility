import tkinter as tk
import getpass
import os
import pyglet
from PIL import Image, ImageTk

#import methods
from compareDrives import compareDrives
from track_preparation.scanTagsOnline import scanTagsOnline
from other.checkForUpdates import checkForUpdates
from other.updatePreferences import updatePreferences

# #add proxima nova regular
# pyglet.font.add_file("C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Proxima Nova Regular.ttf")
# #add proxima nova bold
# pyglet.font.add_file("C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Proxima Nova Bold.otf")
#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

root = tk.Tk()
root.title("Track Management Utility V1.0")
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
x = (ws/2) - (1000/2)
y = (hs/2) - (682/2)
root.geometry('%dx%d+%d+%d' % (1000, 620, x, y))
root.configure(bg=bg)

def createConfigFile(flag):
    CONFIG_FILE = r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt"
    if flag=='F' or (flag=="N" and not os.path.exists(CONFIG_FILE)):
        # create settings folder
        if not os.path.isdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility"):
            path = r"C:/Users/" + str(getpass.getuser()) + "/Documents"
            os.mkdir(path + "/Track Management Utility")
        # create setttings file
        file = open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt", 'w')
        file.write("-GENERAL-\nSubdirectories (B):True\nClose Scraping Window (B):True\nFirst Default Directory (S):\nSecond Default Directory (S):\n\n-SCRAPING SETTINGS-\nScrape Junodownload (B):True\nScrape Beatport (B):True\nScrape Discogs (B):True\nExtract Image from Website (B):True\n\n-IMAGE SCRAPING-\nReverse Image Search (B):True\nDelete Stored Images (B):True\nImage Load Wait Time (I):10\n\n-TAGGING-\nScan Filename and Tags (B):True\nCheck for Numbering Prefix (B):True\nCheck for Extraneous Hyphens (B):True\nCheck for Capitalization (B):True\nAlways Capitalize (L):\nNever Capitalize (L):\nAudio naming format (S):Artist - Title\nSelected Tags (L):Artist, BPM, Genre, Image, Key, Release_Date, ReplayGain, Title\nDelete Unselected Tags (B):False\nCalculate ReplayGain (B):True\nOverwrite existing ReplayGain value (B):False\n")
        file.close()
    return CONFIG_FILE

#handle subdirectory selection
def subdirectorySelection(CONFIG_FILE):
    config_file = open(CONFIG_FILE, 'r').read()
    #if true, turn option to false
    term = "Subdirectories (B)"
    if config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] == "True":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term))+1]) + "True", str(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term))+1])) + "False"))
        file.close()
    #if false, turn option to true
    elif config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] == "False":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1]) + "False", str(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term)) + 1])) + "True"))
        file.close()

def compareDirectories(CONFIG_FILE):
    config_file = open(CONFIG_FILE, 'r').read()
    term = "First Default Directory (S):"
    firstDefaultDirectory = config_file[config_file.index(term) + len(term):config_file.index('\n', config_file.index(term) + len(term))]
    term = "Second Default Directory (S):"
    secondDefaultDirectory = config_file[config_file.index(term) + len(term):config_file.index('\n', config_file.index(term) + len(term))]
    compareDrives(CONFIG_FILE, firstDefaultDirectory, secondDefaultDirectory, root)

def readValuesFromConfig(CONFIG_FILE):
    config_file = open(CONFIG_FILE, 'r').read()
    terms = ["Subdirectories (B)", "Close Scraping Window (B)", "First Default Directory (S)", "Second Default Directory (S)", "Scrape Junodownload (B)", "Scrape Beatport (B)", 'Scrape Discogs (B)', "Extract Image from Website (B)", "Reverse Image Search (B)", "Delete Stored Images (B)", "Image Load Wait Time (I)", "Scan Filename and Tags (B)", "Check for Numbering Prefix (B)", "Check for Extraneous Hyphens (B)", "Check for Capitalization (B)", "Always Capitalize (L)", "Never Capitalize (L)", "Audio naming format (S)", "Selected Tags (L)", "Delete Unselected Tags (B)", "Calculate ReplayGain (B)", "Overwrite existing ReplayGain value (B)"]
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
                try:
                    options[term] = tk.IntVar(value=config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))])
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
    options = readValuesFromConfig(CONFIG_FILE)
    scanTagsOnline(options, CONFIG_FILE)

def selectCompare(CONFIG_FILE):
    options = readValuesFromConfig(CONFIG_FILE)
    compareDirectories(CONFIG_FILE)

# set preferences
CONFIG_FILE = createConfigFile("N")
options = readValuesFromConfig(CONFIG_FILE)
# print(options)

#file topmenu button
optionMenu = tk.Frame(root, bg=bg)
optionMenu.pack(fill="both")
menufile = tk.Menubutton(optionMenu, text="File", font=('Proxima Nova Rg', 10), fg="white", bg=bg, anchor="w")
menufile.menu = tk.Menu(menufile, tearoff=0)
menufile["menu"] = menufile.menu
updates = tk.IntVar()
exit = tk.IntVar()
menufile.menu.add_command(label="Check for Updates", font=('Proxima Nova Rg', 10), command=checkForUpdates)
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
fileImageImport = Image.open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Images/Vinyl.png")
fileImageImport = fileImageImport.resize((300, 300), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(fileImageImport)
fileImage = tk.Label(imageContainer, image=photo, bg=bg)
fileImage.image = photo
fileImage.pack(side="left", anchor="w")

textContainer = tk.Frame(main, bg=bg)
textContainer.pack(side="left", padx=(35, 0))
titleLabel = tk.Label(textContainer, text="TRACK\nMANAGEMENT\nUTILITY", font=('ProximaNova-Bold', 55), fg="#ffdd33", bg=bg, justify="left").pack(pady=(60,45))

buttons = tk.Frame(root, bg=bg)
buttons.pack(fill="both")
# Scans for files in a directory and find their tags online
tk.Button(buttons, text="Perform Tag Analysis", command=lambda: selectSearchTags(CONFIG_FILE), font=('Proxima Nova Rg', 13), fg="white", bg=secondary_bg, width=18, height=1).pack(pady=(0,15))
tk.Label(buttons, text="Scan for files in a directory and find their tags online", font=('Proxima Nova Rg', 12), fg="white", bg=bg).pack(pady=(0,30))
# Scans for differences in files between two separate directories
tk.Button(buttons, text="Compare Directories", command=lambda: selectCompare(CONFIG_FILE), font=('Proxima Nova Rg', 13), fg="white", bg=secondary_bg, width=18, height=1).pack(pady=(0,15))
tk.Label(buttons, text="Scan for differences in files and folders between\ntwo separate directories", font=('Proxima Nova Rg', 12), fg="white", bg=bg).pack()

bottom = tk.Frame(root, bg=bg)
bottom.pack(side="left")
tk.Checkbutton(bottom, var=options['Subdirectories (B)'], activebackground=bg, bg=bg).pack(padx=(10,0), pady=(0, 5), side='left')
tk.Label(bottom, text="Include Subdirectories", font=('Proxima Nova Rg', 12), fg="white", bg=bg).pack(side="left")
root.mainloop()











